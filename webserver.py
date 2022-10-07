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
 
extMap = {
    ".txt" : "text/plain",
    ".html" : "text/html",
    ".ico" : "image/x-icon",
    ".gif" : "image/gif"
    }

s = socket.socket()
s.bind(('', int(port)))
s.listen()


def get_requested_file_name(request):
    #Split request by new lines, first line is the GET
    try:
        GET_reqst = request.split("\r\n")[0]
        #Split GET request and grab the path
        path = GET_reqst.split()[1]
        #Strip the filename from the path
        filename = os.path.split(path)[1]
    except:
        #If request was bad, return no filename - leads to 404
        filename = ''
    return filename

def get_request_header():
    request = b''
    while True:
        chunk = new_socket.recv(4096)
        request = request + chunk
        if request.find(b"\r\n\r\n"):
            break
    request = request.decode("ISO-8859-1")
    return request

def construct_response(filename):
    try:
        with open(filename) as fp:
            extension = os.path.splitext(filename)[1]
            data = fp.read()   # Read entire file
            length = len(data.encode("ISO-8859-1"))
            MIMEType = extMap[extension]
            response = f"HTTP/1.1 200 OK\r\n"\
                        f"Content-Type: {MIMEType}; charset=iso-8859-1\r\n"\
                        f"Content-Length: {length}\r\n"\
                        "Connection: close\r\n\r\n" + data

    except:
        # File not found or other error
        response = f"HTTP/1.1 404 Not Found\r\n"\
                    "Content-Type: text/plain\r\n"\
                    "Content-Length: 13\r\n"\
                    "Connection: close\r\n\r\n"\
                    "404 not found"
    return response
while True:
    new_conn = s.accept()
    new_socket = new_conn[0]

    request = get_request_header()
    filename = get_requested_file_name(request)

    response = construct_response(filename)

    new_socket.sendall(response.encode("ISO-8859-1"))
    new_socket.close()