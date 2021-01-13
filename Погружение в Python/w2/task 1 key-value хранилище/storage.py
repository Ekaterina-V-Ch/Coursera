'''
На этой неделе мы с вами реализуем собственный key-value storage. Вашей задачей будет написать скрипт, который принимает в качестве аргументов ключи и значения и выводит информацию из хранилища (в нашем случае — из файла).
Запись значения по ключу
> storage.py --key key_name --val value
Получение значения по ключу
> storage.py --key key_name
Ответом в данном случае будет вывод с помощью print соответствующего значения
> value
или
> value_1, value_2
если значений по этому ключу было записано несколько. Метрики сохраняйте в порядке их добавления. Обратите внимание на пробел после запятой.
Если значений по ключу не было найдено, выводите пустую строку или None.
Для работы с аргументами командной строки используйте модуль argparse. Вашей задачей будет считать аргументы, переданные вашей программе, и записать соответствующую пару ключ-значение в файл хранилища или вывести значения, если был передан только ключ. Хранить данные вы можете в формате JSON с помощью стандартного модуля json. Проверьте добавление нескольких ключей и разных значений.
Файл следует создавать с помощью модуля tempfile.
'''


import os
import tempfile
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument("--key", required=True)
parser.add_argument("--val")

args = parser.parse_args()


storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

def have_val():
    try:
        with open(storage_path) as f:
            data = json.loads(f.read())
            for v in data.values():
                if args.key in data.keys():
                    return v
                else:
                    return 'add to old'
    except:
        return 'creat new'


if args.val:
    value = have_val()
    if value == 'creat new':
        with open(storage_path, 'w') as f:
            json.dump({args.key:[args.val]}, f)
    elif value == 'add to old':
        with open(storage_path) as f:
            data = json.load(f)
        data.update({args.key : [args.val]})
        with open(storage_path, 'w') as f:
            json.dump(data, f)
    elif value:
        with open(storage_path) as f:
            data = json.load(f)
            value.append(args.val)
        data.update({args.key : value})
        with open(storage_path, 'w') as f:
            json.dump(data, f)
else:
    result = have_val()
    if result == 'add to old':
        print(None)
    elif result == 'creat new':
        print(None)
    elif result:
        with open(storage_path) as f:
            inf = json.load(f)
            for k, v in inf.items():
                if k == args.key:
                    print(', '.join(v))
    else:
        print(None)
