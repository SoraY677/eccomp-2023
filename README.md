<div align=center>

# 2023 🧭進化計算コンペティション

参加者[SoraY677](https://github.com/SoraY677/)のリゾルバ

---

公式サイト：https://ec-comp.jpnsec.org/ja

</div>

## 📰問題一覧

- 単目的部門
  - [練習問題](https://ec-comp.jpnsec.org/ja/matches/93)
  - [本番問題-1](https://ec-comp.jpnsec.org/ja/matches/94)
  - [本番問題-2](https://ec-comp.jpnsec.org/ja/matches/95)
- 多目的部門
  - [練習問題](https://ec-comp.jpnsec.org/ja/matches/96)
  - [本番問題-1](https://ec-comp.jpnsec.org/ja/matches/97)

## 🔧開発方法

### 環境

- [python v3.11.6](https://www.python.org/downloads/)

### コマンド

```bash
# パッケージインストール
pip install -r requirements.txt

# -------------------------------------------------

# 解提出
python main.py {option}

## 使用方法
python main.py         # 練習問題
python main.py --num {1...} # 本番問題-{num}
# -> その後CLI上で単目的/多目的の選択

# -------------------------------------------------

# パッケージ出力
pip freeze > requirements.txt

```