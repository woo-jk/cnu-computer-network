import os
import sys
import socket
import time
import threading

HOST = ''
PORT = 8080

def worker(conn, addr):
    print(f'Connected by {addr}')
    data = conn.recv(1500)
    ptr = data.find('\r\n'.encode('utf-8'))
    header = data[:ptr]
    left = data[ptr:]
    request = header.decode('utf-8')
    method, path, protocol = request.split(' ')
    print(f'Received: {method} {path} {protocol}')
    if not data:
        return
    if path == '/':
        path = '/index.html'
    path = f'.{path}'
    if not os.path.exists(path):
        path = './notfound.html'
        header = 'HTTP/1.1 404 Not Found\r\n'
    else :
        header = 'HTTP/1.1 200 OK\r\n'
    
    if os.path.splitext(path)[1] != '.jpg' or os.path.splitext(path)[1] == '.jpeg':
        with open(path, 'r') as f:
            body = f.read()
            body = body.encode('utf-8')
    else :
        with open(path, 'rb') as f:
            body = f.read()
            
    header = f'{header}Server: Our server\r\n'
    header = f'{header}Connection: close\r\n'
    
    if os.path.splitext(path)[1] == '.html':
        header = f'{header}Content-Type: text/html;charset=utf-8\r\n'
        header = f'{header}Accept: text/html, text/css, text/javascript, image/jpeg\r\n'
    if os.path.splitext(path)[1] == '.css':
        header = f'{header}Content-Type: text/css; charset=utf-8\r\n'
    if os.path.splitext(path)[1] == '.js':
        header = f'{header}Content-Type: text/javascript; charset=utf-8\r\n'
    if os.path.splitext(path)[1] == '.jpg' or os.path.splitext(path)[1] == '.jpeg':
        header = f'{header}Content-Type: image/jpeg\r\n'
    header = f'{header}Content-Length: {len(body)}\r\n'
    header = f'{header}\r\n'
    header = header.encode('utf-8')
    response = header + body
    conn.sendall(response)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f'Start server with {sys.argv}')
    while True:
        try:
            conn, addr = s.accept()
            thread = threading.Thread(target=worker,
                                      args=(conn, addr))
            thread.start()
            print(f'Start child worker {thread}')
        except KeyboardInterrupt:
            print('Shutdown server')
            for thread in threading.enumerate():
                if thread.getName() == 'MainThread':
                    continue
                print('Join thread {0}'.format(thread))
                thread.join(timeout=1)
            break

