from util import filepath
from util import logger

def init(rootpath):
    filepath.init(rootpath)
    logger.init(filepath.PATH_MAP["data/app-log"])
    
def run(dep, num):
    # Todo: 処理を追記
    pass

# 
# 単体テスト
#
if __name__ == "__main__":
    import os
    import unittest
    class LoggerTest(unittest.TestCase):
        def test_init(self):
            rootpath = os.path.join(os.getcwd(),'..')
            init(rootpath)
    unittest.main()