#
# 解提出管理
#
import sys
import subprocess
import json
from util import logger

SOLVE_SINGLE_ID = 's' # 単目的
SOLVE_MULTI_ID  = 'm' # 多目的

QUESTION_MAP = {
    ### 単目的
    # https://ec-comp.jpnsec.org/ja/matches/93
    f"{SOLVE_SINGLE_ID}0": {
        "match_num": 93,
        "submit_max": 10000,
        "work_num": 8
    },
    # https://ec-comp.jpnsec.org/ja/matches/94
    f"{SOLVE_SINGLE_ID}1": {
        "match_num": 94,
        "submit_max": 1000,
        "work_num": 20
    },
    # https://ec-comp.jpnsec.org/ja/matches/95
    f"{SOLVE_SINGLE_ID}2": {
        "match_num": 95,
        "submit_max": 1000,
        "work_num": 23
    },
    ### 多目的
    # https://ec-comp.jpnsec.org/ja/matches/96
    f"{SOLVE_MULTI_ID}0": {
        "match_num": 96,
        "submit_max": 10000,
        "work_num": 8
    },
    # https://ec-comp.jpnsec.org/ja/matches/97
    f"{SOLVE_MULTI_ID}1": {
        "match_num": 97,
        "submit_max": 1000,
        "work_num": 20
    }
}

TIMEOUT = 3000

def _get_match_num(dep, num):
    """問題指定用番号を取得

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    Returns:
        int: 問題指定用番号
    """
    key = f"{dep}{num}"
    if key in QUESTION_MAP:
        match_num = QUESTION_MAP[f"{dep}{num}"]["match_num"]
    else:
        logger.error(f"問題のID`{dep}{num}`は存在しない")
        sys.exit(1)
    return match_num

def get_submit_max(dep, num):
    """提出回数を取得

    Args:
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        int: 提出回数
    """
    key = f"{dep}{num}"
    if key in QUESTION_MAP:
        submit_max = QUESTION_MAP[f"{dep}{num}"]["submit_max"]
    else:
        logger.error(f"問題のID`{dep}{num}`は存在しない")
        sys.exit(1)
    return submit_max

def get_work_num(dep, num):
    key = f"{dep}{num}"
    if key in QUESTION_MAP:
        work_num = QUESTION_MAP[f"{dep}{num}"]["work_num"]
    else:
        logger.error(f"問題のID`{dep}{num}`は存在しない")
        sys.exit(1)
    return work_num

def _decode_response(response_txt):
    """レスポンスのデコード

    Args:
        response_txt (string): レスポンス内容文字列 

    Returns:
        dict: レスポンス内容の辞書型
    """
    decoded_response = json.loads(response_txt)
    logger.info(f'レスポンス: {decoded_response}')
    return decoded_response

def _exec_submit_command(dep, num, ans):
    """実行コマンド

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        ans (dict): 解答

    Returns:
        dict: 成功:レスポンス|失敗:カラ辞書型配列
    """
    match_num = _get_match_num(dep, num)
    
    command = f'echo \'{ans}\' | opt submit --match={match_num}'
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    try:
        response = _decode_response(proc.communicate()[0])
    except Exception as e:
        logger.warn(e)
        response = {}

    return response

def create_ans(dep, schedule, weights=None, timeout=TIMEOUT):
    ans = {
        "schedule": schedule,
        "timeout": timeout
    }
    if dep == SOLVE_MULTI_ID:
        ans[weights] = weights
    
    return ans

def submit(dep, num, ans):
    """解提出

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        ans (any): 解
    """
    # Todo:テストできていないので、テストコードなど修正
    return _exec_submit_command(dep, num, ans)

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_get_match_num(self):
            """問題指定用番号の取得
            """
            match_num = _get_match_num('s', 1)
            self.assertTrue(match_num == 94)
            
        def test_get_match_num_error(self):
            """問題指定用番号のミス
            """
            logger.init()
            with self.assertRaises(SystemExit):
                _get_match_num('n', 1)
                
        def test_get_submit_max(self):
            """提出回数の取得
            """
            submit_max = get_submit_max('s', 1)
            self.assertTrue(submit_max == 1000)
            
        def test_get_submit_max_error(self):
            """問題指定用番号のミス
            """
            logger.init()
            with self.assertRaises(SystemExit):
                get_submit_max('n', 1)

        def test_get_work_num(self):
            """ワーク番号の取得
            """
            work_num = get_work_num('s', 1)
            self.assertTrue(work_num == 20)
        def test_get_work_num_error(self):
            """問題指定用番号のミス
            """
            logger.init()
            with self.assertRaises(SystemExit):
                get_work_num('n', 1)

    unittest.main()