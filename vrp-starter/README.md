# VRP Starter (Day1)
CSV を読み込み、今後ルート最適化や地図表示をするための **箱** だけ作りました。

## 使い方（Day1）
1. Python を用意（3.10 以上）
2. 依存を入れる：`pip install -r requirements.txt`
3. 動作確認：`python src/app.py --help`

## 次のステップ（Day2以降）
- `data/` に CSV を入れる
- `src/solver/` に OR-Tools のモデルを追加
- `src/viz/` に地図・ガント表示を追加
