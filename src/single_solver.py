#
# 単目的用ソルバ
#
import random
if __name__ == "__main__":
    import submiter
    import store
    from util import logger
    from solution import evolution
    from solution.individual import Individual
    from solution.cluster import Cluster
    from solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT, INDIVISUAL_MAX, MUTATE_RATE, INITIALIZE_INDIVIDUAL_MAX_DEFAULT
else:
    from src import submiter
    from src import store
    from src.util import logger
    from src.solution import evolution
    from src.solution.individual import Individual
    from src.solution.cluster import Cluster
    from src.solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT, INDIVISUAL_MAX, MUTATE_RATE, INITIALIZE_INDIVIDUAL_MAX_DEFAULT

STATE_LOOP_HEAD = 0
STATE_INDIVIDUAL_SELECT = 1
STATE_EVALUATION = 2
STATE_EVOLVE = 3
STATE_LOOP_TAIL = 4

def solve(dep, num, work_num, loop_max):
    """解実行

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        work_num (int): ワーク数
        loop_max (int): ループ数
    """
    loaded_data = store.load(dep, num)
    
    if loaded_data is None: # データがない場合
        state = STATE_LOOP_TAIL
        count = 1
        cluster = Cluster(CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT)
        individual_list = [Individual(work_num) for _ in range(INITIALIZE_INDIVIDUAL_MAX_DEFAULT)]
        selected_individual_list = []
        evaluation_list = []
    else: # データが存在している
        state = loaded_data[store.STATE_KEY]
        count = loaded_data[store.COUNT_KEY]
        cluster = loaded_data[store.CLUSTER_KEY]
        individual_list = loaded_data[store.INDIVIDUAL_LIST_KEY]
        selected_individual_list = loaded_data[store.SELECTED_INDIVIDUAL_LIST_KEY]
        evaluation_list = loaded_data[store.EVALUATION_LIST]
        logger.info(f"[system restarted]")
    
    while(count <= loop_max):
        if state == STATE_LOOP_TAIL:
            logger.info(f"==========第{count}回目==========")
            state = STATE_LOOP_HEAD
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list)
        if state == STATE_LOOP_HEAD:
            # 解生成フェーズ
            cluster.generate(individual_list)
            selected_individual_list = cluster.get_separated_individual_list(
                solve_num=INDIVISUAL_MAX
            )
            logger.info(f"[seleted individual List]")
            for individual in selected_individual_list:
                logger.info(f'{hex(id(individual))}:{individual.get_schedule() }')
            state = STATE_INDIVIDUAL_SELECT
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list)
        if state == STATE_INDIVIDUAL_SELECT:
            # 解評価フェーズ
            schedule_list = []
            for individual in selected_individual_list:
                schedule_list.append({
                    submiter.INPUT_FORMAT_SCHEDULE_KEY: individual.get_schedule()
                })
            ans_list = submiter.create_ans_list(dep, schedule_list)
            evaluation_list = submiter.submit(dep, num, ans_list)
            logger.info(f"submit result: {evaluation_list}")
            state = STATE_EVALUATION
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list)
        if state == STATE_EVALUATION:
            individual_list = []
            # 解改善フェーズ
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
                        evaluation_list[individual1_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_SCHEDULE_KEY],
                        evaluation_list[individual2_i][submiter.ANS_KEY][submiter.INPUT_FORMAT_SCHEDULE_KEY]
                    )
                    individual_list.append(new_individual)
                    logger.info(f"[交叉]{hex(id(new_individual))} -> new: {new_individual.get_schedule()}")
                # 突然変異
                else:
                    new_individual = evolution.mutate(work_num)
                    individual_list.append(new_individual)
                    logger.info(f"[変異]{hex(id(new_individual))} -> new:: {new_individual.get_schedule()}")
            state = STATE_EVOLVE
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list)
        if state == STATE_EVOLVE:
            state = STATE_LOOP_TAIL
            store.save(dep, num, state, count, cluster, individual_list, selected_individual_list, evaluation_list)
            count += 1