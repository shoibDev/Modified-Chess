from pieces.base import Piece
from pieces import Flinger, Peon, Knight, Cannon, Queen, King, Zombie, Bishop, Rook

# Map piece letters to piece classes
PIECE_MAP = {
    "F": Flinger, "P": Peon, "N": Knight, "C": Cannon,
    "Q": Queen, "K": King, "Z": Zombie, "B": Bishop, "R": Rook
}

def parse_board(board_path: str = 'board.txt') -> tuple[str, list[Piece]]:
    """Reads board.txt and returns (turn, piece_list) using JSON."""
    with open(board_path, "r") as f:
        lines = f.readlines()

    #Read first line (get turn info)
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
            # Expecting lines like: "a1: 'wF',"
            if ":" in line:
                position, piece_code = line.split(":")
                position = position.strip()
                piece_code = piece_code.strip().strip("',")  # Remove quotes and comma

                color, piece_type = piece_code[0], piece_code[1]

                piece = PIECE_MAP[piece_type](color, position)
                piece_list.append(piece)

    return turn, piece_list
