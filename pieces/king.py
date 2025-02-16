from .base import Piece


class King(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        # Convert chess notation to grid indices
        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # King moves one step in all 8 directions
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Horizontal & Vertical (↑ ↓ → ←)
            (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonal (↗ ↖ ↘ ↙)
        ]

        for dx, dy in king_moves:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:  # Stay within board limits
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces or board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)  # Add empty square or capture enemy

        return valid_moves
