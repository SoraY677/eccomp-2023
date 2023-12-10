#
# 単目的用ソルバ
#
from util import logger
from solution.population import Population
from solution.cluster import Cluster
from solution.constraints import CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT
if __name__ == "__main__":
    import submiter
    import result_repository
else:
    from . import submiter
    from . import result_repository

def solve(dep, num, work_num, loop_max):
    population = Population(work_num)
    cluster = Cluster(CLUSTER_MAX_DEFAULT, CLUSTER_LOOP_MAX_DEFAULT)
    
    for i in range(loop_max):
        count = i+1
        logger.info(f"==========第{count}回目==========")
        
        cluster.generate_cluster(population.get_individual_list())
        
        # 解提出
        ans = submiter.create_ans(dep, [])
        response = submiter.submit(dep, num, ans)
        # 解の保存
        result_dict = result_repository.create_result_dict(count, ans, response)
        result_repository.save(dep, num, count, result_dict)