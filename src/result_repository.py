#
# 結果のファイル入出力
#
import os
import os.path as path
import datetime
from util import json_operator
from util import filepath
from util import logger

def save(dep, num, count, ans, result):
    dirpath = path.join(filepath.PATH_MAP["data/result"], f"{dep}{num}")
    if path.isdir(dirpath) is False:
        os.mkdir(dirpath)
    
    file = path.join(dirpath, f"r{dep}{num}-{str(count).zfill(10)}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    json_operator.write(file, {
        "conut": count,
        "ans": ans,
        "result": result
    })

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_save(self):
            c = {
                "dep": "s",
                "num": 1,
                "count": 1,
                "ans":  {
                    "schedule": [1, 1, 2, 3, 2, 2],
                    "timeout": 600
                }, 
                "result": {
                    "objective": 1550.5,
                    "constraint": None,
                    "error": "エラー文",
                    "info": {
                        "exe_time": 503.223,
                        "delays": [0.0, 0.0, 30.5, 14.5]
                    }
                }
            }
            filepath.init("..")
            logger.init()
            save(c["dep"], c["num"], c["count"], c["ans"], c["result"])

    unittest.main()