import sys
from MoveGenerator import MoveGenerator
from Board import Board
from utils import parse_board


def main():
    turn, piece_list = parse_board()

    # Create the current board and add all pieces.
    current_board = Board()
    current_board.turn = turn
    for piece in piece_list:
        current_board.add_piece(piece)
    current_board.meta_line = sys.stdin.readline().strip()

    # Generate all legal successor boards.
    successors = MoveGenerator.generate_successor_boards(current_board)

    # # For debugging
    # for idx, board in enumerate(successors):
    #     print(f"=== Successor {idx} ===")
    #     print(f"Move: {board.last_move}")
    #     print(board)
    #     print("\n")

    # Write each successor board to a file named board.000, board.001, etc.
    for idx, board in enumerate(successors):
        filename = f"board.{idx:03d}"
        with open(filename, "w") as f:
            # Assuming meta_line is the first line of input.
            # Here, simply write the turn flipped plus reserved numbers as needed.
            meta_parts = turn.split()  # adjust accordingly if you stored meta_line differently.
            meta_parts[0] = MoveGenerator.flip_turn(meta_parts[0])
            f.write(" ".join(meta_parts) + "\n")
            f.write("{\n")
            for pos in sorted(board.pieces.keys()):
                piece = board.pieces[pos]
                f.write(f"  {pos}: '{piece.color}{piece.__class__.__name__[0]}',\n")
            f.write("}\n")
            # Write the final 3 reserved lines (assuming they are known).
            f.write("0\n0\n0\n")