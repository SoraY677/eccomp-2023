#
# 解の多次元クラスタ
# k平均法を使用：https://qiita.com/g-k/items/0d5d22a12a4507ecbf11
#
import math
import random
import copy
if __name__ == "__main__":
    from constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT
    from individual import Individual
else:
    from src.solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT
    from src.solution.individual import Individual

CLUSTER_LIST_INDIVIDUAL_LIST_KEY = "individual_list"
CLUSTER_LIST_CLUSTER_NUM = "cluster_num"
CLUSTER_LIST_CENTER_POS_X_LIST = "center_pos_x_list"
CLUSTER_LIST_CENTER_POS_Y_LIST = "center_pos_y_list"
CLUSTER_LIST_KEY = "cluster_list"
CLUSTER_MAX_KEY = "cluster_max"
CLUSTER_LOOP_KEY = "cluster_key"

class IndividualCluster:
    _cluster_list = []
    _cluster_max = -1
    _cluster_loop_max = -1
    def __init__(self, cluster_max = CLUSTER_MAX_DEFAULT, cluster_loop_max = CLUSTER_LOOP_MAX_DEFAULT, cluster_list = []):
        """初期化

        Args:
            cluster_max (int, optional): クラスタの数. Defaults to CLUSTER_MAX_DEFAULT.
            cluster_loop_max (int, optional): クラスタのループ数. Defaults to CLUSTER_LOOP_MAX_DEFAULT.
        """
        self._cluster_list = cluster_list
        self._cluster_max = cluster_max
        self._cluster_loop_max = cluster_loop_max

    def generate(self, individual_addition_list):
        """クラスター生成

        Args:
            individual_addition_list (list): 追加の個体群

        Returns:
            list: クラスターリスト
        """
        individual_list = self._extract_current_individual_list(individual_addition_list)
        return self._generate_cluster(individual_list)

    def _generate_cluster(self, individual_list):
        """クラスターを生成する

        Args:
            individual_list (list): 個体群のリスト

        Returns:
            list: クラスタリスト
        """
        individual_tuple = tuple(individual_list)
        # クラスタ分け番号をランダムに振る
        cluster_list = [{
            CLUSTER_LIST_INDIVIDUAL_LIST_KEY: [],
            CLUSTER_LIST_CENTER_POS_X_LIST: [],
            CLUSTER_LIST_CENTER_POS_Y_LIST: []
        } for _ in range(self._cluster_max)]
        cluster_num_list = [i % self._cluster_max for i in range(len(individual_list))]
        random.shuffle(cluster_num_list)
        for ind_i, individual in enumerate(individual_tuple):
            cls_i = cluster_num_list[ind_i]
            cluster_list[cls_i][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual)
        

        # 再重心計算・クラスタリング
        is_some_cluster_center_change = True
        cluster_list_tuple = tuple(cluster_list)
        for _ in range(self._cluster_loop_max):
            # クラスタの重心を再計算
            for cls_i, cluster in enumerate(cluster_list_tuple):
                cluster_individual_tuple = tuple(cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY])
                for target_individual in cluster_individual_tuple:
                    individual_pos_x_list, individual_pos_y_list = self._calc_individual_pos(target_individual)
                    cluster_list[cls_i][CLUSTER_LIST_CENTER_POS_X_LIST] = [0] * len(individual_pos_x_list)
                    cluster_list[cls_i][CLUSTER_LIST_CENTER_POS_Y_LIST] = [0] * len(individual_pos_x_list)
                    for sch_i in range(len(individual_pos_x_list)):
                        cluster_pos_x = cluster[CLUSTER_LIST_CENTER_POS_X_LIST]
                        cluster_list[cls_i][CLUSTER_LIST_CENTER_POS_X_LIST][sch_i] = self._calc_center_pos_from_2_pos(cluster_pos_x[sch_i], individual_pos_x_list[sch_i])
                        cluster_pos_y = cluster[CLUSTER_LIST_CENTER_POS_Y_LIST]
                        cluster_list[cls_i][CLUSTER_LIST_CENTER_POS_Y_LIST][sch_i] = self._calc_center_pos_from_2_pos(cluster_pos_y[sch_i], individual_pos_y_list[sch_i])

            # 再クラスタリング
            for clus_i1, cluster1 in enumerate(cluster_list_tuple):
                for clus_i2, cluster2 in enumerate(cluster_list_tuple):
                    if clus_i1 == clus_i2:
                        continue
                    cluster1_tuple = cluster1[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]
                    for ind_i1, individual1 in enumerate(cluster1_tuple):
                        cluster2_tuple = cluster2[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]
                        for ind_i2, individual2 in enumerate(cluster2_tuple):
                            individual_pos_x_list1, individual_pos_y_list1 = self._calc_individual_pos(individual1)
                            individual_pos_x_list2, individual_pos_y_list2 = self._calc_individual_pos(individual2)
                            dif1, dif2 = 0, 0
                            for sch_i in range(len(individual_pos_x_list1)):
                                x1 = self._calc_center_pos_from_2_pos(cluster_list[clus_i1][CLUSTER_LIST_CENTER_POS_X_LIST][sch_i], individual_pos_x_list1[sch_i])
                                y1 = self._calc_center_pos_from_2_pos(cluster_list[clus_i1][CLUSTER_LIST_CENTER_POS_Y_LIST][sch_i], individual_pos_y_list1[sch_i])
                                dif1 += math.sqrt((cluster2[CLUSTER_LIST_CENTER_POS_X_LIST][sch_i] - x1) ** 2 + (cluster2[CLUSTER_LIST_CENTER_POS_Y_LIST][sch_i] * y1) ** 2)
                                x2 = self._calc_center_pos_from_2_pos(cluster_list[clus_i2][CLUSTER_LIST_CENTER_POS_X_LIST][sch_i], individual_pos_x_list2[sch_i])
                                y2 = self._calc_center_pos_from_2_pos(cluster_list[clus_i2][CLUSTER_LIST_CENTER_POS_Y_LIST][sch_i], individual_pos_y_list2[sch_i])
                                dif2 += math.sqrt((cluster2[CLUSTER_LIST_CENTER_POS_X_LIST][sch_i] - x2) ** 2 + (cluster2[CLUSTER_LIST_CENTER_POS_Y_LIST][sch_i] * y2) ** 2)
                            if dif1 < dif2:
                                individual1_tmp = cluster_list[clus_i1][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].pop(ind_i1)
                                individual2_tmp = cluster_list[clus_i2][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].pop(ind_i2)
                                cluster_list[clus_i1][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual2_tmp)
                                cluster_list[clus_i2][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual1_tmp)
                                is_some_cluster_center_change = False
                    

            # 全ての要素が属するクラスタに変更がなければ安定としてループ終了
            if is_some_cluster_center_change is False:
                break
        self._cluster_list = cluster_list
        return cluster_list

    def _calc_individual_pos(self, individual):
        """個体の座標を計算

        Args:
            individual (Individual): 個体のインスタンス

        Returns:
            tuple(list, list): (時間を要した、優先した)の距離を各ワークごとに算出した配列2つ
        """
        schedule_list = individual.get_schedule()
        # x座標 = どのワークにどれほど時間をかけたか
        x_list = [schedule_list[i+1] - schedule_list[i] for i in range(0, len(schedule_list), 2)]         
        # y座標 = どのワークが優先されたか
        y_list = [row[0] for row in sorted([(i, schedule_list[i]) for i in range(0, len(schedule_list), 2)], key=lambda x:x[1])]
        
        return x_list, y_list

    def _calc_center_pos_from_2_pos(self, pos1, pos2):
        return (pos1 + pos2) / 2

    def _extract_current_individual_list(self, individual_addition_list):
        result = []

        result.extend(copy.deepcopy(individual_addition_list))          
        for cluster in self._cluster_list:
            result.extend(copy.deepcopy(cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]))
            
        return result

    def get_separated_individual_list(self, solve_num, cluster_selected_weight = None):
        result = []
        cluster_selected_rate_tmp = cluster_selected_weight if cluster_selected_weight is not None else [1] * self._cluster_max

        for _ in range(solve_num):
            selected_cluster_num = random.choices([i for i in range(self._cluster_max)], k = 1, weights = cluster_selected_rate_tmp)[0]
            individual_list = self._cluster_list[selected_cluster_num][CLUSTER_LIST_INDIVIDUAL_LIST_KEY]
            individual_list_index = individual_list.index(random.choice(individual_list))
            target_individual = individual_list.pop(individual_list_index)
            result.append(target_individual)
            
            if len(individual_list) == 0:
                cluster_selected_rate_tmp[selected_cluster_num] = 0
                
                cluster_selected_rate_set = set(cluster_selected_rate_tmp)
                if len(cluster_selected_rate_set) == 1 and cluster_selected_rate_set[0] == 0:
                    break
                
        return result
    
    def serialize(self):
        """シリアライズ

        Returns:
            dict: シリアライズデータ
        """
        cluster_list_date = []
        for cluster in self._cluster_list:
            cluster_list_date.append({
                CLUSTER_LIST_INDIVIDUAL_LIST_KEY: [individual.serialize() for individual in cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]],
                CLUSTER_LIST_CENTER_POS_X_LIST: cluster[CLUSTER_LIST_CENTER_POS_X_LIST],
                CLUSTER_LIST_CENTER_POS_Y_LIST: cluster[CLUSTER_LIST_CENTER_POS_Y_LIST]
            })
        return {
            CLUSTER_LIST_KEY: cluster_list_date,
            CLUSTER_MAX_KEY: self._cluster_max,
            CLUSTER_LOOP_KEY: self._cluster_loop_max
        }
        
    def desirialize(cluster_data):
        """デシリアライズ

        Args:
            cluster_data (dict): デシリアライズ対象のデータ

        Returns:
            dict: デシリアライズデータ
        """
        cluster_list = []
        for cluster in cluster_data[CLUSTER_LIST_KEY]:
            
            cluster_list.append({
                CLUSTER_LIST_INDIVIDUAL_LIST_KEY: [Individual().deserialize(individual) for individual in cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]],
                CLUSTER_LIST_CENTER_POS_X_LIST: cluster[CLUSTER_LIST_CENTER_POS_X_LIST],
                CLUSTER_LIST_CENTER_POS_Y_LIST: cluster[CLUSTER_LIST_CENTER_POS_Y_LIST]
            })
        return Cluster(
            cluster_max=cluster_data[CLUSTER_MAX_KEY],
            cluster_loop_max=cluster_data[CLUSTER_LOOP_KEY],
            cluster_list=cluster_list
        )
#
# 単体テスト
#
if __name__ == "__main__":
    import unittest
    from individual import Individual
    import datetime
    class Test(unittest.TestCase):
        def test_create_individual_and_get_schedule(self):
            start_time = datetime.datetime.now()
            individual_list = [Individual(10) for _ in range(100)]
            cluster =  Cluster(
                cluster_max= 20,
                cluster_loop_max=10
            )
            cluster.generate(individual_list)
            individual_list = cluster.get_separated_individual_list(10)
            end_time = datetime.datetime.now()
            self.assertTrue(len(individual_list) == 10)
        
        def test_recreate_individual_and_get_schedule(self):
            individual_list1 = [Individual(10) for _ in range(100)]
            cluster =  Cluster(
                cluster_max= 20,
                cluster_loop_max=10
            )
            cluster.generate(individual_list1)
            individual_list2 = [Individual(10) for _ in range(100)]
            cluster.generate(individual_list2)
            individual_list = cluster.get_separated_individual_list(10)
            self.assertTrue(len(individual_list) == 10)
    unittest.main()