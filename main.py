import sys
from MoveGenerator import MoveGenerator
from Board import Board
from utils import parse_board, print_board
from AI import AI


def main():
    turn, piece_list = parse_board()
    ai = AI()

    # Create the current board and add all pieces.
    current_board = Board()
    current_board.turn = turn
    for piece in piece_list:
        current_board.add_piece(piece)
    current_board.meta_line = sys.stdin.readline().strip()


    # Call the AI to choose the best move from the current board.
    best_move_board = ai.choose_best_move(current_board)
    print_board(best_move_board,turn)





