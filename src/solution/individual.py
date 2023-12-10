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
    def __init__(self,
        schedule_list = None,
        weight_list = None,
        ban_generation_list = [],
        work_num = None,
        weight_num = None
    ):
        """初期化

        Args:
            work_num (int): ワーク数
            ban_generation_list (list): 作成禁止リスト（過去に作成済み）
        """
        self._content = {
            INDIVIDUAL_CONTENT_SCHEDULE_KEY: [],
            INDIVIDUAL_CONTENT_WEIGHTS_KEY: []
        }
        
        if schedule_list is not None:
            self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = copy.copy(schedule_list)
        if weight_list is not None:
            self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY] = copy.copy(weight_list)
        
        if len(self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] == 0):
            if work_num is not None:
                self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = self._create_random_schedule_list(work_num, ban_generation_list)
            
        if len(self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY] == 0 and weight_num is not None):
                self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY] = self._create_random_weight_list(weight_num, ban_generation_list)
    
    def _create_random_schedule_list(self, work_num, ban_generation_list = []):
        """スケジュールリスト生成

        Args:
            work_num (int): ワーク数
            ban_generation_list (list): 作成禁止リスト（過去に作成済み）

        Returns:
            list: 開始時間・終了時間の配列
        """
        while(True):
            result = []
            for _ in range(work_num):
                start = random.randint(WORK_MIN_DAY, WORK_MAX_DAY)
                end = random.randint(start, WORK_MAX_DAY)
                result.append(start)
                result.append(end)
            if result not in ban_generation_list:
                break
        
        return result
    
    def _create_random_weight_list(self, weight_num):
        """ランダムに重みを決定

        Args:
            weight_num (int): 重みの数

        Returns:
            list: 重みのリスト 
        """
        return [random.random() for _ in range(weight_num)] 

    def get_schedule(self):
        """スケジュール要素を取得

        Returns:
            str: スケジュールの配列
        """
        return self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY]
    
    def get_weight_list(self):
        return self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY]
    
    def serialize(self):
        """シリアライズ

        Returns:
            dict: 辞書型
        """
        return {
            INDIVIDUAL_CONTENT_SCHEDULE_KEY: self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY],
            INDIVIDUAL_CONTENT_WEIGHTS_KEY: self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY]
        }
        
    def deserialize(self, individual_json):
        """デシリアライズ

        Args:
            individual_json (dict): JSON

        Returns:
            Individual: 個体
        """
        return Individual(schedule_list=individual_json[INDIVIDUAL_CONTENT_SCHEDULE_KEY], weight_list=individual_json[INDIVIDUAL_CONTENT_WEIGHTS_KEY])
    
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_create_individual_and_get_schedule(self):
            individual = Individual(work_num=10)
            self.assertTrue(len(individual.get_schedule()) == 20)
        def test_designation_create_individual(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            individual = Individual(schedule_list=schedule_list)
            self.assertTrue(individual.get_schedule() == schedule_list)
    unittest.main()