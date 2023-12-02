import os
import click
import src.process as process
import src.submiter as submiter

@click.command()
@click.option('--dep', prompt=f'部門選択(`{submiter.SOLVE_SINGLE_ID}`:単目的|{submiter.SOLVE_MULTI_ID}:多目的)', type=click.Choice([submiter.SOLVE_SINGLE_ID, submiter.SOLVE_MULTI_ID], case_sensitive=False))
@click.option('--num', help='番号選択(`0`:練習|`1`以上:本番)', type=int, default=0)
def main(dep, num):
    """メイン処理

    Args:
        dep (string): 部門
        num (string): int
    """
    process.init(os.getcwd())
    process.run(dep, num)
    process.terminate()

if __name__ == '__main__':
    main()