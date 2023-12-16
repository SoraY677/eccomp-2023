#
# ファイル・ディレクトリの管理
#
import json

def read(filepath):
    """読み込み

    Args:
        filepath (string): ファイルパス

    Returns:
        dict|Exception: 読み込んだJSON|読み込み失敗時Exception
    """
    result = None
    try:
        with open(filepath) as f:
            result = json.load(f)
    except Exception as e:
        return e
    return result

def write(filepath, content):
    """書き込み

    Args:
        filepath (string): ファイルパス
        content (dict): 書き込み内容
        
    Returns:
        Exception|None: 書き込みの成否(成:None|否:Exception)
    """
    json_content = json.dumps(content)
    try:
        with open(filepath, 'w') as f:
            f.write(json_content)
        return None
    except Exception as e:
        return e

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    import os
    class Test(unittest.TestCase):
        
        def test_write(self):
            """書き込みテスト
            """
            content = {
                "test": "てすとだよ～",
                "testarr": [
                    1,2,3
                ]
            }
            filepath = "data/test.json"
            write(filepath, content)
            self.assertTrue(os.path.isfile(filepath))
        
        def test_read(self):
            """読み込みテスト
            """
            writtenContent = {
                "test": "test",
                "testarr": [
                    1,2,3
                ]
            }
            filepath = "data/test2.json"
            err = write(filepath, writtenContent)
            readContent = read(filepath)
            self.assertTrue(writtenContent == readContent)
            self.assertTrue(err is None)

    unittest.main()