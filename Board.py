from MoveGenerator import MoveGenerator

from pieces.base import Piece
from pieces import King, Zombie, Peon

class Board:
    def __init__(self) -> None:
        """Initializes an empty board with both a dictionary and a grid representation."""
        self.grid = [['.' for _ in range(8)] for _ in range(8)]
        self.pieces: dict[str, Piece] = {}  # Maps positions ('e4') to Piece objects
        self.turn = None 


    def add_piece(self, piece: Piece) -> None:
        self.pieces[piece.position] = piece

        # Convert to grid coordinates
        file, rank = ord(piece.position[0]) - ord('a'), int(piece.position[1]) - 1
        self.grid[7 - rank][file] = str(piece)  # Store string representation

    def apply_zombie_contagion(self):
        """After a turn, adjacent enemy pieces to zombies become zombies."""
        new_zombies = []  # Store newly infected pieces

        for pos, piece in self.pieces.items():
            if isinstance(piece, Zombie):  # Find all zombies
                piece_x = ord(pos[0]) - ord('a')
                piece_y = 8 - int(pos[1])

                # Check adjacent squares
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    adj_x, adj_y = piece_x + dx, piece_y + dy
                    if 0 <= adj_x < 8 and 0 <= adj_y < 8:
                        adj_pos = f"{chr(adj_x + ord('a'))}{8 - adj_y}"

                        # If there's an enemy piece that isn't a King or another Zombie, convert it
                        if adj_pos in self.pieces:
                            target_piece = self.pieces[adj_pos]
                            if not isinstance(target_piece, (King, Zombie)) and target_piece.color != piece.color:
                                new_zombies.append((adj_pos, piece.color))  # Store (position, color)

        # Convert infected pieces to zombies
        for pos, new_color in new_zombies:
            self.pieces[pos] = Zombie(new_color, pos)  # Turn it into a Zombie

    def apply_peon_promotion(self):
        """Promote any Peon that reaches the end of the board into a Zombie."""
        for pos, piece in list(self.pieces.items()):
            if isinstance(piece, Peon):
                rank = int(pos[1])
                # White Peons promote at rank 8, Black Peons at rank 1.
                if (piece.color == 'w' and rank == 8) or (piece.color == 'b' and rank == 1):
                    self.pieces[pos] = Zombie(piece.color, pos)

    def is_checkmate(self) -> bool:
        kings = [piece for piece in self.pieces.values() if isinstance(piece, King)]
        return len(kings) < 2  # If one or none kings remain, the game is over.

    def generate_successors(self) -> list:
        return MoveGenerator.generate_successor_boards(self)


    def refresh_grid(self):
        """Rebuild the grid from the current board.pieces dictionary. DEBUGGIUNG PURSPOSE ONLY!"""
        self.grid = [['.' for _ in range(8)] for _ in range(8)]
        for pos, piece in self.pieces.items():
            file = ord(pos[0]) - ord('a')
            rank = int(pos[1]) - 1
            self.grid[7 - rank][file] = str(piece)

    def __repr__(self) -> str:
        return "\n".join("  ".join(row) for row in self.grid)
