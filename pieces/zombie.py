from .base import Piece
from .king import King

class Zombie(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # Zombie moves like a one-step Rook (↑ ↓ → ←)
        zombie_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in zombie_moves:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:  # Stay within board limits
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"

                if move_pos not in board.pieces:
                    valid_moves.append(move_pos)  # Move to empty square
                elif board.pieces[move_pos].color != self.color and not isinstance(board.pieces[move_pos], King):
                    valid_moves.append(move_pos)  # Capture enemy piece (except King)

        return valid_moves
