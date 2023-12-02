#
# ファイル・ディレクトリパスの管理
#
import os.path as path

PATH_MAP = {
    "data": "",
    "data/app-log": "",
    "data/result": "",
}

def init(rootpath):
    """初期化

    Args:
        rootpath (string): プロジェクトのルートパス
    """
    for path_key in PATH_MAP:
        PATH_MAP[path_key] = path.join(rootpath, path_key)


