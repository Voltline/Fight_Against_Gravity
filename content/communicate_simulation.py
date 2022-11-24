"""在本地模拟本地与服务端的通信"""
from queue import Queue

msg_to_server = Queue(1000)
msg_to_client = Queue(1000)


def server_send(args=None, kwargs=None):
    """位置参数元组args，关键字参数字典kwargs"""
    msg = (args.copy(), kwargs.copy())
    msg_to_server.put(msg)


def client_send(args=None, kwargs=None):
    msg = (args.copy(), kwargs.copy())
    msg_to_client.put(msg)


def client_receive() -> (list, dict):
    """一次取一个，没有则返回None"""
    if not msg_to_client.empty():
        return msg_to_client.get()
    else:
        return None, None


def server_receive() -> (list, dict):
    """一次取一个，没有则返回None"""
    if not msg_to_server.empty():
        return msg_to_server.get()
    else:
        return None, None


def client_get_room_id() -> int:
    return 1
