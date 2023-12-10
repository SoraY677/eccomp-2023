#
# 集合
#
from individual import Individual
from constraints import INITIALIZE_INDIVIDUAL_MAX_DEFAULT

class Population:
    _individual_list: []
    def __init__(self, work_num, individual_max = INITIALIZE_INDIVIDUAL_MAX_DEFAULT):
        """初期化

        Args:
            work_num (int): ワーク数
            individual_max (int, optional): 個体数. Defaults to INITIALIZE_INDIVIDUAL_MAX_DEFAULT.
        """
        self._individual_list = self._create(work_num, individual_max)
        

    def _create(self, work_num, individual_max):
        """生成

        Returns:
            list: 個体群のリスト
        """
        return [Individual(work_num) for _ in range(individual_max)]
    
    def get_individual_list(self):
        """個体群のリスト取得

        Returns:
            list: 個体群のリスト 
        """
        return self._individual_list

# 
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_get_individual_list(self):
            individual_max = 10
            population = Population(10, individual_max)
            individual_list = population.get_individual_list()
            self.assertTrue(len(individual_list) == individual_max)

    unittest.main()