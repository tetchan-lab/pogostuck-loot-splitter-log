"""
Pogostuck Auto-Splitter
=======================
acklog.txt を監視して LiveSplit Server へコマンドを送信する。

【前提条件】
  - LiveSplit に「LiveSplit Server」コンポーネントを追加し起動しておく
      Edit > Layout > + > Control > LiveSplit Server
      デフォルトポート: 16834

【使い方】
  python autosplitter.py          # 通常起動
  python autosplitter.py --test   # テストモード（LiveSplitに送信しない）

【スプリット設定例（LiveSplit の Layout Editor）】
  Segment 1: Floor 1 → 2
  Segment 2: Floor 2 → 3
  Segment 3: Floor 3 → 4
  ...
"""

import socket
import time
import re
import os
import sys

# ===== 設定 =====
LOG_FILE      = r"C:\Program Files (x86)\Steam\steamapps\common\Pogostuck\acklog.txt"
LIVESPLIT_HOST = "localhost"
LIVESPLIT_PORT = 16834
POLL_INTERVAL  = 0.3   # 秒（ポーリング間隔）

# コマンドライン引数
TEST_MODE = "--test" in sys.argv


# ------------------------------------------------------------------ #
#  LiveSplit 通信
# ------------------------------------------------------------------ #
def send_livesplit(command: str) -> None:
    """LiveSplit Server へコマンドを送信する"""
    if TEST_MODE:
        print(f"  [TEST] LiveSplit: [{command}]")
        return
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((LIVESPLIT_HOST, LIVESPLIT_PORT))
            s.sendall((command + "\r\n").encode())
            print(f"  → LiveSplit: [{command}]")
    except ConnectionRefusedError:
        print("  ✗ LiveSplit に接続できません。LiveSplit Server が起動しているか確認してください。")
    except Exception as e:
        print(f"  ✗ 送信エラー: {e}")


# ------------------------------------------------------------------ #
#  ログ監視メインループ
# ------------------------------------------------------------------ #
def monitor() -> None:
    current_seed: str | None = None   # 現在のランのシード値
    current_lvl:  int        = -1     # 現在の内部フロアインデックス
    last_pos:     int        = 0      # 前回読み込んだファイルの末尾位置

    print("=" * 45)
    print("  Pogostuck Auto-Splitter")
    if TEST_MODE:
        print("  ★ テストモード（LiveSplitへの送信なし）")
    print("=" * 45)
    print(f"ログファイル : {LOG_FILE}")
    print(f"LiveSplit    : {LIVESPLIT_HOST}:{LIVESPLIT_PORT}")
    print("監視開始... (Ctrl+C で終了)\n")

    while True:
        try:
            # ファイルが存在しない場合（ゲーム未起動）は待機
            if not os.path.exists(LOG_FILE):
                time.sleep(POLL_INTERVAL)
                continue

            stat = os.stat(LOG_FILE)

            # ファイルが縮小した場合 → ゲームが再起動して新しいログになった
            if stat.st_size < last_pos:
                print("[ゲーム再起動を検知 → 状態リセット]")
                last_pos     = 0
                current_seed = None
                current_lvl  = -1

            # 新しい内容がある場合のみ読み込む
            if stat.st_size > last_pos:
                with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                    f.seek(last_pos)
                    chunk = f.read()
                last_pos = stat.st_size

                # ---------------------------------------------------
                # パターン1: シード更新 → 新しいランの開始 / リセット
                #   "dungeonSetInitialSeed(1) at frame XXX -> lvl(0) seed(XXXXX)"
                # ---------------------------------------------------
                for m in re.finditer(
                    r"dungeonSetInitialSeed\(1\) at frame \d+ -> lvl\(0\) seed\((\d+)\)",
                    chunk
                ):
                    new_seed = m.group(1)
                    if new_seed != current_seed:
                        current_seed = new_seed
                        current_lvl  = 0       # Floor 1（lvl=0）にいる状態
                        print(f"\n[新ラン検知] seed={new_seed}")
                        send_livesplit("reset")
                        time.sleep(0.05)
                        send_livesplit("starttimer")

                # ---------------------------------------------------
                # パターン2: フロア遷移 → スプリット
                #   "dungeon generation at frame XXX: lvl(N)"
                #   lvl が 0: Floor 1, 1: Floor 2, 2: Floor 3 ...
                # ---------------------------------------------------
                for m in re.finditer(
                    r"dungeon generation at frame \d+: lvl\((\d+)\)",
                    chunk
                ):
                    lvl = int(m.group(1))
                    # current_lvl より大きい AND タイマーが走っているラン中のみ
                    if lvl > current_lvl and current_seed is not None:
                        prev_lvl    = current_lvl
                        current_lvl = lvl
                        print(f"\n[Floor {prev_lvl + 1} → Floor {lvl + 1}] → split")
                        send_livesplit("split")

        except Exception as e:
            print(f"エラー: {e}")

        time.sleep(POLL_INTERVAL)


# ------------------------------------------------------------------ #
#  エントリーポイント
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n終了しました。")
        sys.exit(0)
