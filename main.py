import sys
from MoveGenerator import MoveGenerator
from Board import Board
from utils import parse_board, print_board, print_boards
from AI import AI
import time

def main():
    turn, used_time, total_time, move_number, piece_list = parse_board()

    # Create the current board and add all pieces.
    current_board = Board()
    current_board.turn = turn
    for piece in piece_list:
        current_board.add_piece(piece)

    remaining_time = int(total_time) - int(used_time)

    ai = AI(ai_color=turn, remaining_time=remaining_time, move_count=int(move_number))

    # Call the AI to choose the best move from the current board.
    best_move_board = ai.choose_best_move(current_board)
    print_board(best_move_board,turn)


    

