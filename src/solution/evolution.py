
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

def crossover(parent_individual, child_individual, ban_generation_list = [], crossover_point_max = CROSSOVER_POINT_MAX):
    """交叉

    Args:
        parent_individual (Individual): 個体1
        child_individual (Individual): 個体2
        ban_generation_list (list, optional): 生成禁止リスト. Defaults to [].
        crossover_point_max (int, optional): 交叉点最大数. Defaults to CROSSOVER_POINT_MAX.

    Returns:
        Individual: 新個体
    """
    parent_list, joint_index = parent_individual.get_mating_content()
    child_list, _ = child_individual.get_mating_content()

    while True: # まだ生成されていない個体が生まれるまで無限生成
        result = []
        crossover_point = set([random.randint(0, len(parent_list) - 1) for _ in range(crossover_point_max)])
        is_parent = [True, False][random.randint(0,1)]
        for i in range(len(parent_list)):
            if is_parent:
                result.append(parent_list[i])
            else:
                result.append(child_list[i])
            if i+1 in crossover_point:
                is_parent = not is_parent

        individual = Individual.format_mating_content(result, joint_index)
        if individual.is_allow_generate(ban_generation_list):
            break

    return individual

def mutate(work_num=0, weight_num=0):
    """突然変異

    Args:
        work_num (int): ワーク数

    Returns:
        Individual: 個体
    """
    return Individual(work_num=work_num, weight_num=weight_num)

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