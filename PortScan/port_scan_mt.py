import socket
import threading
import queue


def tcp_scan(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((target_ip, port))

    if result == 0:
        lock.acquire()
        print("Opened-port：{0}".format(port))
        lock.release()


def work():
    while not q.empty():
        job = q.get()
        tcp_scan(job)


def go():
    thread_list = []
    for port in range(port_start, port_end):
        q.put(port)
    for i in range(thread_num):
        thread = threading.Thread(target=work)
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    target_ip = input("输入要扫描的ip地址：")
    port_list = input("输入要扫描的起止端口：").split('-')
    port_start = int(port_list[0])
    port_end = int(port_list[1])
    lock = threading.Lock()
    q = queue.Queue()
    thread_num = int(input("请输入线程数量："))
    go()

