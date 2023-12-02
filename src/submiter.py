#
# 解提出管理
#
import sys
from util import logger

SOLVE_SINGLE_ID = 's' # 単目的
SOLVE_MULTI_ID  = 'm' # 多目的

# 実際の提出時に使用する問題指定用番号
MATCH_NUM = {
    f"{SOLVE_SINGLE_ID}0": 93, # https://ec-comp.jpnsec.org/ja/matches/93
    f"{SOLVE_SINGLE_ID}1": 94, # https://ec-comp.jpnsec.org/ja/matches/94
    f"{SOLVE_SINGLE_ID}2": 95, # https://ec-comp.jpnsec.org/ja/matches/95
    f"{SOLVE_MULTI_ID}0" : 96, # https://ec-comp.jpnsec.org/ja/matches/96
    f"{SOLVE_MULTI_ID}1" : 97, # https://ec-comp.jpnsec.org/ja/matches/97
}

def get_match_num(dep, num):
    """問題指定用番号を取得

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    """
    key = f"{dep}{num}"
    if key in MATCH_NUM:
        match_num = MATCH_NUM[f"{dep}{num}"]
    else:
        logger.error(f"問題のID`{dep}{num}`は存在しない")
        sys.exit(1)
    return match_num

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
            match_num = get_match_num('s', 1)
            self.assertTrue(match_num == 94)
            
        def test_get_match_num_error(self):
            logger.init()
            with self.assertRaises(SystemExit):
                get_match_num('n', 1)
        
    unittest.main()