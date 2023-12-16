#
# 処理の大枠定義用
#
import datetime
import logging
from os import path
import sys
sys.path.append(path.dirname(__file__))
import submiter
import single_solver
import multi_solver
import store
from util import path_util
from util import logger

def init(dep, num, rootpath, is_debug, is_store):
    """初期化

    Args:
        dep (string): 問題部門
        num (int): 問題番号
        rootpath (string): プロジェクトのルートパス
        is_debug (bool): デバッグモードか
        is_store (bool): データ保持するか
    """
    path_util.init(rootpath)
    if is_debug:
        logger.init()
    else:
        logger.init(path.join(path_util.PATH_MAP["data/app-log"], dep+str(num)), logging.INFO)
    store.init(is_store)
    
    logger.info(f"[program start] {datetime.datetime.now()}")
    
def run(dep, num):
    """メイン実行

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    """
    submit_max = submiter.get_submit_max(dep, num)
    work_num = submiter.get_work_num(dep, num)
    weight_num = submiter.get_weight_num()
        
    if dep == submiter.SOLVE_SINGLE_ID :
        single_solver.solve(
            dep,
            num,
            work_num,
            submit_max
        )
    elif dep == submiter.SOLVE_MULTI_ID :
        multi_solver.solve(
            dep,
            num,
            work_num,
            weight_num,
            submit_max
        )

def terminate():
    """終了時
    """
    logger.info(f"[program end] {datetime.datetime.now()}")
    sys.exit(0)