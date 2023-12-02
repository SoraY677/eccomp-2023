#
# 解提出管理
#
import sys
from util import logger

SOLVE_SINGLE_ID = 's' # 単目的
SOLVE_MULTI_ID  = 'm' # 多目的

QUESTION_MAP = {
    ### 単目的
    # https://ec-comp.jpnsec.org/ja/matches/93
    f"{SOLVE_SINGLE_ID}0": {
        "match_num": 93,
        "submit_max": 10000
    },
    # https://ec-comp.jpnsec.org/ja/matches/94
    f"{SOLVE_SINGLE_ID}1": {
        "match_num": 94,
        "submit_max": 1000
    },
    # https://ec-comp.jpnsec.org/ja/matches/95
    f"{SOLVE_SINGLE_ID}2": {
        "match_num": 95,
        "submit_max": 1000
    },
    ### 多目的
    # https://ec-comp.jpnsec.org/ja/matches/96
    f"{SOLVE_MULTI_ID}0": {
        "match_num": 96,
        "submit_max": 10000
    },
    # https://ec-comp.jpnsec.org/ja/matches/97
    f"{SOLVE_MULTI_ID}1": {
        "match_num": 97,
        "submit_max": 1000
    }
}

def get_match_num(dep, num):
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

def submit(dep, num, ans):
    """解提出

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        ans (any): 解
    """
    # Todo: 解答提出スクリプト
    pass

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_get_match_num(self):
            """問題指定用番号の取得
            """
            match_num = get_match_num('s', 1)
            self.assertTrue(match_num == 94)
            
        def test_get_match_num_error(self):
            """問題指定用番号のミス
            """
            logger.init()
            with self.assertRaises(SystemExit):
                get_match_num('n', 1)
                
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
        
    unittest.main()