from pieces.base import Piece

class Board:
    def __init__(self) -> None:
        """Initializes an empty board with both a dictionary and a grid representation."""
        self.grid = [['.' for _ in range(8)] for _ in range(8)]
        self.pieces: dict[str, Piece] = {}  # Maps positions ('e4') to Piece objects
        self.turn = None  # Whose turn it is ('w' or 'b')

    def add_piece(self, piece: Piece) -> None:
        self.pieces[piece.position] = piece

        # Convert to grid coordinates
        file, rank = ord(piece.position[0]) - ord('a'), int(piece.position[1]) - 1
        self.grid[7 - rank][file] = str(piece)  # Store string representation

    def __repr__(self) -> str:
        """Returns a visual representation of the board."""
        return "\n".join("  ".join(row) for row in self.grid)
