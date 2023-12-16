#
# 個体用の多次元クラスタ
# k平均法を使用：https://qiita.com/g-k/items/0d5d22a12a4507ecbf11
#
from os import path
import sys
import math
import random
import copy
sys.path.append(path.dirname(__file__))
from constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT
from individual import Individual, INDIVIDUAL_PLOT_LIST_X_KEY, INDIVIDUAL_PLOT_LIST_Y_KEY

CLUSTER_LIST_INDIVIDUAL_LIST_KEY = "individual_list"
CLUSTER_GRAVITY_POS = "gravity_pos"
CLUSTER_GRAVITY_POS_X = "x"
CLUSTER_GRAVITY_POS_Y = "y"

CLUSTER_PLOT_MAX_KEY = "cluster_plot_max"
CLUSTER_LIST_KEY = "cluster_list"
CLUSTER_MAX_KEY = "cluster_max"
CLUSTER_LOOP_KEY = "cluster_loop"

class Cluster:
    _plot_max = -1
    _cluster_list = []
    _cluster_max = -1
    _cluster_loop_max = -1
    def __init__(self, plot_max, cluster_max = CLUSTER_MAX_DEFAULT, cluster_loop_max = CLUSTER_LOOP_MAX_DEFAULT, cluster_list = []):
        """初期化

        Args:
            cluster_max (int, optional): クラスタの数. Defaults to CLUSTER_MAX_DEFAULT.
            cluster_loop_max (int, optional): クラスタのループ数. Defaults to CLUSTER_LOOP_MAX_DEFAULT.
            cluster_list (list, optional): クラスタリスト. Defaults to [].
        """
        self._plot_max = plot_max 
        self._cluster_max = cluster_max
        self._cluster_loop_max = cluster_loop_max
        self._cluster_list = cluster_list

    def generate(self, individual_addition_list):
        """クラスター生成

        Args:
            individual_addition_list (list): クラスタに追加する個体群

        Returns:
            list: クラスターリスト
        """
        individual_list = self._summarize_current_individual_list(individual_addition_list)

        # クラスタ分け番号をランダムに振ったクラスタを初期生成
        cluster_list = [{
            CLUSTER_LIST_INDIVIDUAL_LIST_KEY: [],
            CLUSTER_GRAVITY_POS: [{
                CLUSTER_GRAVITY_POS_X: 0,
                CLUSTER_GRAVITY_POS_Y: 0
            } for _ in range(self._plot_max)]
        } for _ in range(self._cluster_max)]
        cluster_num_list = [i % self._cluster_max for i in range(len(individual_list))]
        random.shuffle(cluster_num_list)
        for ind_i, individual in enumerate(individual_list):
            cls_i = cluster_num_list[ind_i]
            cluster_list[cls_i][CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual)

        for _ in range(self._cluster_loop_max):
            is_cluster_changed = False # いずれかの個体でクラスタリング変更があったかのフラグ
            # 再重心計算
            for cluster in cluster_list:
                for individual in cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]:
                    plot_list = individual.get_plot_list()
                    for plot_i, plot in enumerate(plot_list):
                        cluster[CLUSTER_GRAVITY_POS][plot_i][CLUSTER_GRAVITY_POS_X] = self._calc_gravity_center_coordinate(
                            cluster[CLUSTER_GRAVITY_POS][plot_i][CLUSTER_GRAVITY_POS_X],
                            plot[INDIVIDUAL_PLOT_LIST_X_KEY]
                        )
                        cluster[CLUSTER_GRAVITY_POS][plot_i][CLUSTER_GRAVITY_POS_Y] = self._calc_gravity_center_coordinate(
                            cluster[CLUSTER_GRAVITY_POS][plot_i][CLUSTER_GRAVITY_POS_Y],
                            plot[INDIVIDUAL_PLOT_LIST_Y_KEY]
                        )

            # 再クラスタリング
            for clus_i1, cluster1 in enumerate(cluster_list):
                for clus_i2, cluster2 in enumerate(cluster_list):
                    if clus_i1 == clus_i2: continue
                    for ind_i1, individual1 in enumerate(cluster1[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]):
                        for ind_i2, individual2 in enumerate(cluster2[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]):
                            if self._is_individual_swap(cluster1, individual1, individual2):
                                individual1_tmp = cluster1[CLUSTER_LIST_INDIVIDUAL_LIST_KEY].pop(ind_i1)
                                individual2_tmp = cluster2[CLUSTER_LIST_INDIVIDUAL_LIST_KEY].pop(ind_i2)
                                cluster1[CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual2_tmp)
                                cluster2[CLUSTER_LIST_INDIVIDUAL_LIST_KEY].append(individual1_tmp)
                                is_cluster_changed = True
                    

            # 全ての要素が属するクラスタに変更がなければ安定としてループ終了
            if is_cluster_changed is False:
                break
        self._cluster_list = cluster_list
        return cluster_list

    def _summarize_current_individual_list(self, individual_addition_list):
        """新規追加分とクラスタに現在するすべての個体をまとめる

        Args:
            individual_addition_list (Individual[]): 追加個体群リスト

        Returns:
            Individual[]: 個体群のリスト
        """
        result = []

        result.extend(copy.deepcopy(individual_addition_list))
        for cluster in self._cluster_list:
            result.extend(copy.deepcopy(cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]))
            
        return result

    def _calc_gravity_center_coordinate(self, coordinate_1, coordinate_2):
        return (coordinate_1 + coordinate_2) / 2

    def _calc_plot_distance(x1, x2, y1, y2):
        """プロットの距離算出
        ユーグリッド距離(https://ja.wikipedia.org/wiki/%E3%83%A6%E3%83%BC%E3%82%AF%E3%83%AA%E3%83%83%E3%83%89%E8%B7%9D%E9%9B%A2)

        Args:
            x1 (int)
            x2 (int)
            y1 (int)
            y2 (int)

        Returns:
            int: 距離
        """
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _is_individual_swap(self, my_cluster, my_cluster_individual, other_cluster_individual):
        """クラスタ重心とそれに属する個体・属さない個体との距離を測り、
        属さない個体のほうがふさわしければ交換可能フラグを返す

        Args:
            my_cluster (dict): 対象クラスタ
            my_cluster_individual (Individual): クラスタに属する個体
            other_cluster_individual (Individual): クラスタに属さない個体

        Returns:
            bool: 交換フラグ(交換すべき:True, 交換不要:False)
        """
        my_individual_plot = my_cluster_individual.get_plot_list()
        other_individual_plot = other_cluster_individual.get_plot_list()
        my_cluster_plot = my_cluster[CLUSTER_GRAVITY_POS]
        
        my_distance = 0
        other_distance = 0
        for plot_i in range(self._plot_max):
            my_distance += Cluster._calc_plot_distance(
                my_individual_plot[plot_i][INDIVIDUAL_PLOT_LIST_X_KEY], my_cluster_plot[plot_i][CLUSTER_GRAVITY_POS_X],
                my_individual_plot[plot_i][INDIVIDUAL_PLOT_LIST_Y_KEY], my_cluster_plot[plot_i][CLUSTER_GRAVITY_POS_Y],
            )
            other_distance += Cluster._calc_plot_distance(
                other_individual_plot[plot_i][INDIVIDUAL_PLOT_LIST_X_KEY], my_cluster_plot[plot_i][CLUSTER_GRAVITY_POS_X],
                other_individual_plot[plot_i][INDIVIDUAL_PLOT_LIST_Y_KEY], my_cluster_plot[plot_i][CLUSTER_GRAVITY_POS_Y],
            )
            
        return my_distance > other_distance

    def get_random_individual_list(self, solve_num):
        """各クラスタの順番をシャッフルし、各クラスタからランダムに選びだした解のリストを返す

        Args:
            solve_num (int): 解の数

        Returns:
            Individual[]: 個体群のリスト
        """
        result = []
        selected_cluster_list = [i for i in range(self._cluster_max)]
        random.shuffle(selected_cluster_list)
        for i in range(solve_num):
            selected_cluster_index = selected_cluster_list[i % self._cluster_max]
            individual_list = self._cluster_list[selected_cluster_index][CLUSTER_LIST_INDIVIDUAL_LIST_KEY]
            individual_list_index = individual_list.index(random.choice(individual_list))
            target_individual = individual_list.pop(individual_list_index)
            result.append(target_individual)
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
                CLUSTER_GRAVITY_POS: cluster[CLUSTER_GRAVITY_POS]
            })
        return {
            CLUSTER_PLOT_MAX_KEY: self._plot_max,
            CLUSTER_LIST_KEY: cluster_list_date,
            CLUSTER_MAX_KEY: self._cluster_max,
            CLUSTER_LOOP_KEY: self._cluster_loop_max
        }
        
    def deserialize(cluster_data):
        """デシリアライズ

        Args:
            cluster_data (dict): デシリアライズ対象のデータ

        Returns:
            Cluster: 解析結果のクラスタ
        """
        cluster_list = []
        for cluster in cluster_data[CLUSTER_LIST_KEY]:
            
            cluster_list.append({
                CLUSTER_LIST_INDIVIDUAL_LIST_KEY: [Individual.deserialize(individual) for individual in cluster[CLUSTER_LIST_INDIVIDUAL_LIST_KEY]],
                CLUSTER_GRAVITY_POS: cluster[CLUSTER_GRAVITY_POS]
            })
        return Cluster(
            plot_max=cluster_data[CLUSTER_PLOT_MAX_KEY],
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
    class Test(unittest.TestCase):
        def test_create_individual(self):
            work_num = 10
            weight_num = 4
            individual_list = [Individual(work_num=work_num, weight_num=weight_num) for _ in range(100)]
            cluster =  Cluster(
                plot_max=Individual.get_plot_max(work_num, weight_num),
                cluster_max= 20,
                cluster_loop_max=10
            )
            cluster.generate(individual_list)
            individual_list = cluster.get_random_individual_list(10)
            self.assertTrue(len(individual_list) == 10)
        def test_serialize_deserialize(self):
            work_num = 10
            weight_num = 4
            individual_list = [Individual(work_num=work_num, weight_num=weight_num) for _ in range(100)]
            cluster =  Cluster(
                plot_max=Individual.get_plot_max(work_num, weight_num),
                cluster_max= 20,
                cluster_loop_max=10
            )
            cluster.generate(individual_list)
            cluster_data=cluster.serialize()
            Cluster.deserialize(cluster_data)
        def test_recreate_individual_and_get_schedule(self):
            work_num = 10
            weight_num = 4
            individual_list1 = [Individual(work_num=work_num, weight_num=weight_num) for _ in range(100)]
            cluster =  Cluster(
                plot_max=Individual.get_plot_max(work_num, weight_num),
                cluster_max= 20,
                cluster_loop_max=10
            )
            cluster.generate(individual_list1)
            individual_list2 = [Individual(work_num=work_num, weight_num=weight_num) for _ in range(100)]
            cluster.generate(individual_list2)
            individual_list = cluster.get_random_individual_list(10)
            self.assertTrue(len(individual_list) == 10)
    unittest.main()