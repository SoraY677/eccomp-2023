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
        {
            [palette_id: string]: {
                'jig_id': string
            }
        }
    """
    origin_content = _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/palette.tsv"], dep, num)
    result_dict = {}
    for item in origin_content:
        result_dict_item = {
            "jig_id": item[1]
        }
        result_dict[item[0]] = result_dict_item
    return result_dict
    
def read_work(dep, num):
    """ワークの前提条件読み出し

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    Returns:
        dict: ワーク情報の辞書型
        {
            [work_id: string]: {
                work_product_number: int,
                procedure: [
                    {
                        installation_time: int
                        processing_time: int,
                        removal_time: int,
                        jig_id: string
                    },...
                ],
                available_time: int,
                deadline_time: int
            }
        }
    """
    origin_content = _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/work.tsv"], dep, num)
    
    precedure_count = int((len(origin_content[0]) - 4) / 4)
    
    result_dict = {}
    for item in origin_content:
        result_dict_item = {
            "work_product_number": int(item[1]),
            "procedure": [],
            "available_time": int(item[-2]),
            "deadline_time": int(item[-1])
        }
        for i in range(precedure_count):
            current_start_index = 2 + i * 4
            if(item[current_start_index + 3] == '-'):
                break
            
            procedure_item = {
                "installation_time": item[current_start_index],
                "processing_time": item[current_start_index + 1],
                "removal_time": item[current_start_index + 2],
                "jig_id": item[current_start_index + 3]
            }
            result_dict_item["procedure"].append(procedure_item)
        result_dict[item[0]] = result_dict_item
    return result_dict

def read_jig(dep, num):
    """治具の前提条件読み出し

    Args:
        dep (string): 問題部門
        num (int): 問題番号

    Returns:
        dict: 治具情報の辞書型
        {
            [palette_id: string]: {
                'num': int
            }
        }
    """
    origin_content =  _read_premise_tsv(path_util.PATH_MAP["data/premise/{}/{}/jig.tsv"], dep, num)
    result_dict = {}
    for item in origin_content:
        result_dict_item = {
            "num": int(item[1])
        }
        result_dict[item[0]] = result_dict_item
    return result_dict
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
            self.assertTrue(result == {'1': {'jig_id': '1000'}, '2': {'jig_id': '3000'}, '3': {'jig_id': '3000'}, '4': {'jig_id': '4000'}, '5': {'jig_id': '4000'}, '6': {'jig_id': '5000'}, '7': {'jig_id': '5000'}, '8': {'jig_id': '6000'}, '9': {'jig_id': '6000'}, '10': {'jig_id': '6000'}, '11': {'jig_id': '8000'}, '12': {'jig_id': '8000'}})
        def test_read_work(self):
            _init()
            result = read_work('s', 2)
            self.assertTrue(result == {'1': {'work_product_number': 1, 'procedure': [{'installation_time': '12', 'processing_time': '78', 'removal_time': '2', 'jig_id': '9000'}], 'available_time': 1, 'deadline_time': 5}, '2': {'work_product_number': 2, 'procedure': [{'installation_time': '14', 'processing_time': '150', 'removal_time': '13', 'jig_id': '2000'}], 'available_time': 1, 'deadline_time': 5}, '3': {'work_product_number': 3, 'procedure': [{'installation_time': '15', 'processing_time': '72', 'removal_time': '15', 'jig_id': '9000'}], 'available_time': 1, 'deadline_time': 3}, '4': {'work_product_number': 4, 'procedure': [{'installation_time': '15', 'processing_time': '90', 'removal_time': '15', 'jig_id': '8000'}], 'available_time': 1, 'deadline_time': 5}, '5': {'work_product_number': 4, 'procedure': [{'installation_time': '15', 'processing_time': '90', 'removal_time': '15', 'jig_id': '8000'}], 'available_time': 1, 'deadline_time': 5}, '6': {'work_product_number': 5, 'procedure': [{'installation_time': '15', 'processing_time': '36', 'removal_time': '15', 'jig_id': '5000'}], 'available_time': 1, 'deadline_time': 2}, '7': {'work_product_number': 5, 'procedure': [{'installation_time': '15', 'processing_time': '36', 'removal_time': '15', 'jig_id': '5000'}], 'available_time': 1, 'deadline_time': 2}, '8': {'work_product_number': 6, 'procedure': [{'installation_time': '22', 'processing_time': '117', 'removal_time': '22', 'jig_id': '10000'}], 'available_time': 1, 'deadline_time': 4}, '9': {'work_product_number': 6, 'procedure': [{'installation_time': '22', 'processing_time': '117', 'removal_time': '22', 'jig_id': '10000'}], 'available_time': 1, 'deadline_time': 4}, '10': {'work_product_number': 7, 'procedure': [{'installation_time': '15', 'processing_time': '60', 'removal_time': '15', 'jig_id': '3000'}, {'installation_time': '15', 'processing_time': '60', 'removal_time': '15', 'jig_id': '5000'}], 'available_time': 1, 'deadline_time': 5}, '11': {'work_product_number': 8, 'procedure': [{'installation_time': '15', 'processing_time': '144', 'removal_time': '15', 'jig_id': '4000'}, {'installation_time': '14', 'processing_time': '48', 'removal_time': '14', 'jig_id': '6000'}], 'available_time': 1, 'deadline_time': 5}, '12': {'work_product_number': 9, 'procedure': [{'installation_time': '10', 'processing_time': '34', 'removal_time': '10', 'jig_id': '3000'}, {'installation_time': '12', 'processing_time': '40', 'removal_time': '12', 'jig_id': '6000'}], 'available_time': 2, 'deadline_time': 5}, '13': {'work_product_number': 9, 'procedure': [{'installation_time': '10', 'processing_time': '34', 'removal_time': '10', 'jig_id': '3000'}, {'installation_time': '12', 'processing_time': '40', 'removal_time': '12', 'jig_id': '6000'}], 'available_time': 2, 'deadline_time': 5}, '14': {'work_product_number': 10, 'procedure': [{'installation_time': '14', 'processing_time': '108', 'removal_time': '14', 'jig_id': '8000'}, {'installation_time': '15', 'processing_time': '96', 'removal_time': '15', 'jig_id': '7000'}, {'installation_time': '15', 'processing_time': '114', 'removal_time': '15', 'jig_id': '2000'}], 'available_time': 2, 'deadline_time': 6}, '15': {'work_product_number': 11, 'procedure': [{'installation_time': '12', 'processing_time': '108', 'removal_time': '12', 'jig_id': '8000'}, {'installation_time': '7', 'processing_time': '96', 'removal_time': '7', 'jig_id': '6000'}, {'installation_time': '10', 'processing_time': '144', 'removal_time': '10', 'jig_id': '2000'}], 'available_time': 1, 'deadline_time': 5}})
        def test_read_jig(self):
            _init()
            result = read_jig('s', 2)
            self.assertTrue(result == {'1000': {'num': 1}, '2000': {'num': 2}, '3000': {'num': 3}, '4000': {'num': 3}, '5000': {'num': 2}, '6000': {'num': 4}, '7000': {'num': 1}, '8000': {'num': 3}, '9000': {'num': 2}, '10000': {'num': 1}})
    unittest.main()