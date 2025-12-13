import asyncio
import queue
import socket
import threading
from typing import Dict, Tuple, Optional

import json
import msgpack

from Server.Modules.Flogger import Flogger
from Server.Modules.message_dealer import MessageDealer


class SocketServer:
    """
    基于 asyncio 的 TCP 服务器封装。
    - 单线程事件循环，避免每连接一线程的开销
    - 心跳超时控制（可选）
    - 收/发消息统一通过 MessageDealer 处理
    """

    def __init__(self, ip: str, port: int, heart_time: int = -1, debug: bool = False,
                 msg_len: int = 1024, password: str = None,
                 models=Flogger.DLOGG, logpath=None, level=Flogger.L_INFO):
        self.logger = Flogger(models, logpath, level, folder_name="safeserver")
        self.heart_time = heart_time
        """心跳检测（秒），<=0 关闭"""
        self.__host = ip
        self.__port = port
        self.que = queue.Queue()
        """消息队列 [（address， recv）]"""
        self._connections: Dict[Tuple[str, int], asyncio.StreamWriter] = {}
        """连接池 {address : writer}"""
        self.conn_poll = self._connections  # 兼容旧命名
        self.debug = debug
        """debug选项"""
        self.msg_len = msg_len
        """消息长度（建议短"""
        self.password = None
        """加密选项,如需加密请直接输入秘钥"""
        if password:
            self.password = password.encode()
        if (password is not None) and (len(password) != 16):
            self.logger.error("秘钥长度非16:" + password)
            exit(-1)

        self.logger.info("heart time：" + str(self.heart_time))
        self.logger.info("ip:" + str(self.__host) + " port:" + str(self.__port))
        self.logger.info("message length:" + str(self.msg_len))
        self.logger.info("debug:" + str(self.debug))
        self.logger.info("Encrypt message %s" % ("on" if password else "off"))

        self._loop = asyncio.new_event_loop()
        self._server_task: Optional[asyncio.Task] = None
        self._server_thread = threading.Thread(target=self._run_loop, name="async_socket_server", daemon=True)
        self._server_ready = threading.Event()
        self._lock = threading.Lock()
        self._server_thread.start()
        # 等待事件循环启动，避免初始化后立即访问连接池为空导致的异常
        if not self._server_ready.wait(timeout=5):
            self.logger.error("Fail to start async socket server within 5 seconds")
            raise RuntimeError("socket server failed to start")
        if self._server_task and self._server_task.done():
            # 触发异常抛出
            self._server_task.result()

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._server_task = self._loop.create_task(self._start_server())
        self._loop.run_forever()

    async def _start_server(self):
        try:
            server = await asyncio.start_server(self._handle_client, self.__host, self.__port,
                                                limit=self.msg_len)
            addresses = ", ".join(str(sock.getsockname()) for sock in server.sockets or [])
            self.logger.info("server started on %s" % addresses)
            self._server_ready.set()
            async with server:
                await server.serve_forever()
        except Exception as err:
            self.logger.error("Fail to build a socket listener: %s" % err)
            self._server_ready.set()
            raise

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        address = writer.get_extra_info("peername")
        if address is None:
            address = ("unknown", 0)
        self.logger.info("client %s connected" % (address,))
        raw_socket = writer.get_extra_info("socket")
        if raw_socket:
            raw_socket.setsockopt(socket.SOL_SOCKET, socket.TCP_NODELAY, True)
        with self._lock:
            self._connections[address] = writer

        try:
            while True:
                try:
                    if self.heart_time > 0:
                        recv = await asyncio.wait_for(reader.read(self.msg_len), timeout=self.heart_time)
                    else:
                        recv = await reader.read(self.msg_len)
                except asyncio.TimeoutError as err:
                    self.logger.info("连接%s超时%s" % (address, err))
                    break
                except Exception as err:
                    self.logger.info("连接%s意外断开%s" % (address, err))
                    break

                if not recv:
                    self.logger.info("连接%s客户端主动断开" % (address,))
                    break

                tmpmsg = MessageDealer.decode(recv, self.password)
                for message in tmpmsg:
                    try:
                        if isinstance(message, (dict, list)):
                            parsed = message
                        elif isinstance(message, (bytes, bytearray)):
                            parsed = msgpack.unpackb(message, raw=False)
                        else:
                            parsed = json.loads(message)
                        if isinstance(parsed, dict) and parsed.get("opt", 0) != 0:
                            self.logger.debug("receive msg {} from {}".format(parsed, address))
                        self.que.put((address, parsed))
                    except Exception as err:
                        self.logger.warning("消息{}不是json格式报文,未解析".format(message) + str(err))
                        self.que.put((address, message))
        finally:
            with self._lock:
                self._connections.pop(address, None)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as err:
                self.logger.warning("关闭连接{}异常{}".format(address, err))
            self.logger.info("连接{}断开".format(address))

    def get_message(self):
        """
        返回当前消息队列中的所有消息
        格式[(address, msg)]
        """
        res = []
        while not self.que.empty():
            res.append(self.que.get())
        return res

    def get_connection(self) -> list:
        """
        放回连接池中的address
        """
        with self._lock:
            return list(self._connections.keys())

    async def _async_close(self, address):
        writer = None
        with self._lock:
            writer = self._connections.pop(address, None)
        if writer:
            try:
                writer.close()
                await writer.wait_closed()
            except Exception as err:
                self.logger.warning("[in close]%s 连接关闭异常" % err)
        else:
            self.logger.error("[in close]连接未找到: %s" % (address,))

    def close(self, address):
        """
        关闭指定连接
        """
        asyncio.run_coroutine_threadsafe(self._async_close(address), self._loop)

    async def _async_send(self, address, message: bytes):
        writer = self._connections.get(address)
        if writer is None:
            self.logger.error("[in send]连接未找到: %s" % (address,))
            return
        try:
            writer.write(message)
            await writer.drain()
        except Exception as err:
            self.logger.error("[in send]" + str(err) + "发送失败")

    def send(self, address, message):
        """
        msg:支持dict（json）/str格式
        """
        try:
            if isinstance(message, dict):
                message = json.dumps(message)
            self.logger.debug("{send %d lenth msg to %s}:%s" % (len(message), address, message))
            encoded = MessageDealer.encode(message, self.password)
            fut = asyncio.run_coroutine_threadsafe(self._async_send(address, encoded), self._loop)
            fut.result(timeout=2)
        except Exception as err:
            self.logger.error("[in send]" + str(err) + "发送失败")


if __name__ == "__main__":
    ip = "localhost"
    port = 25555
    online = False
    if online:
        ip = "192.168.0.57"
    server = SocketServer(ip, port, heart_time=10, debug=False, msg_len=8192,
                          password="0123456789abcdef")
    while True:
        messages = server.get_message()
        for item in messages:
            print(item)
            address = item[0]
            msg = {
                "opt": -1,
                "info": item
            }
            # print(msg)
            server.send(address, msg)
        lt = server.get_connection()
