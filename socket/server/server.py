import socket
from threading import Thread

address = (socket.gethostname(), 25555)
g_socket_server = None
g_conn_poll = []


def init():
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    g_socket_server.bind(address)
    g_socket_server.listen(5)
    print("staring, wating for client")


def accept_client():
    while(True):
        client, address = g_socket_server.accept()
        print("a client %s connected" % (str(address)))
        client.sendall("accepted".encode(encoding="utf-8"))
        g_conn_poll.append((client, address))
        thread = Thread(target=message_handle, args=(client, address))
        thread.setDaemon(True)
        thread.start()


def message_handle(client: socket.socket, address):
    while(True):
        try:
            recv = client.recv(1024)
        except:
            g_conn_poll.remove((client, address))
            print("a client left unexcpted")
            break
        if(len(recv) == 0):
            client.sendall("closing".encode())
            client.close()
            g_conn_poll.remove((client, address))
            print("a client left")
            break
        client.sendall("status:200".encode())
        print("message from" + str(address) +
              ":" + recv.decode(encoding="utf-8"))


if __name__ == "__main__":
    init()
    thread = Thread(target=accept_client)
    thread.setDaemon(True)
    thread.start()
    while(True):
        cmd = input("")
