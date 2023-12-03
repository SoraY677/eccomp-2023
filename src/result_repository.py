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

def load(filepath):
    """読み込み

    Args:
        filepath (string): ファイルパス

    Returns:
        dict: ファイル内容
    """
    content = json_operator.read(filepath)
    if type(content) is not dict:
        logger.error(content)
        sys.exit(1)
        
    return content

def save(dep, num, count, ans, response):
    """保存

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        count (int): 解提出回数
        ans (dict): 解提出形式のマップ
        response (dict): 提出結果のマップ
    """
    dirpath = path.join(path_util.PATH_MAP["data/result"], f"{dep}{num}")
    if path.isdir(dirpath) is False:
        os.mkdir(dirpath)
    
    
    file = path.join(dirpath, f"r{dep}{num}-{str(count).zfill(10)}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    error = json_operator.write(file, {
        "conut": count,
        "ans": ans,
        "response": response
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

def get_latest_result(dep, num, index):
    """最新{index}件目のリザルト取得

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        index (int): 上から何番目か
    Returns:
        dict: 存在すればその内容が含まれたdict|なければカラのdict
    """
    result_filepath_list = get_result_file_path_list_order_by_count_desc(dep, num)
    if len(result_filepath_list) < index + 1:
        return {}
    return load(result_filepath_list[index])
# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    import time
    def test_start():
        path_util.init(".")
        logger.init()
        filelist = glob.glob(os.path.join("data/result/s1", "*"))
        for f in filelist:
            os.remove(f)
    def test_end():
        filelist = glob.glob(os.path.join("data/result/s1", "*"))
        for f in filelist:
            os.remove(f)
        time.sleep(1)
    class Test(unittest.TestCase):
        def test_load(self):
            test_start()
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
            filepath = save(c["dep"], c["num"], c["count"], c["ans"], c["result"])
            load(filepath)
            test_end()
        def test_load_error(self):
            test_start()
            with self.assertRaises(SystemExit):
                load("hogehoge")
            test_end()
        def test_save(self):
            """保存のテスト
            """
            test_start()
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
            save(c["dep"], c["num"], c["count"], c["ans"], c["result"])
            test_end()
        def test_result_file_path_list_order_by_count_desc_empty(self):
            """ファイル一覧降順がカラの場合
            """
            test_start()
            list = get_result_file_path_list_order_by_count_desc('s', 1)
            self.assertTrue(len(list) == 0)
            test_end()
        def test_result_file_path_list_order_by_count_desc(self):
            """一覧ソートのテスト
            """
            test_start()
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
            save(c["dep"], c["num"], 1, c["ans"], c["result"])
            save(c["dep"], c["num"], 2, c["ans"], c["result"])
            list = get_result_file_path_list_order_by_count_desc(c["dep"], c["num"])
            for i in range(len(list)-1):
                self.assertTrue(list[i] > list[i+1])
            test_end()
        def test_get_latest_result(self):
            """最新1件目取得成功
            """
            test_start()
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
            save(c["dep"], c["num"], c["count"], c["ans"], c["result"])
            result = get_latest_result(c["dep"], c["num"], 0)
            self.assertTrue(result is not {})
            test_end()
        def test_get_latest_second_result(self):
            """最新2件目取得失敗
            """
            test_start()
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
            save(c["dep"], c["num"], c["count"], c["ans"], c["result"])
            result = get_latest_result(c["dep"], c["num"], 1)
            self.assertTrue(any(result) is False)
            test_end()
        def test_get_latest_result_empty(self):
            """最新1件目取得失敗（カラ）
            """
            test_start()
            result = get_latest_result("s", "1", 0)
            self.assertTrue(any(result) is False)
            test_end()
    unittest.main()