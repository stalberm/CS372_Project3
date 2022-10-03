import socket
import sys

host = sys.argv[1]
if len(sys.argv) > 2:
    port = int(sys.argv[2])
else:
    port = 80
sock = socket.socket()
sock.connect((host, port))
s = f"GET /file2.html HTTP/1.1\r\n\
Host: {host}\r\n\
Connection: close\r\n\r\n"
s = s.encode("ISO-8859-1")
sock.sendall(s)
response = ''
while True: 
    chunk = sock.recv(4096)
    if len(chunk) == 0:
        break
    response = response + chunk.decode("ISO-8859-1")
sock.close()
print(response)

