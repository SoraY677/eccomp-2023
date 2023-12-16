#
# 個体
#
from os import path
import sys
import random
import copy
sys.path.append(path.dirname(__file__))
from constraints import WORK_MAX_DAY, WORK_MIN_DAY

INDIVIDUAL_CONTENT_SCHEDULE_KEY = "schedule"
INDIVIDUAL_CONTENT_SCHEDULE_START_KEY = "start"
INDIVIDUAL_CONTENT_SCHEDULE_END_KEY = "end"
INDIVIDUAL_CONTENT_WEIGHTS_KEY = "weights"
INDIVIDUAL_PLOT_LIST_X_KEY = "x"
INDIVIDUAL_PLOT_LIST_Y_KEY = "y"

class Individual:
    _content = {}
    def __init__(self,
        schedule_list = None,
        weight_list = None,
        ban_generation_list = [],
        work_num = 0,
        weight_num = 0
    ):
        """初期化

        Args:
            schedule_list (int[], optional): スケジュールの配列. Defaults to None.
            weight_list (float[], optional): _description_. Defaults to None.
            ban_generation_list (list, optional): _description_. Defaults to [].
            work_num (int, optional): ワーク数. Defaults to 0.
            weight_num (float, optional): SCIP重み数. Defaults to 0.
        """
        self._content = {
            INDIVIDUAL_CONTENT_SCHEDULE_KEY: [],
            INDIVIDUAL_CONTENT_WEIGHTS_KEY: []
        }
        while True:
            if len(self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY]) == 0 and schedule_list is None and work_num > 0:
                self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = self._create_random_schedule_list(work_num)
            if len(self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY]) == 0 and weight_list is None and weight_num > 0:
                self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY] = self._create_random_weight_list(weight_num)
            if self.is_allow_generate(ban_generation_list):
                break
        
        if schedule_list is not None:
            self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY] = copy.copy(schedule_list)
        if weight_list is not None:
            self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY] = copy.copy(weight_list)

    def _create_random_schedule_list(self, work_num):
        """スケジュールリスト生成

        Args:
            work_num (int): ワーク数

        Returns:
            list: 開始時間・終了時間の配列
        """
        result = []
        for _ in range(work_num):
            start = random.randint(WORK_MIN_DAY, WORK_MAX_DAY)
            end = random.randint(start, WORK_MAX_DAY)
            result.append(start)
            result.append(end)
        
        return result

    def _create_random_weight_list(self, weight_num, ban_generation_list):
        """ランダムに重みを決定

        Args:
            weight_num (int): 重みの数
            ban_generation_list (list): 作成禁止リスト（過去に作成済み）
        Returns:
            list: 重みのリスト 
        """
        return [random.random() for _ in range(weight_num)] 

    def get_schedule_list(self):
        """スケジュール要素を取得

        Returns:
            int[]: スケジュールの配列
        """
        return self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY]

    def get_weight_list(self):
        """SCIP重みリストを取得

        Returns:
            float[]: SCIP重みの配列
        """
        return self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY]

    def get_plot_list(self):
        """プロット用のリストを作成

        Returns:
            list: プロット用リスト
        """
        # Todo: スケジュールと重みのプロット幅が異なることから正しくプロットできていないので修正して
        result = []
        # スケジュール
        # x -> 工数 = endtime - starttime
        # y -> 優先度 = starttime
        schedule_list = self.get_schedule_list()
        if len(schedule_list) != 0:
            result.extend([{
                INDIVIDUAL_PLOT_LIST_X_KEY: schedule_list[i+1] - schedule_list[i],
                INDIVIDUAL_PLOT_LIST_Y_KEY: schedule_list[i+1],
            } for i in range(0, len(schedule_list), 2)])
        # SCIP重み
        # x,y -> 異なる重み
        weight_list = self.get_weight_list()
        if len(weight_list) != 0:
            for line_i in range(1, len(weight_list), 1):
                for row_i in range(line_i):
                    result.append({
                        INDIVIDUAL_PLOT_LIST_X_KEY: weight_list[row_i],
                        INDIVIDUAL_PLOT_LIST_Y_KEY: weight_list[line_i],
                    })

        if len(result) != Individual.get_plot_max(len(schedule_list)/2, len(weight_list)):
            return None

        return result

    def get_plot_max(work_num=0, weight_num=0):
        """プロット配列の数を取得

        Args:
            work_num (int, optional): ワーク数. Defaults to -1.
            weight_num (float, optional): SCIP重み数. Defaults to -1.

        Returns:
            int: プロット配列数
        """
        work_max = work_num
        weight_max = (weight_num-1)*(weight_num)/2 if weight_num > 0 else 0
        return int(work_max + weight_max)

    def serialize(self):
        """シリアライズ

        Returns:
            dict: JSON対応Dict
        """
        return {
            INDIVIDUAL_CONTENT_SCHEDULE_KEY: self._content[INDIVIDUAL_CONTENT_SCHEDULE_KEY],
            INDIVIDUAL_CONTENT_WEIGHTS_KEY: self._content[INDIVIDUAL_CONTENT_WEIGHTS_KEY]
        }

    def deserialize(individual_json):
        """デシリアライズ

        Args:
            individual_json (dict): JSON

        Returns:
            Individual: 個体
        """
        return Individual(schedule_list=individual_json[INDIVIDUAL_CONTENT_SCHEDULE_KEY], weight_list=individual_json[INDIVIDUAL_CONTENT_WEIGHTS_KEY])

    def get_mating_content(self):
        """個体から交叉用の配列への変換用

        Returns:
            list, int: 交叉用の配列, 結合部分(結合なしなら-1)
        """
        schedule_list = self.get_schedule_list()
        mating_list = [{
            INDIVIDUAL_CONTENT_SCHEDULE_START_KEY: schedule_list[i],
            INDIVIDUAL_CONTENT_SCHEDULE_END_KEY: schedule_list[i+1] 
        } for i in range(0, len(schedule_list), 2)]
        joint_index = len(schedule_list) / 2
        
        if len(self.get_weight_list()) != 0:
            mating_list.extend(self.get_weight_list())
        
        return mating_list, int(joint_index)

    def format_mating_content(mating_list, joint_index):
        """交叉用配列から個体への変換

        Args:
            mating_list (list): 交叉用配列
            joint_index (int): 結合部

        Returns:
            Individual: 新規個体
        """
        schedule_dict_list = mating_list[:joint_index]
        schedule_list = []
        for schedule_dict in schedule_dict_list:
            schedule_list.append(schedule_dict[INDIVIDUAL_CONTENT_SCHEDULE_START_KEY])
            schedule_list.append(schedule_dict[INDIVIDUAL_CONTENT_SCHEDULE_END_KEY])
        weight_list = mating_list[joint_index:]
        
        return Individual(schedule_list, weight_list)
        
    def is_allow_generate(self, ban_generation_list):
        # Todo:後で実装
        return True
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    class Test(unittest.TestCase):
        def test_create_individual_and_get_items(self):
            work_num = 10
            weight_num = 4
            individual = Individual(work_num=work_num, weight_num=weight_num)
            self.assertTrue(len(individual.get_schedule_list()) == work_num * 2)
            self.assertTrue(len(individual.get_weight_list()) == weight_num)
        def test_designation_create_individual(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            weight_list = [0.6947156931851072, 0.5260175487956781, 0.7449466428168457, 0.29364899784938414]
            individual = Individual(schedule_list=schedule_list, weight_list=weight_list)
            self.assertTrue(individual.get_schedule_list() == schedule_list)
            self.assertTrue(individual.get_weight_list() == weight_list)
        def test_serialize(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            weight_list = [0.6947156931851072, 0.5260175487956781, 0.7449466428168457, 0.29364899784938414]
            individual = Individual(schedule_list=schedule_list, weight_list=weight_list)
            self.assertTrue({
                {
                    INDIVIDUAL_CONTENT_SCHEDULE_KEY: schedule_list,
                    INDIVIDUAL_CONTENT_WEIGHTS_KEY: weight_list
                } == individual.serialize()
            })
        def test_desirialize(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            weight_list = [0.6947156931851072, 0.5260175487956781, 0.7449466428168457, 0.29364899784938414]
            individual = Individual.deserialize(individual_json = {
                    INDIVIDUAL_CONTENT_SCHEDULE_KEY: schedule_list,
                    INDIVIDUAL_CONTENT_WEIGHTS_KEY: weight_list
            })
            self.assertTrue(individual.get_schedule_list() == schedule_list)
            self.assertTrue(individual.get_weight_list() == weight_list)
        def test_get_plot_list(self):
            schedule_list = [7, 7, 6, 8, 3, 7, 9, 9, 6, 9, 2, 2, 1, 8, 1, 2, 1, 7, 7, 8]
            weight_list = [0.6947156931851072, 0.5260175487956781, 0.7449466428168457, 0.29364899784938414]
            individual = Individual(schedule_list=schedule_list, weight_list=weight_list)
            plot_list = individual.get_plot_list()
            self.assertTrue(len(plot_list) == 16)
        # Todo: 禁止リストに関するテスト
            
    unittest.main()