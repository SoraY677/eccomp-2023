import os.path as path

PATH_MAP = {
    "data": "",
    "data/app-log": "",
}

def init(rootpath):
    '''
    初期化
    '''
    for path_key in PATH_MAP:
        PATH_MAP[path_key] = path.join(rootpath, path_key)

