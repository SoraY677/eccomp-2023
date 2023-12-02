#
# 結果のファイル入出力
#
import os
import os.path as path
import datetime
import glob
import sys
from util import json_operator
from util import path_util
from util import logger

# def load (filepath):
    

def save(dep, num, count, ans, result):
    """保存

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        count (int): 解提出回数
        ans (map): 解提出形式のマップ
        result (map): 提出結果のマップ
    """
    dirpath = path.join(path_util.PATH_MAP["data/result"], f"{dep}{num}")
    if path.isdir(dirpath) is False:
        os.mkdir(dirpath)
    
    
    file = path.join(dirpath, f"r{dep}{num}-{str(count).zfill(10)}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    error = json_operator.write(file, {
        "conut": count,
        "ans": ans,
        "result": result
    })
    if error is not None:
        logger.error(error)
        sys.exit(1)
    return file

def get_result_file_path_list_order_by_count_desc(dep, num):
    """保存している結果一覧のリストを降順で取得する

    Args:
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        [string]: 降順に並んだ保存している結果一覧
    """
    filepath_list = glob.glob(path.join(path_util.PATH_MAP["data/result"], f"{dep}{num}", '*'))
    filepath_list.sort(reverse=True)
    return filepath_list

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_save(self):
            """保存のテスト
            """
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
            path_util.init("..")
            logger.init()
            save(c["dep"], c["num"], c["count"], c["ans"], c["result"])
        def test_result_file_path_list_order_by_count_desc_empty(self):
            path_util.init("..")
            logger.init()
            filelist = glob.glob(os.path.join("../data/result/s1", "*"))
            for f in filelist:
                os.remove(f)
            list = get_result_file_path_list_order_by_count_desc('s', 1)
            self.assertTrue(len(list) == 0)
        def test_result_file_path_list_order_by_count_desc(self):
            """一覧ソートのテスト
            """
            c = {
                "dep": "s",
                "num": 1,
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
            path_util.init("..")
            logger.init()
            save(c["dep"], c["num"], 1, c["ans"], c["result"])
            save(c["dep"], c["num"], 2, c["ans"], c["result"])
            list = get_result_file_path_list_order_by_count_desc(c["dep"], c["num"])
            for i in range(len(list)-1):
                self.assertTrue(list[i] > list[i+1])

    unittest.main()