import sys
import socket

if len(sys.argv) not in [2,3]:
    print("Number of arguments required is 1 atleast !!")
    exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = sys.argv[1] 
if len(sys.argv) == 3:
    try:
        port = int(sys.argv[2])
        if not (1 <= port <= 65535):
            raise ValueError
    except ValueError:
        print("Invalid port number")
else:
    port = 80

try:
    connect = sock.connect((address, port))
except socket.timeout:
    print(f"Dead server {address} seems to be dead !!")
except socket.gaierror:
    print(f"Some kind of gai error !!!")

request = b"HEAD / HTTP/1.1\r\nHost:"+bytes(address,"utf8")+b"\r\nConnection:Close\r\n\r\n"
sock.send(request)
reply = sock.recv(500).decode("utf8")
sock.shutdown(socket.SHUT_RDWR)
sock.close()
print(reply[:reply.find("\r")])