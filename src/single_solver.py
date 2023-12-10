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

def solve(dep, num, work_num, loop_max):
    loaded_data = store.load(dep, num)
    
    if loaded_data is None: # データがない場合
        count = 1
        cluster = Cluster(CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT)
        individual_list = [Individual(work_num) for _ in range(INITIALIZE_INDIVIDUAL_MAX_DEFAULT)]
    else: # データが存在している
        count = loaded_data[store.COUNT_KEY]
        cluster = loaded_data[store.CLUSTER_KEY]
        individual_list = loaded_data[store.SELECTED_INDIVIDUAL_LIST]
        
    print(count)
    
    while(count <= loop_max):
        logger.info(f"==========第{count}回目==========")
        
        # import sys
        # sys.exit(1)
        
        # 解生成フェーズ
        cluster.generate(individual_list)
        selected_individual_list = cluster.get_separated_individual_list(
            solve_num=INDIVISUAL_MAX
        )
        store.save(dep, num, count, cluster, selected_individual_list)
        logger.info(f"[seleted individual List]")
        for individual in selected_individual_list:
            logger.info(f'{hex(id(individual))}:{individual.get_schedule() }')
        
        # 解評価フェーズ
        evaluation_list = []
        objective_list = []
        for individual in selected_individual_list:
            ans = submiter.create_ans(dep, individual.get_schedule())
            response = submiter.submit(dep, num, ans)
            logger.info(f"{hex(id(individual))} -> response: {response}")
            # 解の保存
            
            
            objective = response["objective"]
            evaluation_list.append({
                "individual": individual,
                "objective": objective
            })
            objective_list.append(objective)
        
        # 解改善フェーズ
        individual_list = []
        objective_max = max(objective_list)
        for individual in range(len(selected_individual_list)):
            # 交叉
            if random.random() > MUTATE_RATE:
                selected_weight =  [objective_max / item["objective"] for item in evaluation_list]
                individual_index_list = [i for i in range(len(selected_weight))]
                individual1_i = random.choices(individual_index_list, k = 1, weights = selected_weight)[0]
                selected_weight[individual1_i] = 0
                individual2_i = random.choices(individual_index_list, k = 1, weights = selected_weight)[0]
                new_individual = evolution.crossover(
                    selected_individual_list[individual1_i],
                    selected_individual_list[individual2_i]
                )
                individual_list.append(new_individual)
                logger.info(f"[交叉]{hex(id(new_individual))} -> new: {new_individual.get_schedule()}")
            # 突然変異
            else:
                new_individual = evolution.mutate(work_num)
                individual_list.append(new_individual)
                logger.info(f"[変異]{hex(id(new_individual))} -> new:: {new_individual.get_schedule()}")
                
        count += 1