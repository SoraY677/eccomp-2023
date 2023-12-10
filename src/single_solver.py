#
# 単目的用ソルバ
#
import random
if __name__ == "__main__":
    import submiter
    import result_repository
    from util import logger
    from solution import evolution
    from solution.population import Population
    from solution.cluster import Cluster
    from solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT, INDIVISUAL_MAX, MUTATE_RATE
else:
    from src import submiter
    from src import result_repository
    from src.util import logger
    from src.solution import evolution
    from src.solution.population import Population
    from src.solution.cluster import Cluster
    from src.solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT, INDIVISUAL_MAX, MUTATE_RATE

def solve(dep, num, work_num, loop_max):
    population = Population(work_num)
    cluster = Cluster(CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT)
    individual_list = population.get_individual_list()
    
    for i in range(loop_max):
        count = i+1
        logger.info(f"==========第{count}回目==========")
        
        # 解生成フェーズ
        cluster.generate(individual_list)
        selected_individual_list = cluster.get_separated_individual_list(
            solve_num=INDIVISUAL_MAX
        )
        
        # 解評価フェーズ
        evaluation_list = []
        objective_list = []
        for individual in selected_individual_list:
            # 提出用解情報の生成
            ans = submiter.create_ans(dep, individual.get_schedule())
            response = submiter.submit(dep, num, ans)
            # 解の保存
            result_dict = result_repository.create_result_dict(count, ans, response)
            result_repository.save(dep, num, count, result_dict)
            objective = result_dict["objective"]
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
            # 突然変異
            else:
                new_individual = evolution.mutate(work_num)
                individual_list.append(new_individual)