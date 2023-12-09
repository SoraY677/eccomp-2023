def read(filepath):
    """読み込み

    Args:
        filepath (string): ファイルパス

    Returns:
        list|Exception: 読み込んだList|読み込み失敗時Exception
    """
    try:
        with open(filepath, encoding='utf-8') as f:
            result = []
            for line in f:
                result.append([x.strip() for x in line.split('\t')])
            return result
    except Exception as e:
        return e
# 
# 単体テスト
#
if __name__ == "__main__":
    filepath = "data/test/test.tsv"
    readContent = read(filepath)
    import unittest
    class Test(unittest.TestCase):
        def test_read(self):
            """読み込みテスト
            """
            filepath = "data/test/test.tsv"
            readContent = read(filepath)
            self.assertTrue(readContent == [['1', 'hoge'], ['2', 'fuga']])

    unittest.main()