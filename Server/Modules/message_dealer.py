import base64
import gzip
import re

import msgpack
from Crypto.Cipher import AES


class MessageDealer:
    FLAG_COMPRESS = 0x01
    FLAG_MSGPACK = 0x02
    COMPRESS_THRESHOLD = 512  # bytes

    @staticmethod
    def encrypt(message, password: bytes) -> bytes:
        """
        使用AES加密
        message:要加密的消息，接受str或byte类型
        password:秘钥，byte类型，需保证是16位

        """
        if len(password) % 16:
            raise ValueError("秘钥长度非16")
        if type(message) == str:
            message = message.encode()
        if type(message) != bytes:
            raise TypeError("加密数据类型错误")

        lenth = len(message) % 16
        message = message + b'$' * (16 - lenth)
        e = AES.new(password, AES.MODE_ECB).encrypt(message)
        return e

    @staticmethod
    def decrypt(message: bytes, password: bytes):
        """
        使用AES解密
        message:要解密的信息
        """
        if len(password) % 16:
            raise ValueError("秘钥长度非16")
        if type(message) != bytes:
            raise TypeError("加密数据类型错误")
        d = AES.new(password, AES.MODE_ECB).decrypt(message)
        d = d.strip(b'$')
        return d

    @staticmethod
    def enbase64(message) -> bytes:
        """
        转换为base64格式，并添加-S- -E-
        """
        if type(message) == str:
            message = message.encode()
        if type(message) != bytes:
            raise TypeError("加密数据类型错误")
        message = base64.b64encode(message)
        return b"-S-" + message + b"-E-"

    @staticmethod
    def debase64(message: bytes) -> [bytes]:
        """
        从base64格式转出为标准格式，并根据-S- -E-切片
        """
        msg_list = re.findall(b"-S-([^-]*?)-E-", message)
        return [base64.b64decode(item) for item in msg_list]

    @staticmethod
    def engzip(message: bytes) -> bytes:
        res = gzip.compress(message)
        return res

    @staticmethod
    def degzip(message: bytes) -> bytes:
        res = gzip.decompress(message)
        return res

    @staticmethod
    def encode(message: str, password=None) -> bytes:
        """
        将消息编码为带头部的 bytes，再进行可选 AES、base64 封装。
        头部第 1 字节为 flags：
        - bit0: 是否压缩
        - bit1: 是否 msgpack 编码（否则按 utf-8 文本或原始 bytes）
        """
        flags = 0
        payload = None
        if isinstance(message, (dict, list, tuple)):
            payload = msgpack.packb(message, use_bin_type=True)
            flags |= MessageDealer.FLAG_MSGPACK
        elif isinstance(message, str):
            payload = message.encode()
        elif isinstance(message, (bytes, bytearray)):
            payload = bytes(message)
        else:
            raise TypeError("不支持的消息类型: %s" % type(message))

        if len(payload) > MessageDealer.COMPRESS_THRESHOLD:
            payload = MessageDealer.engzip(payload)
            flags |= MessageDealer.FLAG_COMPRESS

        payload = bytes([flags]) + payload
        if password:
            payload = MessageDealer.encrypt(payload, password)
        payload = MessageDealer.enbase64(payload)
        return payload

    @staticmethod
    def decode(message: bytes, password=None) -> [str]:
        """
        解码并返回对象列表（dict/list/str/bytes）。
        """
        chunks = MessageDealer.debase64(message)
        results = []
        for chunk in chunks:
            if password:
                chunk = MessageDealer.decrypt(chunk, password)
            flags = chunk[0]
            payload = chunk[1:]
            if flags & MessageDealer.FLAG_COMPRESS:
                payload = MessageDealer.degzip(payload)
            if flags & MessageDealer.FLAG_MSGPACK:
                try:
                    obj = msgpack.unpackb(payload, raw=False)
                    results.append(obj)
                    continue
                except Exception:
                    pass
            try:
                results.append(payload.decode())
            except Exception:
                results.append(payload)
        return results


if __name__ == "__main__":
    # a = MessageDealer.encrypt("abc", b"1234567887654321")
    # b = MessageDealer.encrypt("def", b"1234567887654321")
    # a = MessageDealer.enbase64(a)
    # b = MessageDealer.enbase64(b)
    # # print(MessageDealer.decrypt(a + b, b"1234567887654321"))
    # print([MessageDealer.decrypt(item, b"1234567887654321") for item in MessageDealer.debase64(a + b)])
    a = MessageDealer.encode("abc")
    b = MessageDealer.encode("def")
    print(MessageDealer.decode(a+b))
