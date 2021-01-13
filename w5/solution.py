# клиент для отправки метрик


import socket
import time


class ClientError(Exception):
    pass

class Client(object):

    def __init__(self, host, port, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)
    
    def put(self, key, value, timestamp=None):
        if timestamp is None:
            timestamp=int(time.time())

        try:
            self.sock.sendall(f'put {key} {value} {timestamp}\n'.encode('utf-8'))
            self.checking_values()
        except:
            raise ClientError

            

    def get(self, id):
        try:
            self.sock.sendall(f'get {id}\n'.encode('utf-8'))
        except:
            raise ClientError
        while True:
            data = self.checking_values()
            print_dict = {}
            if len(data) == 0:
                return print_dict
            else:
                try:
                    data.sort(key=lambda i: i.split(' ')[2])
                    for i in range(0, len(data)):
                        key, val, t = data[i].split(' ')
                        assert float(val)
                        assert int(t)
                        if key in print_dict.keys():
                            print_dict[key].append((int(t), float(val)))
                        else:
                            print_dict[key] = [(int(t), float(val))]
                    return print_dict
                except:
                    raise ClientError


    def checking_values(self):
        try:
            data = self.sock.recv(1024)
            data = bytes(data)
            data = data.decode('utf-8')
        except socket.error:
            raise ClientError

        b = list(data.split('\n'))
        if b[0] == 'error':
            raise ClientError
        elif b[0] == 'ok':
            return b[1:-2]
        else:
            raise ClientError


