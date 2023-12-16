
#
# 進化
# 手法: GA
# - https://ja.wikipedia.org/wiki/%E9%81%BA%E4%BC%9D%E7%9A%84%E3%82%A2%E3%83%AB%E3%82%B4%E3%83%AA%E3%82%BA%E3%83%A0
#
import random
from os import path
import sys
sys.path.append(path.dirname(__file__))
from individual import Individual
from constraints import CROSSOVER_POINT_MAX

def crossover(schedule1, schedule2, ban_generation_list = [], crossover_point_max = CROSSOVER_POINT_MAX):
    """交叉

    Args:
        individual1 (Individual): 個体1
        individual2 (Individual): 個体2
        ban_generation_list (list, optional): 生成禁止リスト. Defaults to [].
        crossover_point_max (int, optional): 交叉点最大数. Defaults to CROSSOVER_POINT_MAX.

    Returns:
        _type_: _description_
    """
    parent_num = random.randint(1,2)
    parent_schedule = schedule1 if parent_num == 1 else schedule2
    child_schedule = schedule2 if parent_num == 1 else schedule1

    result = []
    crossover_point = set([random.randint(0, len(parent_schedule) - 1) for _ in range(crossover_point_max)])
    is_parent = True
    for i in range(len(parent_schedule)):
        if is_parent:
            result.append(parent_schedule[i])
        else:
            result.append(child_schedule[i])
        
        if i+1 in crossover_point:
            is_parent = not is_parent

    return Individual(schedule_list=result, ban_generation_list=ban_generation_list)

def mutate(work_num):
    """突然変異

    Args:
        work_num (int): ワーク数

    Returns:
        Individual: 個体
    """
    return Individual(work_num=work_num)
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_crossover(self):
            new_individual = crossover(Individual(work_num=10), Individual(work_num=10))
            self.assertTrue(len(new_individual.get_schedule()) == 20)
        def test_mutate(self):
            new_individual = mutate(10)
            self.assertTrue(len(new_individual.get_schedule()) == 20)
    unittest.main()