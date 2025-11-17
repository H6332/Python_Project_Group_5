import random
from collections import deque


class Board_Information:
    def __init__(self, has_been_clicked=False, is_mine=False, is_flag=False):
        self.clicked = has_been_clicked
        self.is_mine = is_mine
        self.flag = is_flag
        self.number = 0  # 周圍地雷數


def create_board(level):
    if level == 1:
        rows, cols, mine = 9, 9, 10
    elif level == 2:
        rows, cols, mine = 16, 16, 40
    elif level == 3:
        rows, cols, mine = 16, 30, 99

    matrix = [[Board_Information() for _ in range(cols)] for _ in range(rows)]

    all_positions = [(r, c) for r in range(rows) for c in range(cols)]
    mined_positions = random.sample(all_positions, mine)

    for r, c in mined_positions:
        matrix[r][c].is_mine = True

    return matrix, rows, cols, mine


def introduction():
    print("==== 歡迎來到踩地雷 ====")
    print("O = 翻開格子")
    print("F = 插旗")
    print("U = 拔旗")
    print("R = 重新開始新的一局（隨時可用）")
    print("ROW、COL 從 0 開始計算")
    print("=======================")


def choose_difficulty():
    while True:
        level = input("請選擇難度 (1:初級 2:中級 3:高級): ")
        if level in ("1", "2", "3"):
            return int(level)
        print("輸入錯誤，請重新輸入。")


def count_adjacent_mines(matrix, r, c, rows, cols):
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if matrix[nr][nc].is_mine:
                    count += 1
    return count


def print_board(matrix, rows, cols):
    print("\n   ", end="")
    for c in range(cols):
        print(f"{c:2}", end=" ")
    print()

    for r in range(rows):
        print(f"{r:2} ", end="")
        row_display = []
        for c in range(cols):
            cell = matrix[r][c]
            if cell.flag:
                row_display.append("🚩")
            elif not cell.clicked:
                row_display.append("■")
            else:
                if cell.is_mine:
                    row_display.append("💣")
                else:
                    row_display.append(str(cell.number))
        print(" ".join(row_display))
    print()


def toggle_flag(matrix, r, c):
    cell = matrix[r][c]
    if cell.clicked:
        print("不能在已翻開的格子插旗！")
        return
    cell.flag = True


def unflag(matrix, r, c):
    cell = matrix[r][c]
    if not cell.flag:
        print("這格沒有旗子可以拔。")
        return
    cell.flag = False


def reveal_cell(matrix, rows, cols, r, c):
    cell = matrix[r][c]

    if cell.clicked or cell.flag:
        return False

    cell.clicked = True

    if cell.is_mine:
        return True

    if cell.number == 0:
        queue = deque()
        queue.append((r, c))

        while queue:
            cr, cc = queue.popleft()
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor = matrix[nr][nc]
                        if not neighbor.clicked and not neighbor.flag:
                            neighbor.clicked = True
                            if neighbor.number == 0:
                                queue.append((nr, nc))

    return False


def check_win(matrix, rows, cols, mine_count):
    clicked_count = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c].clicked:
                clicked_count += 1

    return clicked_count == rows * cols - mine_count


# ===============================
#        ⭐ 主遊戲迴圈（含 R 重開）
# ===============================
def game_loop():
    while True:  # ← 整個遊戲（包含重新開始）
        level = choose_difficulty()
        matrix, rows, cols, mine_count = create_board(level)

        # 計算數字
        for r in range(rows):
            for c in range(cols):
                if not matrix[r][c].is_mine:
                    matrix[r][c].number = count_adjacent_mines(
                        matrix, r, c, rows, cols)

        print_board(matrix, rows, cols)

        # ========== 單局遊戲 ==========
        while True:
            print("指令：O(翻開) F(插旗) U(拔旗) R(重開新局)")
            command = input("請輸入指令: ").upper()

            # ⭐ 隨時重新開始
            if command == "R":
                print("\n🔄 正在開始新的一局...\n")
                break  # ← 跳出本局，回到外層 while 開始新局

            if command not in ("O", "F", "U"):
                print("指令錯誤")
                continue

            try:
                r = int(input("ROW: "))
                c = int(input("COL: "))
            except:
                print("輸入錯誤")
                continue

            if not (0 <= r < rows and 0 <= c < cols):
                print("超出地圖範圍")
                continue

            if command == "F":
                toggle_flag(matrix, r, c)

            elif command == "U":
                unflag(matrix, r, c)

            elif command == "O":
                hit_mine = reveal_cell(matrix, rows, cols, r, c)
                if hit_mine:
                    print("💥 你踩到地雷！遊戲結束！")

                    for rr in range(rows):
                        for cc in range(cols):
                            matrix[rr][cc].clicked = True

                    print_board(matrix, rows, cols)
                    break  # ← 跳去詢問是否重玩

            print_board(matrix, rows, cols)

            if check_win(matrix, rows, cols, mine_count):
                print("🎉 恭喜你贏了！")
                break

        # ========== 局結束 → 詢問是否再玩 ==========
        again = input("要再玩一局嗎？(Y/N): ").upper()
        if again != "Y":
            print("感謝遊玩，再見！")
            return


def main():
    introduction()
    game_loop()


if __name__ == "__main__":
    main()
