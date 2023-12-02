#
# ファイル・ディレクトリの管理
#
import json
import sys
import logger

def read(filepath):
    """読み込み

    Args:
        filepath (string): ファイルパス

    Returns:
        map: 読み込んだJSON
    """
    result = None
    try:
        with open(filepath) as f:
            result = json.load(f)
    except Exception as e:
        logger.error(e)
        sys.exit(1)
    return result

def write(filepath, content):
    """書き込み

    Args:
        filepath (string): ファイルパス
        content (map): 書き込み内容
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(content, f, indent=2)
    except Exception as e:
        logger.error(e)
        sys.exit(1)

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    import os
    class LoggerTest(unittest.TestCase):
        
        def test_write(self):
            """書き込みテスト
            """
            content = {
                "test": "てすとだよ～",
                "testarr": [
                    1,2,3
                ]
            }
            filepath = "../../data/test.json"
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
            filepath = "../../data/test2.json"
            write(filepath, writtenContent)
            logger.init()
            readContent = read(filepath)
            self.assertTrue(writtenContent == readContent)

    unittest.main()