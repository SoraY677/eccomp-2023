#
# 処理の大枠定義用
#
import datetime
from .util import filepath
from .util import logger
from . import submiter
from . import solver
import sys

def init(rootpath):
    """初期化

    Args:
        rootpath (string): プロジェクトのルートパス
    """
    filepath.init(rootpath)
    logger.init()
    
    logger.info(f"[program start] {datetime.datetime.now()}")
    
def run(dep, num):
    """メイン実行

    Args:
        dep (string): 問題部門
        num (int): 問題番号
    """
    if dep == submiter.SOLVE_SINGLE_ID :
        ans = solver.solve_single()
    elif dep == submiter.SOLVE_MULTI_ID :
        ans = solver.solve_multi()
    else:
        logger.error(f"部門選択に存在しないものが選ばれました: selected '{dep}' not in [{submiter.SOLVE_SINGLE_ID}| {submiter.SOLVE_MULTI_ID}]")
    
    submiter.submit(dep, num, ans)

def terminate():
    """終了時
    """
    logger.info(f"[program end] {datetime.datetime.now()}")
    sys.exit(0)