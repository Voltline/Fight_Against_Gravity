import socket
import send_email
import database_operate as db
import aes
from time import ctime
class TCPServer:
    def __init__(self, PORT, BUFFSIZE, MAX_LISTEN):
        self.__PORT = PORT
        self.__BUFFSIZE = BUFFSIZE
        self.__MAX_LISTEN = MAX_LISTEN
        self.__HOST = ''
        self.__ADDR = (self.__HOST, self.__PORT)
    def Start_Register(self):
        # TCP服务
        # with socket.socket() as s:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # 绑定服务器地址和端口
            s.bind(self.__ADDR)
            # 启动服务监听
            s.listen(self.__MAX_LISTEN)
            print('等待用户接入。。。。。。。。。。。。')
            aes_password = ''
            for i in range(3):
                # 等待客户端连接请求,获取connSock
                conn, addr = s.accept()
                print('警告，远端客户:{} 接入系统！！！'.format(addr))
                db.insert_connection_data([str(addr), str(ctime())])
                with conn:
                    print('接收请求信息。。。。。')
                    # 接收请求信息
                    data = conn.recv(self.__BUFFSIZE)
                    print('data=%s' % data)
                    print('接收数据：{!r}'.format(data.decode('utf-8')))
                    if aes_password == '':
                        print("第一次接入获取密钥")
                        aes_password = getPassword(data)
                    else:
                        data = process(data, aes_password)
                        if data != "":
                            try:
                                conn.send(data.encode('utf-8'))
                            except AttributeError:
                                conn.send(data)
                        print('发送返回完毕！！！')

def getPassword(Data : bytes) -> bytes:
    """获取密钥.
    :参数: Data 为bytes类型Base64编码
    :返回: AES密钥
    """
    password = ''
    with open("../password.txt", 'r') as f:
        password = bytes(f.read(), encoding='utf-8')
        f.close()
    ans = bytes(aes.aes_decrypt(password, Data), encoding='utf-8')
    print(ans)
    return ans

def process(Data : bytes, password : bytes) -> str:
    """处理数据.
    :参数: Data：bytes类型Base64编码，password：bytes类型AES密钥
    :返回: 处理结果
    """
    print(type(Data))
    print(Data)
    data = aes.aes_decrypt(password, Data)
    # try:
    data_list = eval(data)
    if len(data_list) == 2:
        print("第二次接入返回验证码")
        check_code = send_email.generate_id_code()
        send_email.send_email(data_list[0], data_list[1], check_code)
        data = check_code
    else:
        print("第三次接入传入具体信息")
        result = db.insert_acc_data(data_list)
        if result:
            data = "True"
    return data
    # except:
    #     return ''


if __name__ == '__main__':
    PORT = 25555
    BUFFSIZE = 1024
    MAX_LISTEN = 5
    Identify_Sever = TCPServer(PORT, BUFFSIZE, MAX_LISTEN)
    while True:
        print('execute tcpsever')
        while True:
            try:
                Identify_Sever.Start_Register()
            except:
                pass
