# сервер для приема метрик


import asyncio


class Repository:
    
    def __init__(self):
        self.inf_list = []

    def put(self, data):

        data_str = ' '.join(data) + '\n'
        for element in self.inf_list:
            j = element.strip('\n').split(' ')
            if j[2] == data[2] and j[0] == data[0]:
                i = self.inf_list.index(element)
                self.inf_list[i] = data_str
        if data_str in self.inf_list:
            i = self.inf_list.index(data_str)
            self.inf_list[i] = data_str
        if data_str not in self.inf_list:
            self.inf_list.append(data_str)
        return 'ok\n\n'
        

    def get(self, key):
        inf = ''
        if key == '*':
            for element in self.inf_list:
                inf += element
        else:
            for element in self.inf_list:
                if element.split(' ')[0] == key:
                    inf += element
        return 'ok\n' + inf + '\n'


class Process_data:

    def __init__(self, repository):
        self.repository = repository

    def run(self, data):
        client_command = data[0]
        metrics = data[1:]
        if client_command == 'put' and len(metrics) == 3:
            try:
                if metrics[1] != '0.0':
                    metrics[1] = str(float(metrics[1]))
                metrics[2] = str(int(metrics[2]))
                return self.repository.put(metrics)
            except:
                return 'error\nwrong command\n\n'
            
        elif client_command == 'get' and len(metrics) == 1:
            return self.repository.get(metrics[0])
        else:
            return 'error\nwrong command\n\n'
        


class ServerClientProtocol(asyncio.Protocol):

    repository = Repository()

    def __init__(self):
        super().__init__()
        self.process_data = Process_data(self.repository)

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if len(data.decode().strip('\n') + 'a') != 1:
            resp = self.process_data.run(data.decode().strip('\n').split(' '))
        else:
            resp = 'error\nwrong command\n\n'
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ServerClientProtocol, host, port)
    server = loop.run_until_complete(coro)
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


