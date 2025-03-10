import sys
from MoveGenerator import MoveGenerator
from Board import Board
from utils import parse_board


def main():
    turn, piece_list = parse_board()

    current_board = Board()
    current_board.turn = turn
    for piece in piece_list:
        current_board.add_piece(piece)
    current_board.meta_line = sys.stdin.readline().strip()

    successors = MoveGenerator.generate_successor_boards(current_board)

    # # For debugging
    # for idx, board in enumerate(successors):
    #     print(f"=== Successor {idx} ===")
    #     print(f"Move: {board.last_move}")
    #     print(board)
    #     print("\n")

    for idx, board in enumerate(successors):
        filename = f"board.{idx:03d}"
        with open(filename, "w") as f:

            meta_parts = turn.split()
            meta_parts[0] = MoveGenerator.flip_turn(meta_parts[0])
            f.write(" ".join(meta_parts) + "\n")
            f.write("{\n")
            for pos in sorted(board.pieces.keys()):
                piece = board.pieces[pos]
                f.write(f"  {pos}: '{piece.color}{piece.__class__.__name__[0]}',\n")
            f.write("}\n")

            f.write("0\n0\n0\n")
