# Pogostuck Loot Mode Auto-Splitter (Log-based)

[English version available here → README.en.md](./README.en.md)

LiveSplitと連動して、Pogostuck の **Loot Mode（ルートモード）** のフロア進行を自動でスプリットするツールです。

ゲームのログファイル（`acklog.txt`）を監視する方式のため、**画面キャプチャ不要・OCR不要**で動作します。

---

## 特徴

- OCRや画面キャプチャを使わないため**動作が軽い**
- ゲームエンジンのログを直接読むため**誤検知がない**
- **追加ライブラリのインストール不要**（Python標準ライブラリのみ使用）
- フロアをクリアするたびに自動でスプリット
- 新しいランを開始（リセット）すると自動でタイマーリセット＆再スタート

---

## 必要なもの

| ソフトウェア | 入手先 |
|---|---|
| Python 3.10 以上 | https://www.python.org/downloads/ |
| LiveSplit | https://livesplit.org/ |
| Pogostuck（起動オプション設定が必要） | Steam |

---

## ダウンロード方法

### Git を使わない場合（推奨）

1. このページ右上の緑色の **`Code`** ボタンをクリック
2. **`Download ZIP`** を選択してダウンロード
3. ZIPを解凍して好きな場所に置く（例: `C:\tools\pogostuck-loot-splitter-log\`）

### Git を使う場合

```
git clone https://github.com/tetchan-lab/pogostuck-loot-splitter-log.git
```

---

## Python のインストール方法

### 1. Python をダウンロードする

1. https://www.python.org/downloads/ を開く
2. **`Download Python 3.x.x`** ボタンをクリックしてインストーラーをダウンロード

### 2. インストールする

1. ダウンロードした `.exe` ファイルを実行する
2. **⚠️ 重要：** インストール画面の一番下にある **`Add python.exe to PATH`** にチェックを入れる
3. **`Install Now`** をクリックしてインストール完了

> `Add python.exe to PATH` のチェックを忘れると、後述の `start_autosplitter.bat` が動作しません。チェックを忘れた場合はインストーラーを再実行して `Modify` → `Next` → `Add Python to environment variables` にチェックを入れてください。

### 3. インストールの確認

インストール後、スタートメニューで「PowerShell」を検索して開き、以下を入力します：

```
python --version
```

`Python 3.x.x` と表示されればインストール成功です。

---

## セットアップ手順

### 1. Pogostuck の起動オプションを設定する

Steam ライブラリで Pogostuck を右クリック →「プロパティ」→「起動オプション」に以下を入力します：

```
-diag
```

> `-diag` オプションを付けることで `acklog.txt` にログが出力されます。これがないと動作しません。

### 2. LiveSplit の設定

LiveSplit には TCP Server 機能が標準搭載されています。以下のいずれかの方法で起動してください。

**毎回手動で起動する場合：**
1. LiveSplit を起動する
2. 画面を右クリック → `Control` → `Start TCP Server` を選択する

**自動起動に設定する場合（推奨）：**
1. LiveSplit を右クリック → `Settings` を開く
2. `Startup Behavior` の項目で `Start TCP Server` を選択する
3. 以降は LiveSplit 起動時に自動で TCP Server が立ち上がる

> ポートはデフォルトの `16834` のままで問題ありません。

### 3. LiveSplit のスプリット設定

「Edit Splits」でフロアごとにセグメントを作成します。

| セグメント名（例） | タイミング |
|---|---|
| Floor 1 | Level 1 クリア時 |
| Floor 2 | Level 2 クリア時 |
| Floor 3 | Level 3 クリア時 |
| ...（必要な数だけ） | |

### 4. スクリプトを起動する

`start_autosplitter.bat` をダブルクリックします。

```
ゲーム起動 → Loot Mode 選択 → 自動でタイマースタート！
```

---

## ファイル構成

```
pogostuck-loot-splitter-log/
├── autosplitter.py              # メインスクリプト
├── start_autosplitter.bat       # 通常起動（これをダブルクリック）
├── start_autosplitter_test.bat  # テストモード（LiveSplitに送信しない）
└── README.md                    # このファイル
```

---

## テストモードについて

`start_autosplitter_test.bat` を起動すると、LiveSplitへの実際の送信は行わずにコンソールへの出力だけ行います。動作確認やトラブルシューティングに使えます。

```
[新ラン検知] seed=7877
  [TEST] LiveSplit: [reset]
  [TEST] LiveSplit: [starttimer]

[Floor 1 → Floor 2] → split
  [TEST] LiveSplit: [split]
```

---

## 動作の仕組み

ゲームのログファイル `acklog.txt` を0.3秒ごとに監視し、以下のパターンを検知します。

| 検知内容 | LiveSplitへの送信 |
|---|---|
| 新しいランが始まった（シード値が更新された） | `reset` → `starttimer` |
| 次のフロアに進んだ | `split` |
| ゲームを再起動した | 内部状態をリセット（次のラン開始を待機） |

---

## トラブルシューティング

**タイマーが動かない**
- LiveSplit Server が起動しているか確認してください（「Start Server」ボタンを押す）
- Pogostuck の起動オプションに `-diag` が入っているか確認してください

**フロアをクリアしてもスプリットされない**
- `start_autosplitter_test.bat` でテストモードを起動し、コンソールに `[Floor N → Floor N+1]` の表示が出るか確認してください

**`acklog.txt が見つかりません` のようなエラーが出る**
- Pogostuck を一度起動してから本スクリプトを起動してください

---

## 関連プロジェクト

- [pogostuck-loot-splitter-ocr](https://github.com/tetchan-lab/pogostuck-loot-splitter-ocr) — OCR（画面キャプチャ）を使ったバージョン。スコア表示にも対応

---

## ライセンス

MIT License
