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

### 提出先サーバへのI/Oフォーマット

#### 単目的

##### 入力フォーマット

|キー|型|説明|
|:---:|:---:|:---|
|`schedule`|`list[int]`|各作業（取り付け・取り外し）の日付割り当て（[ワーク1取り付け日, ワーク1取り外し日, ワーク2取り付け日, ワーク2取り外し日, …]）|
|`timeout`|`int`|サーバーでの計算時間（s）|

ex.
```json
{
	"schedule": [1, 1, 2, 3, 2, 2,...],
	"timeout": 600
}
```

##### 出力フォーマット

|キー|型|説明|
|:---:|:---:|:---|
|`objective`|`float`|評価値（目的関数値）|
|`constraint`|`null`|未使用|
|`error`|`str`|エラーが発生した場合のエラー文．入力された解のフォーマットに問題がある場合などに表示される．|
|`info`|`dict[str, union[float, list[float]]]	`|・`exe_time: float`<br>評価値の計算にかかった時間（サーバーのSCIPでの計算時間）<br> `delays: list[float]`<br>各ワークの納期違反量のリスト．納期までに作業が終わったワークは0.0となる．|

ex.
```
{
	"objective": 1550.5,
	"constraint": null,
	"error": "エラー文",
	"info": {
		"exe_time": 503.223,
		"delays": [0.0, 0.0, 30.5, 14.5,...]
	}
}
```

#### 多目的
|キー| 型|説明|
|:---:|:---:|:---|

