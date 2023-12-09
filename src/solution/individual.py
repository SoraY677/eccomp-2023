#
# 個体
#
import random
from constraints import WORK_MAX_DAY,WORK_MIN_DAY

INDIVIDUAL_CONTENT_SCHEDULE_KEY = "schedule"
INDIVIDUAL_CONTENT_WEIGHTS_KEY = "weights" # Todo: 多目的部門用。後で実装

class Individual:
    _content = {
        INDIVIDUAL_CONTENT_SCHEDULE_KEY: []
    }
    def __init__(self, work_num):
        self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = self._create(work_num)
    
    def _create(self, work_num):
        result = []
        for _ in range(work_num):
            start = random.randint(WORK_MIN_DAY, WORK_MAX_DAY)
            end = random.randint(start, WORK_MAX_DAY)
            result.append(start)
            result.append(end)
        return result
    
    def get_schedule(self):
        return self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY]
    
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_create_individual_and_get_schedule(self):
            individual = Individual(10)
            self.assertTrue(len(individual.get_schedule()) == 20)
    unittest.main()