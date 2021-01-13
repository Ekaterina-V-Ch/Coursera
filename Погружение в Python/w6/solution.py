'''
На предыдущей неделе вы разработали клиентское сетевое приложение — клиента для сервера метрик, который умеет отправлять и получать всевозможные метрики. Пришло время финального задания — нужно реализовать серверную часть самостоятельно.
Как обычно вам необходимо разработать программу в одном файле-модуле, который вы загрузите на проверку обычным способом. Сервер должен соответствовать протоколу, который был описан в задании к предыдущей неделе. Он должен уметь принимать от клиентов команды put и get, разбирать их, и формировать ответ согласно протоколу. По запросу put требуется сохранять метрики в структурах данных в памяти процесса. По запросу get сервер обязан отдавать данные в правильной последовательности.
На верхнем уровне вашего модуля должна быть объявлена функция run_server(host, port) — она принимает адрес и порт, на которых должен быть запущен сервер.
Для проверки правильности решения мы воспользуемся своей реализацией клиента и будем отправлять на ваш сервер put и get запросы, ожидая в ответ правильные данные от сервера (согласно объявленному протоколу). Все запросы будут выполняться с таймаутом — сервер должен отвечать за приемлемое время.
Сервер должен быть готов к неправильным командам со стороны клиента и отдавать клиенту ошибку в формате, оговоренном в протоколе. В таком случае работа сервера не должна завершаться аварийно.
На последней неделе мы с вами разбирали пример tcp-сервера на asyncio:
import asyncio
class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())
loop = asyncio.get_event_loop()
coro = loop.create_server(
    ClientServerProtocol,
    '127.0.0.1', 8181
)
server = loop.run_until_complete(coro)
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
Данный код создает tcp-соединение для адрса 127.0.0.1:8181 и слушает все входящие запросы. При подключении клиента будет создан новый экземпляр класса ClientServerProtocol, а при поступлении новых данных вызовется метод этого объекта - data_received. Внутри asyncio.Protocol спрятана вся магия обработки запросов через корутины, остается реализовать протокол взаимодействия между клиентом и сервером.
Этот код может использоваться как основа для реализации сервера. Это не обязательное требование. Для реализации задачи вы можете использовать любые вызовы из стандартной библиотеки Python 3. Сервер должен обрабатывать запросы от нескольких клиентов одновременно.
В процессе разработки сервера для тестирования работоспособности вы можете использовать клиент, написанный на предыдущей неделе.
Давайте еще раз посмотрим на текстовый протокол в действии при использовании утилиты telnet:
$: telnet 127.0.0.1 8888
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
> get test_key
< ok
< 
> got test_key
< error
< wrong command
< 
> put test_key 12.0 1503319740
< ok
< 
> put test_key 13.0 1503319739
< ok
< 
> get test_key 
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< 
> put another_key 10 1503319739
< ok
< 
> get *
< ok
< test_key 13.0 1503319739
< test_key 12.0 1503319740
< another_key 10.0 1503319739
< 
'''



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


