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

    for idx, board in enumerate(successors):
        filename = f"board.{idx:03d}"
        with open(filename, "w") as f:
            # Set the first line: flipped turn followed by "0 6000 0" (or "0 0 0" if that's what you require)
            flipped_turn = MoveGenerator.flip_turn(turn)
            f.write(f"{flipped_turn} 0 6000 0\n")

            # Write the board state inside braces.
            f.write("{\n")
            for pos in sorted(board.pieces.keys()):
                piece = board.pieces[pos]
                # Use "N" for Knight, otherwise use the first character of the class name.
                symbol = "N" if piece.__class__.__name__ == "Knight" else piece.__class__.__name__[0]
                f.write(f"  {pos}: '{piece.color}{symbol}',\n")
            f.write("}\n")

            # Write the final three reserved lines, always "0"
            f.write("0\n0\n0\n")