#
# 解の多次元クラスタ
# k平均法を使用：https://qiita.com/g-k/items/0d5d22a12a4507ecbf11
#
import math
import random
from constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT

CLUSTER_LIST_INDIVIDUAL_LIST_KEY = "individual_list"
CLUSTER_LIST_CLUSTER_NUM = "cluster_num"
CLUSTER_LIST_CENTER_POS_X_LIST = "center_pos_x_list"
CLUSTER_LIST_CENTER_POS_Y_LIST = "center_pos_y_list"

class Cluster:
    _cluster_list = []
    _cluster_max = -1
    _cluster_loop_max = -1
    def __init__(self, cluster_max = CLUSTER_MAX_DEFAULT, cluster_loop_max = CLUSTER_LOOP_MAX_DEFAULT):
        """初期化

        Args:
            cluster_max (int, optional): クラスタの数. Defaults to CLUSTER_MAX_DEFAULT.
            cluster_loop_max (int, optional): クラスタのループ数. Defaults to CLUSTER_LOOP_MAX_DEFAULT.
        """
        self._cluster_max = cluster_max
        self._cluster_loop_max = cluster_loop_max

    def generate_cluster(self, individual_list):
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
            cluster_list = cluster.generate_cluster(individual_list)
            end_time = datetime.datetime.now()
            
            self.assertTrue(len(cluster_list) == 20)
    unittest.main()