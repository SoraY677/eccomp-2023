#
# ソルバ共通の関数定義
#
import sys
from util import logger
from util import path_util
from util import tsv_operator

def _read_premise_tsv(path_template, dep, num):
    """前提情報読み出しの共通関数

    Args:
        path_template (string): パスの文字列テンプレート
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        list: 読み込んだ配列
    """
    path = path_template.format(str(dep), str(num))
    content = tsv_operator.read(path)
    if type(content) is not list:
        logger.error(content)
        sys.exit(1)
    return content

def read_palette(dep, num):
    """ワークの前提条件読み出し

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    Returns:
        dict: パレット情報の辞書型
    """
    return _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/palette.tsv"], dep, num)
    
def read_work(dep, num):
    """ワークの前提条件読み出し

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    Returns:
        dict: ワーク情報の辞書型
    """
    return _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/work.tsv"], dep, num)

def read_jig(dep, num):
    """治具の前提条件読み出し

    Args:
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        dict: 治具情報の辞書型
    """
    return _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/jig.tsv"], dep, num)
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    def _init():
        path_util.init(".")
        logger.init()

    class Test(unittest.TestCase):
        def test_read_palette(self):
            _init()
            result = read_palette('s', 2)
            self.assertTrue(result == [['1', '1000'], ['2', '3000'], ['3', '3000'], ['4', '4000'], ['5', '4000'], ['6', '5000'], ['7', '5000'], ['8', '6000'], ['9', '6000'], ['10', '6000'], ['11', '8000'], ['12', '8000']])
        def test_read_work(self):
            _init()
            result = read_work('s', 2)
            self.assertTrue(result == [['1', '1', '12', '78', '2', '9000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '5'], ['2', '2', '14', '150', '13', '2000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '5'], ['3', '3', '15', '72', '15', '9000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '3'], ['4', '4', '15', '90', '15', '8000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '5'], ['5', '4', '15', '90', '15', '8000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '5'], ['6', '5', '15', '36', '15', '5000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '2'], ['7', '5', '15', '36', '15', '5000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '2'], ['8', '6', '22', '117', '22', '10000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '4'], ['9', '6', '22', '117', '22', '10000', '-', '-', '-', '-', '-', '-', '-', '-', '1', '4'], ['10', '7', '15', '60', '15', '3000', '15', '60', '15', '5000', '-', '-', '-', '-', '1', '5'], ['11', '8', '15', '144', '15', '4000', '14', '48', '14', '6000', '-', '-', '-', '-', '1', '5'], ['12', '9', '10', '34', '10', '3000', '12', '40', '12', '6000', '-', '-', '-', '-', '2', '5'], ['13', '9', '10', '34', '10', '3000', '12', '40', '12', '6000', '-', '-', '-', '-', '2', '5'], ['14', '10', '14', '108', '14', '8000', '15', '96', '15', '7000', '15', '114', '15', '2000', '2', '6'], ['15', '11', '12', '108', '12', '8000', '7', '96', '7', '6000', '10', '144', '10', '2000', '1', '5']])
        def test_read_jig(self):
            _init()
            result = read_jig('s', 2)
            self.assertTrue(result == [['1000', '1'], ['2000', '2'], ['3000', '3'], ['4000', '3'], ['5000', '2'], ['6000', '4'], ['7000', '1'], ['8000', '3'], ['9000', '2'], ['10000', '1']])
    unittest.main()