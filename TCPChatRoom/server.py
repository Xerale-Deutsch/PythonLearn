import socket
import threading


def tcp_connect(sock, addr):
    info = sock.recv(1024).decode().split("----")
    client_name = info[0]
    print("Accept new connection from {0}:{1}".format(*addr))
    sock.send("Welcome! {0}".format(client_name).encode())
    for client in client_list:
        client[0].send("{0}----{1} enter this chatroom.".format("Server", client_name).encode())

    while 1:
        try:
            data = sock.recv(1024).decode()
            if data:
                name_message = data.split('----')
                name = name_message[0]
                message = name_message[1]

                for client in client_list:
                    client[0].send("{0}----{1}".format(name, message).encode())

        except ConnectionResetError:
            client_list.remove((sock, addr))
            if len(client_list) > 0:
                message = "{0} has leave this chatroom.".format(client_name)
                for client in client_list:
                    client[0].send("{0}----{1}".format("Server", message).encode())
            break


    sock.close()
    print("Connection from {0}:{1} closed.".format(*addr))


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('0.0.0.0', 4444))
    server_sock.listen()
    print("Waiting for connection...")

    # 接收多个客户端请求
    while 1:
        sock, addr = server_sock.accept()
        client_list.append((sock, addr))
        t = threading.Thread(target=tcp_connect, args=(sock, addr))
        t.start()
    server_sock.close()


if __name__ == '__main__':
    client_list = []
    main()

