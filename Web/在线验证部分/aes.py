from Crypto.Cipher import AES
import random
import base64


def decode_base64(data: bytes) -> bytes:
    """解码base64, 不满足条件时补'='.
    :参数: data 为bytes类型Base64编码
    :返回: 解码后的Base64编码
    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'=' * missing_padding
    return base64.b64decode(data)


def generate_id_code() -> str:
    """generate_id_code
    :返回：生成一个十六位随机密钥用于AES加密
    """
    char_check = ''
    for i in range(16):
        # 生成一个不包括0,o和O的字符
        char1 = random.choice([chr(random.randint(65, 78)), chr(random.randint(80, 90)), str(random.randint(1, 9)),
                               chr(random.randint(97, 110)), chr(random.randint(112, 122))])
        char_check += char1
    return char_check


def trans_typ_detext(content: str) -> bytes:
    """转换文本函数
    :参数：content: 内容字符串
    :返回：content转换为bytes后再补字符为16的整数倍得到的bytes
    """
    content = bytes(content, encoding='utf-8')
    while len(content) % 16 != 0:
        content += b'\x00'
    return content


def aes_encrypt(password: bytes, content: str) -> bytes:
    """AES加密函数
    :参数：password：密钥，content：内容
    :返回：密文Base64编码
    """
    aes = AES.new(password, AES.MODE_ECB)
    text = trans_typ_detext(content)
    en_text = base64.b64encode(aes.encrypt(text))
    return en_text


def aes_decrypt(password: bytes, en_text: bytes) -> str:
    """AES解密函数
    :参数：password：密钥，content：内容
    :返回：字符串类型明文
    """
    aes = AES.new(password, AES.MODE_ECB)
    den_text = aes.decrypt(decode_base64(en_text))
    den_text = den_text.replace(b'\x00', b'')
    return str(den_text, encoding='utf-8')
