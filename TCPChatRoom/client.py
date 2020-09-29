import socket
import threading


def recv_data():
    while 1:
        data = client_sock.recv(1024).decode().split("----")
        data = "[{0}]: {1}".format(data[0], data[1])
        print(data)


def send_data():
    while 1:
        data = input()
        data = "{0}----{1}".format(name, data)
        client_sock.send(data.encode())


def main():
    info = "{0}----{1}".format(name, socket.gethostbyname("localhost"))
    client_sock.send(info.encode())
    connect_info = client_sock.recv(1024).decode()
    print("[Server]: {0}".format(connect_info))
    send_thread = threading.Thread(target=send_data)
    recv_thread = threading.Thread(target=recv_data)
    send_thread.start()
    recv_thread.start()


if __name__ == '__main__':
    server_ip = input("请输入服务器IPv4地址：")
    name = input("请输入用户名：")
    addr = (server_ip, 4444)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect(addr)

    main()


