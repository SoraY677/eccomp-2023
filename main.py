import os
import click
import src.process as process
import src.util.logger as logger

@click.command()
@click.option('--dep', prompt='部門選択(`s`:単目的|`m`:多目的)', type=click.Choice(['s', 'm'], case_sensitive=False))
@click.option('--num', help='番号選択(`0`:練習|`1`以上:本番)', type=int, default=0)
def main(dep, num):
    process.init(os.getcwd())
    process.run(dep, num)

if __name__ == '__main__':
    main()