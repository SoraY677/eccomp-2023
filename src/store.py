#
# 結果のファイル入出力
#
import os
import os.path as path
import datetime
import glob
from os import path
import sys
sys.path.append(path.dirname(__file__))
from util import json_operator
from util import path_util
from util import logger
from solution.cluster import Cluster
from solution.individual import Individual

STATE_KEY = 'state'
COUNT_KEY = "count"
CLUSTER_KEY = "cluster"
WEIGHT_CLUSTER_KEY = "weight_cluster"
SELECTED_INDIVIDUAL_LIST_KEY = "selected_individual_list"
INDIVIDUAL_LIST_KEY = "individual_list"
EVALUATION_LIST = "evaluation_list"

def load(dep, num):
    """読み込み

    Args:
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        dict|None: ファイル内容|なければNone
    """
    dirpath = path.join(path_util.PATH_MAP["data/result"], f"{dep}{num}")
    file_list = sorted(glob.glob(dirpath + '\*'), reverse=True)
    if len(file_list) == 0:
        return None
    content = json_operator.read(file_list[0])
    if len(file_list) < 0 or type(content) is not dict:
        return None
    return _deserialize(content)

def _deserialize(content):
    """デシリアライズ

    Args:
        content (dict): デシリアライズ対象

    Returns:
        dict: デシリアライズ後のデータ
    """
    return {
        STATE_KEY: content[STATE_KEY],
        COUNT_KEY: content[COUNT_KEY],
        CLUSTER_KEY: Cluster.deserialize(content[CLUSTER_KEY]),
        INDIVIDUAL_LIST_KEY: [Individual.deserialize(individual_json) for individual_json in content[INDIVIDUAL_LIST_KEY]],
        SELECTED_INDIVIDUAL_LIST_KEY: [Individual.deserialize(individual_json) for individual_json in content[SELECTED_INDIVIDUAL_LIST_KEY]],
        EVALUATION_LIST: content[EVALUATION_LIST]
    }

def save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list):
    """保存

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        state(int): 状態変数
        count (int): 現在の回数
        cluster (Cluster): 個体群のクラスター
        individual_list (list): 生成した個体群
        selected_individual_list (list): 選択された個体群
        evaluation_list(list): 評価リスト
    Returns:
        str: ファイルパス
    """
    dirpath = path.join(path_util.PATH_MAP["data/result"], f"{dep}{num}")
    if path.isdir(dirpath) is False:
        os.mkdir(dirpath)
    filepath = path.join(dirpath, f"r{dep}{num}-{str(count).zfill(10)}-{state}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    
    data = _serialize(state, count, cluster, individual_list, selected_individual_list, evaluation_list)
    error = json_operator.write(filepath, data)
    if error is not None:
        logger.error(error)
        sys.exit(1)
    return filepath

def _serialize(state, count, cluster, individual_list, selected_individual_list, evaluation_list):
    """シリアライズ

    Args:
        state(int): 状態変数
        count (int): 現在の回数
        cluster (Cluster): 個体群のクラスター
        individual_list (list): 生成した個体群
        selected_individual_list (list): 選択された個体群
        evaluation_list(list): 評価リスト

    Returns:
        dict: シリアライズ後のデータ
    """
    return {
        STATE_KEY: state,
        COUNT_KEY: count,
        CLUSTER_KEY: cluster.serialize(),
        INDIVIDUAL_LIST_KEY: [individual.serialize() for individual in individual_list],
        SELECTED_INDIVIDUAL_LIST_KEY: [individual.serialize() for individual in selected_individual_list],
        EVALUATION_LIST: evaluation_list
    }

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
                "count": 10,
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
            filepath = save("s", 1, 1, c)
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
                "count": 10,
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
            save("s", 1, 1, c)
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
                "count": 10,
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
            save("s", 1, 1, c)
            save("s", 1, 2, c)
            list = get_result_file_path_list_order_by_count_desc("s", 1)
            for i in range(len(list)-1):
                self.assertTrue(list[i] > list[i+1])
            test_end()
        def test_get_latest_result(self):
            """最新1件目取得成功
            """
            test_start()
            c = {
                "count": 10,
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
            save("s", 1, 1, c)
            result = get_latest_result("s", 1, 0)
            self.assertTrue(result is not {})
            test_end()
        def test_get_latest_second_result(self):
            """最新2件目取得失敗
            """
            test_start()
            c = {
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
            save("s", 1, 1, c)
            result = get_latest_result("s", 1, 1)
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