#
# 集合クラス
#
import random

class Population:
    """
    治具同士の距離に対する重みを管理する
    ex) row_num(治具種類数) = 6
    
    __|  1  |  2  |  3  |  4  |  5  |  6  |
    ---------------------------------------
    1 | 0.1 | 0.4 | 0.3 | 0.1 | 0.7 | 0.3 |
    ---------------------------------------
    2 |  x  | 5.1 | 2.7 | 0.2 | 0.2 | 1.1 |
    ---------------------------------------
    3 |  x  |  x  | 0.4 | 0.3 | 1.8 | 2.6 |
    ---------------------------------------
    4 |  x  |  x  |  x  | 1.1 | 2.0 | 3.2 |
    ---------------------------------------
    5 |  x  |  x  |  x  |  x  | 0.0 | 1.3 |
    ---------------------------------------
    6 |  x  |  x  |  x  |  x  |  x  | 0.3 |
    """
    _row_num = -1
    _population = {}
    def _create_key(self, xi, yi):
        """key生成

        Args:
            x (int): 横インデックス
            y (int): 縦インデックス

        Returns:
            str: 辞書型のキー 
        """
        return str(yi + 1) + 'x' + str(xi + 1)
    def _get_pop_item(self, xi, yi):
        """_populationから指定のアイテム取得

        Args:
            x (int): 横インデックス
            y (int): 縦インデックス

        Returns:
            float: 重み
        """
        cx, cy = (xi, yi) if xi < yi else (yi, xi)
        key = self._create_key(cx, cy)
        return self._population[key]
    def __init__(self, row_num):
        """初期化

        Args:
            row_num (int): 治具種類数
        """
        self._row_num = row_num
        for yi in range(self._row_num):
            for xi in range(self._row_num):
                if yi > xi:
                    continue
                
                key = self._create_key(xi, yi)
                self._population[key] = random.random()
    def centralization(self):
        """一次元配列化

        Returns:
            int[]: 距離への重みの一次元配列
        """
        result = []
        for yi in range(self._row_num):
            for xi in range(self._row_num):
                if yi > xi:
                    continue
                key = self._create_key(xi, yi)
                result.append(self._population[key])
        return result
# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_population_len(self):
            """集合を生成し、一元配列としてサイズが間違いないかテスト
            """
            pop = Population(6)
            arr = pop.centralization()
            print(arr)
            self.assertTrue(len(arr) == 21)
    unittest.main()