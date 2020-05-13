#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
while True:
    s.listen(5)
    conn, addr = s.accept()
    print('Connected by', addr)
    print('Connected by', conn)
    while True:
        data = conn.recv(1024)

        conn.sendall(data)