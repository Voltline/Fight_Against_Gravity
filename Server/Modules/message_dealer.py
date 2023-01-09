import gzip
import json
import re
import base64
from Crypto.Cipher import AES


class MessageDealer:
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
        return d.decode()

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
        if type(message) == str:
            message = message.encode()
        if type(message) != bytes:
            raise TypeError("加密数据类型错误")
        # print(message)
        if password:
            message = MessageDealer.encrypt(message, password)
            # print(message)
        message = MessageDealer.engzip(message)
        message = MessageDealer.enbase64(message)
        return message

    @staticmethod
    def decode(message: bytes, password=None) -> [str]:
        message = MessageDealer.debase64(message)
        message = [MessageDealer.degzip(item) for item in message]
        if password:
            message = [MessageDealer.decrypt(item, password) for item in message]
        else:
            message = [item.decode() for item in message]
        return message


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
