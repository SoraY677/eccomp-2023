#
# 個体
#
import random
import copy
if __name__ == "__main__":
    from constraints import WORK_MAX_DAY, WORK_MIN_DAY
else:
    from src.solution.constraints import WORK_MAX_DAY, WORK_MIN_DAY

INDIVIDUAL_CONTENT_SCHEDULE_KEY = "schedule"
INDIVIDUAL_CONTENT_WEIGHTS_KEY = "weights" # Todo: 多目的部門用。後で実装

class Individual:
    _content = {}
    def __init__(self, work_num = -1, ban_generation_list = []):
        """初期化

        Args:
            work_num (int): ワーク数
            ban_generation_list (list): 作成禁止リスト（過去に作成済み）
        """
        self._content = {}
        self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = self._create(work_num, ban_generation_list)
    
    def _create(self, work_num, ban_generation_list = []):
        """生成

        Args:
            work_num (int): ワーク数
            ban_generation_list (list): 作成禁止リスト（過去に作成済み）

        Returns:
            list: 開始時間・終了時間の配列
        """
        result = []
        while(True):
            for _ in range(work_num):
                start = random.randint(WORK_MIN_DAY, WORK_MAX_DAY)
                end = random.randint(start, WORK_MAX_DAY)
                result.append(start)
                result.append(end)
            if result not in ban_generation_list:
                break
        
        return result
    
    def create(self, schedule_list, ban_generation_list = []):
        """生成

        Args:
            schedule_list (list): スケジュールの配列
            ban_generation_list (list, optional): 生成禁止リスト. Defaults to [].

        Returns:
            Individual: 個体
        """
        result = []
        
        for i in range(0, len(schedule_list), 2):
            start_time = schedule_list[i]
            end_time = schedule_list[i+1]
            
            if end_time < start_time:
                end_time = random.randint(start_time, WORK_MAX_DAY)
            result.append(start_time)
            result.append(end_time)
        
        self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = copy.copy(result)
        return self

    def get_schedule(self):
        """スケジュール要素を取得

        Returns:
            str: スケジュールの配列
        """
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
        def test_designation_create_individual(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            individual = Individual().create(schedule_list)
            self.assertTrue(individual.get_schedule() == schedule_list)
    unittest.main()