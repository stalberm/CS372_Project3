import socket
import sys
import os

if len(sys.argv) > 1:
    if sys.argv[1].isnumeric():
        port = sys.argv[1]
    else:
        sys.exit(f"Invalid Port Number: {sys.argv[1]}")
else:
    port = 28333
 
extMap = {".txt" : "text/plain", ".html" : "text/html", ".ico" : "image/x-icon"}

s = socket.socket()
s.bind(('', int(port)))
s.listen()

while True:
    new_conn = s.accept()
    new_socket = new_conn[0]

    request = b''
    while True:
        chunk = new_socket.recv(4096)
        request = request + chunk
        if request.find(b"\r\n\r\n"):
            break
    request = request.decode("ISO-8859-1")

    path = request.split("\r\n")[0].split()[1]
    print(path)

    filename = os.path.split(path)[1]
    print(os.path.splitext(filename)[1])

    try:
        with open(filename) as fp:
            data = fp.read()   # Read entire file
            length = len(data.encode("ISO-8859-1"))
            MIMEType = extMap[os.path.splitext(filename)[1]]
            response = f"HTTP/1.1 200 OK\r\n\
Content-Type: {MIMEType}; charset=iso-8859-1\r\n\
Content-Length: {length}\r\n\
Connection: close\r\n\r\n" + data

    except:
        # File not found or other error
        response = f"HTTP/1.1 404 Not Found\r\n\
Content-Type: text/plain\r\n\
Content-Length: 13\r\n\
Connection: close\r\n\r\n\
404 not found"
    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()