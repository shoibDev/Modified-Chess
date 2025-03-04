from pieces.base import Piece
from pieces import Flinger, Peon, Knight, Cannon, Queen, King, Zombie, Bishop, Rook

# Map piece letters to piece classes
PIECE_MAP = {
    "F": Flinger, "P": Peon, "N": Knight, "C": Cannon,
    "Q": Queen, "K": King, "Z": Zombie, "B": Bishop, "R": Rook
}

def parse_board() -> tuple[str, list[Piece]]:
    import sys
    lines = sys.stdin.readlines()

    # Read the first line to get turn info (e.g., "w 0 60000 0")
    turn, _, _, _ = lines[0].split()

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

    return turn, piece_list
