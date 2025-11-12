import random
from collections import deque

ROWS, COLS = 5, 5
NUM_MINES = 3

def create_board(rows, cols, num_mines):
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_positions = set(random.sample(range(rows*cols), num_mines))
    for idx in mine_positions:
        r, c = divmod(idx, cols)
        board[r][c] = -1
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == -1:
                continue
            count = 0
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r+dr, c+dc
                    if 0<=nr<rows and 0<=nc<cols and board[nr][nc]==-1:
                        count += 1
            board[r][c] = count
    return board

def print_hidden_board():
    hidden_board = [["格" for _ in range(COLS)] for _ in range(ROWS)]
    for row in hidden_board:
        print(row)
    print()

def print_board_list(board, revealed, flag_board):
    display_board = []
    for r in range(ROWS):
        row_display = []
        for c in range(COLS):
            if revealed[r][c]:
                if board[r][c] == -1:
                    row_display.append("雷")
                else:
                    row_display.append(board[r][c])
            elif flag_board[r][c]:
                row_display.append("🚩")
            else:
                row_display.append("格")
        display_board.append(row_display)
    for row in display_board:
        print(row)
    print()

def reveal(board, revealed, flag_board, x, y):
    col_index = x - 1
    row_index = y - 1

    if revealed[row_index][col_index] or flag_board[row_index][col_index]:
        return False
    
    revealed[row_index][col_index] = True
    
    if board[row_index][col_index] == 0:
        queue = deque()
        queue.append((row_index, col_index))
        while queue:
            r, c = queue.popleft()
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r+dr, c+dc
                    if 0<=nr<ROWS and 0<=nc<COLS and not revealed[nr][nc] and not flag_board[nr][nc]:
                        revealed[nr][nc] = True
                        if board[nr][nc]==0:
                            queue.append((nr,nc))
                            
    return board[row_index][col_index] == -1

def toggle_flag(flag_board, revealed, x, y):
    col_index = x - 1
    row_index = y - 1
    
    if revealed[row_index][col_index]:
        print("不能在已經揭開的格子上插旗。")
    else:
        flag_board[row_index][col_index] = not flag_board[row_index][col_index]

def check_win(board, revealed):
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1 and not revealed[r][c]:
                return False
    return True

def reveal_all_and_print(board, revealed, flag_board):
    """ (新增) 遊戲結束時揭露所有格子並印出 """
    for r in range(ROWS):
        for c in range(COLS):
            revealed[r][c] = True # 揭露所有格子
    print("--- 最終地圖 ---")
    print_board_list(board, revealed, flag_board)

def play_game():
    """ (重大修改) 加入「遊戲結束邏輯」和「重新遊玩」邏輯 """
    
    # 這個 while True 迴圈負責「重新遊玩」
    while True:
        # --- 遊戲初始化 ---
        board = create_board(ROWS, COLS, NUM_MINES)
        revealed = [[False]*COLS for _ in range(ROWS)]
        flag_board = [[False]*COLS for _ in range(ROWS)]
        mode = 'dig'

        print("\n===== 新遊戲開始 =====")
        print_hidden_board()

        game_over = False
        user_restarted = False # (新增) 用來追蹤玩家是否輸入 'restart'
        
        # --- 單局遊戲的迴圈 ---
        while not game_over:
            
            mode_text = '挖掘' if mode == 'dig' else '插旗🚩'
            user_input = input(f"目前模式: {mode_text} | 請輸入(行,列), 'flag', 'dig', 或 'restart': ").strip()

            if user_input.lower() == "restart":
                user_restarted = True # (修改) 標記為 true
                break # 跳出單局遊戲迴圈
            
            if user_input.lower() == 'flag':
                mode = 'flag'
                print("模式切換為：插旗🚩")
                continue
            if user_input.lower() == 'dig':
                mode = 'dig'
                print("模式切換為：挖掘")
                continue
            
            try:
                user_input = user_input.replace("(", "").replace(")", "").replace(" ", "")
                x, y = map(int, user_input.split(","))
                if not (1 <= x <= COLS and 1 <= y <= ROWS):
                    print("輸入超出範圍，請重新輸入")
                    continue
            except:
                print("輸入格式錯誤，請輸入 (行,列)")
                continue

            if mode == 'dig':
                hit_mine = reveal(board, revealed, flag_board, x, y)
                
                # (修改) 只有在遊戲 "未" 結束時才印出進度
                if not hit_mine and not check_win(board, revealed):
                    print_board_list(board, revealed, flag_board)

                if hit_mine:
                    print("你踩到地雷了，遊戲結束！")
                    # (修改) 呼叫新函式來揭露地圖
                    reveal_all_and_print(board, revealed, flag_board)
                    game_over = True
                elif check_win(board, revealed):
                    print("恭喜你，成功翻開所有非地雷格子，勝利！")
                    # (修改) 呼叫新函式來揭露地圖
                    reveal_all_and_print(board, revealed, flag_board)
                    game_over = True
            
            elif mode == 'flag':
                toggle_flag(flag_board, revealed, x, y)
                print_board_list(board, revealed, flag_board)
        
        # --- (新增) 遊戲結束後的詢問邏輯 ---
        
        # 如果玩家是輸入 'restart'，我們就跳過詢問，直接開始新遊戲
        if user_restarted:
            continue

        # 詢問是否要玩下一把
        while True:
            play_again = input("\n是否要開始下一把遊戲？ (yes/no): ").strip().lower()
            if play_again == 'yes':
                break # 跳出 "詢問迴圈"，外層的 "while True" 會繼續執行
            elif play_again == 'no':
                print("感謝遊玩，再見！")
                return # 結束 play_game() 函式，關閉遊戲
            else:
                print("輸入錯誤，請輸入 'yes' 或 'no'")


if __name__ == "__main__":
    play_game()