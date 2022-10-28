from Web.SafeSocket import safeclient
from Web.SafeSocket import safeserver
import send_email
import database_operate
import json
import time

email_sent = {}
user_list = []  # {"username" : address}


def reg_server(ip: str, port: int, heart_time: int = -1) -> None:
    """注册服务器
    :参数: ip: 服务器ip， port: 端口， heart_time: 心跳时间（默认-1）
    :返回: 无返回
    """
    server = safeserver.SocketSever(ip, port)
    server.start()
    sttm = time.time()
    while True:
        if time.time() - sttm > 4:
            print(user_list)
            sttm = time.time()
        messages = server.get_message()
        for message in messages:
            addr = message[0] # addr : client's address
            rmessage = json.loads(message[1])
            user_list.append({rmessage["user"]: message[0]})
            print(rmessage)
            username, email = rmessage["user"], rmessage["email"]
            if rmessage["opt"] == 1:
                email_sent[(username, email)] = True
                id_code = send_email.generate_id_code()
                send_email.send_email(username, email, id_code)
                server.send(addr, id_code)
            elif rmessage["opt"] == 2:
                if (username, email) in email_sent:
                    password = rmessage["password"]
                    time_n = time.ctime()
                    database_operate.insert_acc_data([username, password, time_n, email])
                    email_sent.pop((username, email))

                else:
                    server.send(addr, "ERROR")
                server.close(addr)
            else:
                print("unexpected opt")
        # 处理超时链接
        get_user_list = server.get_message()



if __name__ == "__main__":
    _debug_ = 1
    ip = "localhost"
    port = 25555
    reg_server(ip, port)

