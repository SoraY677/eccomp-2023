#
# ソルバ
#
import random
from os import path
import sys
sys.path.append(path.dirname(__file__))
import submiter
import store
from util import logger
from solution import evolution
from solution.individual import Individual
from solution.cluster import Cluster
from solution.constraints import CLUSTER_MAX_DEFAULT, INDIVISUAL_MAX, MUTATE_RATE, INITIALIZE_INDIVIDUAL_MAX_DEFAULT

STATE_LOOP_HEAD = 0
STATE_INDIVIDUAL_SELECT = 1
STATE_EVALUATION = 2
STATE_EVOLVE = 3
STATE_LOOP_TAIL = 4

def solve(dep, num, work_num, weight_num, loop_max, is_debug):
    """解実行

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        work_num (int): ワーク数
        weight_num (int): SCIP重み数
        loop_max (int): ループ数
        is_debug (bool): デバッグフラグ
    """
    loaded_data = store.load(dep, num)
    
    if loaded_data is None: # データがない場合
        state = STATE_LOOP_TAIL
        count = 1
        cluster = Cluster(
            plot_max=Individual.get_plot_max(work_num, weight_num),
            cluster_max=CLUSTER_MAX_DEFAULT,
            cluster_loop_max=1)
        individual_list = [Individual(work_num=work_num, weight_num=weight_num) for _ in range(INITIALIZE_INDIVIDUAL_MAX_DEFAULT)]
        selected_individual_list = []
        evaluation_list = []
        ban_generation_list = []
    else: # データが存在している
        state = loaded_data[store.STATE_KEY]
        count = loaded_data[store.COUNT_KEY]
        cluster = loaded_data[store.CLUSTER_KEY]
        individual_list = loaded_data[store.INDIVIDUAL_LIST_KEY]
        selected_individual_list = loaded_data[store.SELECTED_INDIVIDUAL_LIST_KEY]
        evaluation_list = loaded_data[store.EVALUATION_LIST]
        ban_generation_list = loaded_data[store.BAN_GENERATE_LIST]
        logger.info(f"[system restarted]")
    
    while(count <= loop_max):
        if state == STATE_LOOP_TAIL:
            logger.info(f"==========第{count}回目==========")
            state = STATE_LOOP_HEAD
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list, ban_generation_list)
        if state == STATE_LOOP_HEAD:
            # 解選択フェーズ
            cluster.generate(individual_list)
            selected_individual_list = cluster.get_random_individual_list(
                solve_num=INDIVISUAL_MAX
            )
            logger.info(f"[seleted individual List]")
            for individual in selected_individual_list:
                logger.info(f'{hex(id(individual))} -> [select] schedule:{individual.get_schedule_list()} weight:{individual.get_weight_list()}')
            state = STATE_INDIVIDUAL_SELECT
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list, ban_generation_list)
        if state == STATE_INDIVIDUAL_SELECT:
            # 解評価フェーズ
            evaluation_list = submiter.submit(dep, num, selected_individual_list, is_debug)
            for evaluation in evaluation_list: 
                logger.info(f"submit result: {evaluation}")
                ban_generation_list.append(Individual.create_individual_id(
                    evaluation[submiter.ANS_KEY][submiter.INPUT_FORMAT_SCHEDULE_KEY],
                    evaluation[submiter.ANS_KEY][submiter.INPUT_FORMAT_WEIGHT_KEY]
                ))
            state = STATE_EVALUATION
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list, ban_generation_list)
        if state == STATE_EVALUATION:
            # 解改善フェーズ
            individual_list = []
            objective_max = max([evaluation[submiter.EVAL_KEY][submiter.OUTPUT_FORMAT_OBJECTIVE_KEY] for evaluation in evaluation_list])
            for _ in range(len(evaluation_list)):
                # 交叉
                if random.random() > MUTATE_RATE:
                    selected_weight =  [objective_max / evaluation[submiter.EVAL_KEY][submiter.OUTPUT_FORMAT_OBJECTIVE_KEY] for evaluation in evaluation_list]
                    individual_index_list = [i for i in range(len(evaluation_list))]
                    individual1_i = random.choices(individual_index_list, k = 1, weights = selected_weight)[0]
                    selected_weight[individual1_i] = 0
                    individual2_i = random.choices(individual_index_list, k = 1, weights = selected_weight)[0]
                    new_individual = evolution.crossover(
                        Individual(evaluation_list[individual1_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_SCHEDULE_KEY],
                            evaluation_list[individual1_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_WEIGHT_KEY]),
                        Individual(evaluation_list[individual2_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_SCHEDULE_KEY],
                            evaluation_list[individual2_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_WEIGHT_KEY] )
                    )
                    individual_list.append(new_individual)
                    logger.info(f"[交叉]{hex(id(new_individual))} -> [new] schedule:{new_individual.get_schedule_list()} weight:{new_individual.get_weight_list()}")
                # 突然変異
                else:
                    new_individual = evolution.mutate(work_num, weight_num)
                    individual_list.append(new_individual)
                    logger.info(f"[変異]{hex(id(new_individual))} -> [new] schedule:{new_individual.get_schedule_list()} weight:{new_individual.get_weight_list()}")
            state = STATE_EVOLVE
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list, ban_generation_list)
        if state == STATE_EVOLVE:
            state = STATE_LOOP_TAIL
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list, ban_generation_list)
            count += 1