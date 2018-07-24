import sys

# for importing helper classes
sys.path.append("..")

import socket
import pickle
from helper_classes import Job, Individual
import eval_cnn

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 4123              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    data = conn.recv(1024)
    conn.close()
    training_data = pickle.loads(data)
    assert(isinstance(training_data, Job))
    eval_cnn.eval_network(training_data.individual, training_data.epochs, training_data.seed)


