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