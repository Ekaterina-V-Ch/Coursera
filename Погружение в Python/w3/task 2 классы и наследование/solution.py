'''
Как правило задачи про классы не носят вычислительный характер. Обычно нужно написать классы, которые отвечают определенным интерфейсам. 
Насколько удобны эти интерфейсы и как сильно связаны классы между собой, определит легкость их использования в будущих программах.

Предположим есть данные о разных автомобилях и спецтехнике. Данные представлены в виде таблицы с характеристиками. Вся техника разделена 
на три вида: спецтехника, легковые и грузовые автомобили. Обратите внимание на то, что некоторые характеристики присущи только определенному 
виду техники. Например, у легковых автомобилей есть характеристика «кол-во пассажирских мест», а у грузовых автомобилей — габариты кузова: 
«длина», «ширина» и «высота».
Вам необходимо создать свою иерархию классов для данных, которые описаны в таблице. Классы должны называться CarBase (базовый класс для всех 
типов машин), Car (легковые автомобили), Truck (грузовые автомобили) и SpecMachine (спецтехника). Все объекты имеют обязательные атрибуты:

- car_type, значение типа объекта и может принимать одно из значений: «car», «truck», «spec_machine».

- photo_file_name, имя файла с изображением машины, допустимы названия файлов изображений с расширением из списка: «.jpg», «.jpeg», «.png», «.gif»

- brand, марка производителя машины

- carrying, грузоподъемность

В базовом классе CarBase нужно реализовать метод get_photo_file_ext для получения расширения файла изображения. Расширение файла можно получить 
при помощи os.path.splitext.

Для грузового автомобиля необходимо в конструкторе класса определить атрибуты: body_length, body_width, body_height, отвечающие соответственно 
за габариты кузова — длину, ширину и высоту. Габариты передаются в параметре body_whl (строка, в которой размеры разделены латинской буквой «x»). 
Обратите внимание на то, что характеристики кузова должны быть вещественными числами и характеристики кузова могут быть не валидными (например, 
пустая строка). В таком случае всем атрибутам, отвечающим за габариты кузова, присваивается значение равное нулю.

Также для класса грузового автомобиля необходимо реализовать метод get_body_volume, возвращающий объем кузова.

В классе Car должен быть определен атрибут passenger_seats_count (количество пассажирских мест), а в классе SpecMachine — extra (дополнительное описание машины).

Полная информация о атрибутах классов приведена в таблице ниже, где 1 - означает, что атрибут обязателен для объекта, 0 - атрибут должен отсутствовать.
Обратите внимание, что у каждого объекта из иерархии должен быть свой набор атрибутов и методов. Например, у класса легковой автомобиль не должно 
быть метода get_body_volume в отличие от класса грузового автомобиля. Имена атрибутов и методов должны совпадать с теми, что описаны выше.

Далее вам необходимо реализовать функцию get_car_list, на вход которой подается имя файла в формате csv. Файл содержит данные, аналогичные строкам 
из таблицы. Вам необходимо прочитать этот файл построчно при помощи модуля стандартной библиотеки csv. Затем проанализировать строки на валидность и 
создать список объектов с автомобилями и специальной техникой. Функция должна возвращать список объектов.
Первая строка в исходном файле — это заголовок csv, который содержит имена колонок. Нужно пропустить первую строку из исходного файла. Обратите 
внимание на то, что в некоторых строках исходного файла , данные могут быть заполнены некорректно, например, отсутствовать обязательные поля или 
иметь не валидное значение. В таком случае нужно проигнорировать подобные строки и не создавать объекты. Строки с пустым или не валидным значением 
для body_whl игнорироваться не должны.  Вы можете использовать стандартный механизм обработки исключений в процессе чтения, валидации и создания 
объектов из строк csv-файла. Проверьте работу вашего кода с входным файлом, прежде чем загружать задание для оценки.
>>> from solution import *
>>> car = Car('Bugatti Veyron', 'bugatti.png', '0.312', '2')
>>> print(car.car_type, car.brand, car.photo_file_name, car.carrying,
... car.passenger_seats_count, sep='\n')
car
Bugatti Veyron
bugatti.png
0.312
2
>>> truck = Truck('Nissan', 'nissan.jpeg', '1.5', '3.92x2.09x1.87')
>>> print(truck.car_type, truck.brand, truck.photo_file_name, truck.body_length,
... truck.body_width, truck.body_height, sep='\n')
truck
Nissan
nissan.jpeg
3.92
2.09
1.87
>>> spec_machine = SpecMachine('Komatsu-D355', 'd355.jpg', '93', 'pipelayer specs')
>>> print(spec_machine.car_type, spec_machine.brand, spec_machine.carrying,
... spec_machine.photo_file_name, spec_machine.extra, sep='\n')
spec_machine
Komatsu-D355
93.0
d355.jpg
pipelayer specs
>>> spec_machine.get_photo_file_ext()
'.jpg'
>>> cars = get_car_list('cars_week3.csv')
>>> len(cars)
4
>>> for car in cars:
...     print(type(car))
... 
<class 'solution.Car'>
<class 'solution.Truck'>
<class 'solution.Truck'>
<class 'solution.Car'>
>>> cars[0].passenger_seats_count
4
>>> cars[1].get_body_volume()
60.0
>>> 
'''

import csv
import os


class ExCSV:
    '''work with csv'''
    @staticmethod
    def write_CSV(data):
        fieldnames = ['car_type', 'brand', 'photo_file_name', 'carrying', 'passenger_seats_count', 'body_width', 'body_height', 'body_length', 'extra']
        if not os.path.exists('cars.csv'):
            with open('cars.csv', 'w', newline='', encoding='utf-8') as csv_fd:
                writer = csv.DictWriter(csv_fd, delimiter=';', fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(data)
        else:
            with open('cars.csv', 'a', newline='', encoding='utf-8') as csv_fd:
                writer = csv.DictWriter(csv_fd, delimiter=';', fieldnames=fieldnames)
                writer.writerow(data)


class CarBase:
    '''главный класс'''
    '''headclass'''
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = self.text_validity(brand)
        self.photo_file_name = str(self.photo_validity(photo_file_name))
        self.carrying = self.float_validity(carrying)

    @staticmethod
    def photo_validity(photo_file_name):
        '''проверка фото на валидность'''
        '''checking the photo for validity'''
        if list(os.path.splitext(photo_file_name))[1] in ['.jpg', '.jpeg', '.png', '.gif']:
            return photo_file_name
        else:
            return 0

    def get_photo_file_ext(self):
        '''получение расширения фотографии'''
        '''getting a photo extension'''
        return os.path.splitext(self.photo_file_name)[1]

    @staticmethod
    def text_validity(element): 
        '''проверка бренда, допинф на валидность'''
        '''checking brand, extra info for validity'''
        try:
            element = str(element)
            assert element != ''
            assert isinstance(element, str)
            return element
        except AssertionError:
            return 0
        except ValueError:
            return 0
        except IndexError:
            return 0

    @staticmethod
    def int_validity(element):
        '''проверка кол-ва пассажирских мест на валидность'''
        '''checking the number of passenger seats for validity'''
        try:
            element = int(element)
            assert element > 0
            assert isinstance(element, int)
            return element
        except AssertionError:
            return 0

    @staticmethod
    def float_validity(element):
        '''проверка кузова, грузоподъемности на валидность'''
        '''checking the body, carrying capacity for validity'''
        try:
            element = float(element)
            assert element > 0.0
            assert isinstance(element, float)
            return element
        except AssertionError:
            return 0.0
        except ValueError:
            return 0.0

'''дочерние классы'''
'''child classes'''

class Car(CarBase):
    '''машины / cars'''
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        self.car_type = 'car'
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = super().int_validity(passenger_seats_count)
        self.collect_inf(self.car_type, brand, photo_file_name, carrying, passenger_seats_count)

    @staticmethod
    def collect_inf(car_type, brand, photo_file_name, carrying, passenger_seats_count):
        '''сбор информации класса для передачи на экспорт. Если есть хотя бы один элемент 0, код переходит к след списку'''
        '''collection of class information for export. If there is at least one 0 element, the code jumps to the next list'''
        fieldnames = ['car_type', 'brand', 'photo_file_name', 'carrying', 'passenger_seats_count']
        inf = [car_type, brand, photo_file_name, carrying, passenger_seats_count]
        if inf.count(0):
            print('Невалидные значения для ' + brand) # Invalid brand values
        else:
            data = dict(zip(fieldnames, inf))
            ExCSV.write_CSV(data)


class Truck(CarBase): 
    '''грузовики / trucks'''
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        self.car_type = 'truck'
        super().__init__(brand, photo_file_name, carrying)
        self.body_length = self.count_body(self, body_whl, 0)
        self.body_width = self.count_body(self, body_whl, 1)
        self.body_height = self.count_body(self, body_whl, 2)
        self.collect_inf(self.car_type, brand, photo_file_name, carrying, self.body_length, self.body_width, self.body_height)

    @staticmethod
    def collect_inf(car_type, brand, photo_file_name, carrying, body_length, body_width, body_height):
        '''сбор информации класса для передачи на экспорт. Если есть хотя бы один элемент 0, код переходит к след списку'''
        '''collection of class information for export. If there is at least one 0 element, the code jumps to the next list'''
        fieldnames = ['car_type', 'brand', 'photo_file_name', 'carrying', 'body_length', 'body_width', 'body_height']
        inf = [car_type, brand, photo_file_name, carrying, body_length, body_width, body_height]
        valid = [car_type, brand, photo_file_name, carrying]
        if valid.count(0):
            print('Невалидные значения для ' + brand) # Invalid brand values
        else:
            data = dict(zip(fieldnames, inf))
            ExCSV.write_CSV(data)

    @staticmethod
    def count_body(self, body_whl, indx):
        '''определение габаритов кузова'''
        '''determination of body dimensions'''
        try:
            if len(body_whl.split('x')) == 3:
                x = self.float_validity(body_whl.split('x')[indx])
                return x
            else:
                return 0.0
        except:
            return 0.0
    
    '''I am not sure it's working''' ### ВНИМАНИЕ!!!!
    def get_body_volume(self):
        '''получение объема кузова'''
        '''getting body volume'''
        return self.body_length * self.body_width * self.body_height


class SpecMachine(CarBase):
    '''спецмашины / spec_machines'''
    def __init__(self, brand, photo_file_name, carrying, extra):
        self.car_type = 'spec_machine'
        super().__init__(brand, photo_file_name, carrying)
        self.extra = super().text_validity(extra)
        self.collect_inf(self.car_type, brand, photo_file_name, carrying, extra)

    @staticmethod
    def collect_inf(car_type, brand, photo_file_name, carrying, extra):
        '''сбор информации класса для передачи на экспорт. Если есть хотя бы один элемент 0, код переходит к след списку'''
        '''collection of class information for export. If there is at least one 0 element, the code jumps to the next list'''
        fieldnames = ['car_type', 'brand', 'photo_file_name', 'carrying', 'extra']
        inf = [car_type, brand, photo_file_name, carrying, extra]
        if inf.count(0):
            print('Невалидные значения для ' + brand) # Invalid brand values
        else:
            data = dict(zip(fieldnames, inf))
            ExCSV.write_CSV(data)



def get_car_list(csv_filename):
    '''функция на получения списка из файла'''
    '''function to get a list from a file'''
    car_list = []
    with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:  
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            car_list.append(row)
    '''создание индексов по ключам'''
    '''creating indexes by keys'''
    c_t = car_list[0].index('car_type')
    brand = car_list[0].index('brand')
    p_f_n = car_list[0].index('photo_file_name')
    carrying = car_list[0].index('carrying')
    p_s_c = car_list[0].index('passenger_seats_count')
    extra = car_list[0].index('extra')
    b_w = car_list[0].index('body_whl')
    x = len(car_list)
    '''прогон значений внутри листа по индексам'''
    '''iteration of values within a sheet by indices'''
    for i in range(x-1, 0, -1):
        try:
            assert car_list[i][c_t] in ['car', 'truck', 'spec_machine']
            assert type(car_list[i][brand]) is str and car_list[i][brand] != ''
            assert list(os.path.splitext(car_list[i][p_f_n]))[1] in ['.jpg', '.jpeg', '.png', '.gif']
            assert float(car_list[i][carrying]) > 0.0
            if car_list[i][c_t] == 'car':
                assert int(car_list[i][p_s_c]) > 0
                assert car_list[i][b_w] == ''
                assert car_list[i][extra] == ''
                car_list[i] = Car(car_list[i][brand], car_list[i][p_f_n], car_list[i][carrying], car_list[i][p_s_c])
            elif car_list[i][c_t] == 'truck':
                assert car_list[i][p_s_c] == ''
                assert car_list[i][extra] == ''
                if car_list[i][b_w] != '':
                    if list(car_list[i][b_w].split('x')).count('0') == False:
                        x1 = car_list[i][b_w].split('x')[0]
                        x2 = car_list[i][b_w].split('x')[1]
                        x3 = car_list[i][b_w].split('x')[2]
                        car_list[i][b_w] = f'{x1}x{x2}x{x3}'
                else:
                    car_list[i][b_w] = '0.0x0.0x0.0'
                car_list[i] = Truck(car_list[i][brand], car_list[i][p_f_n], car_list[i][carrying], car_list[i][b_w])
            elif car_list[i][c_t] == 'spec_machine':
                assert car_list[i][extra] != ''
                assert car_list[i][p_s_c] == ''
                assert car_list[i][b_w] == ''
                car_list[i] = SpecMachine(car_list[i][brand], car_list[i][p_f_n], car_list[i][carrying], car_list[i][extra])
        except:
            del car_list[i]
    '''удаление листа с ключами'''
    '''deleting a sheet with keys'''
    del car_list[0]
    return car_list