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
