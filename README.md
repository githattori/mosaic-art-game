# mosaic-art-game

モザイクアート＆マインスイーパーのゲームリポ

## Minesweeper

端末上で動作するシンプルなマインスイーパーゲームです。

### 環境構築

Python 3.10 以降が必要です。未インストールの場合は [Python公式サイト](https://www.python.org/downloads/) などから入手してください。依存パッケージは `requirements.txt` に記載されています。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Python をインストールしたくない場合は Docker イメージで実行できます。

```bash
docker build -t minesweeper .
docker run -it --rm minesweeper
```

スマホ向けの `index.html` を配信したい場合は次のようにします。

```bash
docker run -it --rm -p 8000:8000 minesweeper python -m http.server
```

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

行数と列数を入力して「Start」を押すと、そのサイズに対しておよそ 15% の地雷数で盤面が生成されます。
画面中央の「Flag Mode」ボタンで旗モードのオン/オフを切り替え、マスをタップしてプレイできます。

### テストの実行

```bash
pytest
```
