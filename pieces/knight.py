from .base import Piece

class Knight(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Knight move offsets (L-shape)
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in knight_moves:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:  # Check board boundaries
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces or board.pieces[move_pos].color != self.color:
                    valid_moves.append(move_pos)

        return valid_moves
