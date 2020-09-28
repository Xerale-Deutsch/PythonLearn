import sys
import socket

# host = sys.argv[1]
# port_list = sys.argv[2].split('-')

host = input("扫描的主机：")
port_list = input("输入起止端口：").split("-")

start_port = int(port_list[0])
end_port = int(port_list[1])

target = socket.gethostbyname(host)
open_ports = []

for port in range(start_port, end_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    result = sock.connect_ex((target, port))
    print("port{0}: {1}".format(port, result))
    if result == 0:
        open_ports.append(port)

print("Opened-ports:")
for port in open_ports:
    print(port)
