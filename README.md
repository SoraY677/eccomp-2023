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
python main.py {single or multi} {question-num}
# {single or multi}: single=単目的 / multi=多目的
# {quesition-num}: 0=練習問題(default) / 1~=本番問題

## 使用方法
### 単目的
python main.py single   # 練習問題
python main.py single 1 # 本番問題-1
python main.py single 2 # 本番問題-2
### 多目的
python main.py multi    # 練習問題
python main.py multi 1  # 本番問題-1

# -------------------------------------------------

# パッケージ出力
pip freeze > requirements.txt

```

