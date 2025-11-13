import random


class Board_Information:
    def __init__(self, has_been_clicked=False, is_mine=False, is_flag=False):
        self.clicked = has_been_clicked
        self.is_mine = is_mine
        self.flag = is_flag


def create_board(level):
    # 隨機創造地圖並埋地雷
    if (level == 1):
        rows, cols, mine = 9, 9, 10
    if (level == 2):
        rows, cols, mine = 16, 16, 40
    if (level == 3):
        rows, cols, mine = 16, 30, 99
    matrix = [[Board_Information() for _ in range(cols)] for _ in range(rows)]
    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    mined_positions = random.sample(all_positions, mine)
    for r, c in mined_positions:
        matrix[r][c].is_mine = True

    return matrix, rows, cols, mine


def introduction():
    print("=" * 30)
    print("歡迎來到《採地雷遊戲》!")
    print("=" * 30)
    print("遊戲目標：翻開所有安全的格子，不要踩到地雷。")

    print("\n【操作與顯示說明】")
    # 說明操作模式
    print("請依序輸入列與行的編號，例如：「1 2」表示第1列第2行。")
    print("  - 輸入 'flag' 切換到插旗模式。")
    print("  - 輸入 'dig' 切換到挖掘模式。")
    print("  - 輸入 'restart' 重新開始新遊戲。")

    # 說明顯示符號
    print("\n【顯示符號】")
    print("  □ = 未翻開")
    print("  🚩 = 旗幟")
    print("  數字 = 周圍地雷數 (1~8)")
    print("  * = 地雷（遊戲結束）\n")
    return

def show_board(board, revealed, flag_board, rows, cols):
 # 顯示欄位編號
 print("\n    ", end="")
 for c in range(cols):
     print(f"{c+1:2}", end=" ")      # 玩家視角 1-based
 print("\n   " + "---" * cols)

 # 顯示每一列
 for r in range(rows):
     print(f"{r+1:2} |", end="")     # 行數顯示 (1-based)

     for c in range(cols):
         if flag_board[r][c]:
             ch = "🚩"               # 插旗
         elif revealed[r][c]:
             val = board[r][c]
             if val == -1:
                 ch = "*"           # 地雷
             elif val == 0:
                 ch = " "            # 空格
             else:
                 ch = str(val)       # 1~8 數字
         else:
             ch = "□"                # 未翻格

         print(f" {ch}", end="")

     print(" |")                     # 每行右邊框

 print("   " + "---" * cols + "\n")  # 底線


# 以上由謝杰叡負責


def choose_difficulty():
    # 選擇難度
    while (True):
        level = input("請選擇難度:")
        if (level != 1 or level != 2 or level != 3):
            print("請重新輸入")
            continue
        return level


def get_player_input():
    # 取得玩家輸入
    return


def reveal_cell(board, revealed, r, c):
    # 翻開格子：踩雷、顯示數字、展開空白
    # 踩到雷交給外面判斷

    # 計算周圍地雷

    # 自動展開空白格（遞迴）
    return


def game_loop():
    # 選難度
    level = choose_difficulty()
    # 根據難度設計棋盤
    matrix, rows, cols, mine = create_board(level)
    # 輸入指令
    while (True):
        command = input("輸入指令")
        if (command != "F" or command != "R" or command != "C"):
            print("重新輸入")
            continue
        while (True):
            row_pos = input("輸入ROW")
            if (row_pos > matrix.row):
                print("重新輸入")
                continue
        while (True):
            col_pos = input("輸入COL")
            if (col_pos > matrix.col):
                print("重新輸入")
                continue
    # 翻格子

    # 判斷勝利與否

# 以上由黃郁晟負責


def main():
    introduction()
    game_loop()


if __name__ == "__main__":
    main()