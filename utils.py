from pieces.base import Piece
from pieces import Flinger, Peon, Knight, Cannon, Queen, King, Zombie, Bishop, Rook

# Map piece letters to piece classes
PIECE_MAP = {
    "F": Flinger, "P": Peon, "N": Knight, "C": Cannon,
    "Q": Queen, "K": King, "Z": Zombie, "B": Bishop, "R": Rook
}

def print_boards(successors) -> None:
    for idx, board in enumerate(successors):
        print(f"=== Successor {idx} ===")
        print(f"Move: {board.last_move}")
        print(board)
        print("\n")


def parse_board() -> tuple[str, list[Piece]]:
    import sys
    lines = sys.stdin.readlines()

    # Read the first line to get turn info (e.g., "w 0 60000 0")
    turn, used_time, total_time, move_number = lines[0].split()

    piece_list: list[Piece] = []
    inside_braces: bool = False

    for line in lines[1:]:
        line = line.strip()
        if line == "{":  # Start reading pieces
            inside_braces = True
            continue
        elif line == "}":  # Stop reading pieces
            inside_braces = False
            break

        if inside_braces:
            if ":" in line:
                position, piece_code = line.split(":")
                position = position.strip()
                # Remove quotes, commas, and any extra whitespace.
                piece_code = piece_code.strip().strip("',")
                color, piece_type = piece_code[0], piece_code[1]
                piece = PIECE_MAP[piece_type](color, position)
                piece_list.append(piece)

    return turn, used_time, total_time, move_number, piece_list

def save_successor_boards(successors, turn):
    """
    Saves each successor board state to a separate file.

    Args:
        successors (list): A list of successor Board objects.
        turn (str): The current player's turn.
    """
    from MoveGenerator import MoveGenerator

    for idx, board in enumerate(successors):
        filename = f"board.{idx:03d}"
        with open(filename, "w") as f:
            # Set the first line: flipped turn followed by "0 6000 0"
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

def print_board(board, turn):
    from MoveGenerator import MoveGenerator

    # Flip the turn (since the AI is making a move)
    flipped_turn = MoveGenerator.flip_turn(turn)

    # Print the first line with turn and time details
    print(f"{flipped_turn} 0 6000 0")

    # Print the board state inside braces
    print("{")
    for pos in sorted(board.pieces.keys()):
        piece = board.pieces[pos]
        # Use "N" for Knight, otherwise use the first character of the class name.
        symbol = "N" if piece.__class__.__name__ == "Knight" else piece.__class__.__name__[0]
        print(f"  {pos}: '{piece.color}{symbol}',")
    print("}")

    # Print the final three reserved lines, always "0"
    print("0\n0\n0")

