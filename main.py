from Board import Board
from utils import load_board_from_file
from AI import AI

if __name__ == "__main__":
    turn, used_time, total_time, move_number, piece_list = load_board_from_file("board")

    # Create the current board and add all pieces.
    current_board = Board()
    current_board.turn = turn
    for piece in piece_list:
        current_board.add_piece(piece)

    remaining_time = int(total_time) - int(used_time)

    ai = AI(ai_color=turn, remaining_time=remaining_time, move_count=int(move_number))

    # Call the AI to choose the best move from the current board.
    best_move_board = ai.choose_best_move(current_board)
    print(best_move_board)




