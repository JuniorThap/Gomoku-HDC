import curses
from mcts import MCTS
from gobanHD import GobanHD

H = W = 13

def board_ui(stdscr, board, mcts, n_simulation):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(100)  # Set timeout to allow periodic updates
    
    current_row, current_col = 0, 0  # Start at the top-left corner
    
    game_end = ''
    # Game loop for input handling
    while True:
        stdscr.clear()  # Clear the screen

        # Draw the board
        ui = '   '
        ui += " ".join(f"{num:2}" for num in range(1, W+1)) + '\n'
        for i in range(H):
            ui += f"{i+1:2} "
            for j in range(W):
                value = board.board[i, j]
                if value == 1:
                    ui += ' ● '  # Black stone
                elif value == -1:
                    ui += ' ○ '  # White stone
                elif i == H // 2 and j == W // 2:
                    ui += ' • '  # Larger dot at the center
                elif value == 0:
                    ui += ' . '  # Empty spot
            
            # No \n in the last line
            if i < H-1:
                ui += '\n'

        # Check game end after update the UI
        if game_end != '':
            print('Gomoku')
            print(ui)
            print(game_end)
            break

        # Highlight the current position with a cursor
        ui_list = ui.split('\n')
        ui_list[current_row + 1] = ui_list[current_row + 1][:current_col * 3 + 3] + '[' + ui_list[current_row + 1][current_col * 3 + 4] + ']' +  ui_list[current_row + 1][current_col * 3 + 6:] # Highlight current cell

        # Render the UI
        stdscr.addstr(f'Gomoku: {"White turn ●" if board.last_turn == -1 else "Black turn ○"}')
        for i, line in enumerate(ui_list):
            stdscr.addstr(i+1, 0, line)

        stdscr.refresh()  # Refresh the screen to show the updated UI
        
        # -1 is black turn (opponent turn) so next is player turn
        if board.last_turn == -1:
            key = stdscr.getch()  # Get user input

            if key == 27:  # Escape key to exit
                break
            elif key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < H - 1:
                current_row += 1
            elif key == curses.KEY_LEFT and current_col > 0:
                current_col -= 1
            elif key == curses.KEY_RIGHT and current_col < W - 1:
                current_col += 1
            elif key == ord('\n'):  # Enter key to place a marker
                if board.board[current_row, current_col] == 0:
                    board.update_board(board.get_position_index((current_row, current_col)))  # Black stone (you can alternate)
                    if board.check_gomoku() != 2:
                        game_end = 'White win'
        # 1 is white turn (player turn) so next is opponent turn
        elif board.last_turn == 1:
            position = mcts.search(board, n_simulation)
            board.update_board(board.get_position_index(position))
            if board.check_gomoku() != 2:
                game_end = 'Black win'

            

def main():
    # Initialize the board and MCTS
    board = GobanHD(H=H, W=W, use_HD=False)
    mcts = MCTS()

    # Start the board and run the interactive UI
    board.start_board()
    curses.wrapper(board_ui, board, mcts, 3)

if __name__ == '__main__':
    main()