#
# 処理の大枠定義用
#
import datetime
from util import path_util
from util import logger
if __name__ == "__main__":
    import submiter
    import solver
    import result_repository
else:
    from . import submiter
    from . import solver
    from . import result_repository
import sys

def init(rootpath):
    """初期化

    Args:
        rootpath (string): プロジェクトのルートパス
    """
    path_util.init(rootpath)
    logger.init()
    
    logger.info(f"[program start] {datetime.datetime.now()}")
    
def run(dep, num):
    """メイン実行

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    """
    submit_max = submiter.get_submit_max(dep, num)
    prev_result_dict = result_repository.get_result_file_path_list_order_by_count_desc(dep, num, 0)
        
    for i in range(submit_max):
        count = i+1
        logger.info(f"==========第{count}回目==========")
        # 解算出
        if dep == submiter.SOLVE_SINGLE_ID :
            ans = solver.solve_single()
        elif dep == submiter.SOLVE_MULTI_ID :
            ans = solver.solve_multi()
        # 解提出
        response = submiter.submit(dep, num, ans)
        result_dict = result_repository.create_result_dict(count, ans, response)
        result_repository.save(dep, num, count, result_dict)
        prev_result_dict = result_dict
        logger.info(f"============================")

def terminate():
    """終了時
    """
    logger.info(f"[program end] {datetime.datetime.now()}")
    sys.exit(0)