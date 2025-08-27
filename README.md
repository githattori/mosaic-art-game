# mosaic-art-game

モザイクアート＆マインスイーパーのゲームリポ

## Minesweeper

端末上で動作するシンプルなマインスイーパーゲームです。

### 遊び方

```bash
python minesweeper.py [rows] [cols] [mines]
```

`rows` `cols` `mines` はそれぞれ行数、列数、地雷数で、省略時は `8 8 10` になります。

ゲーム中の操作は以下の通りです。

- `r row col` : 指定したマスを開く
- `f row col` : 指定したマスに旗を立てる/外す

### スマホで遊ぶ

スマートフォンのブラウザからも遊べる簡易版を `index.html` として同梱しています。

1. PC 上でリポジトリのルートに移動し、簡易サーバーを起動します。

   ```bash
   python -m http.server
   ```

2. PC と同じネットワークに接続したスマホのブラウザで
   `http://<PCのIPアドレス>:8000/index.html` にアクセスします。

画面中央の「Flag Mode」ボタンで旗モードのオン/オフを切り替え、マスをタップしてプレイできます。

### テストの実行

```bash
pytest
```
