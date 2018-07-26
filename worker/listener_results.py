import socket
import os

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 4124              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)
    if b"RDY?" in data:
        if not os.path.isfile("result"):
            conn.send(b"BSY")
        else:
            with open("result", "rb") as f:
                res = f.read()
                conn.sendall(res)
                print("Sending results...")
            os.remove("result")
    conn.close()
s.close()

