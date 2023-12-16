import os
import click
import src.process as process
import src.submiter as submiter

@click.command()
@click.option('--dep', type=click.Choice([submiter.SOLVE_SINGLE_ID, submiter.SOLVE_MULTI_ID]), help='部門選択', prompt='部門選択')
@click.option('--num', type=int, help='番号選択(`0`:練習|`1`以上:本番)', default=0)
@click.option('--debug', type=bool, help='デバッグモード(`True`:デバッグモード|`False`:本番モード)', default=True)
@click.option('--store', type=bool, help='データ保持スイッチ(`True`:ON|`False`:OFF)', default=True)
def main(dep, num, debug, store):
    """メイン処理

    Args:
        dep (string): 部門
        num (string): int
    """
    process.init(dep, num, os.getcwd(), debug, store)
    process.run(dep, num)
    process.terminate()

if __name__ == '__main__':
    main()