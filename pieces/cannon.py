from .base import Piece


class Cannon(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')  # 'a' -> 0, 'h' -> 7
        piece_y = 8 - int(self.position[1])  # '1' -> 7, '8' -> 0

        # Move like a one-step Rook (↑ ↓ → ←)
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces:  # Can only move to an empty square
                    valid_moves.append(move_pos)

        return valid_moves

    def get_cannonball_targets(self, board) -> list:
        """Returns a list of pieces that would be destroyed by firing a cannonball."""
        targets = []
        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # Fire diagonally (↗ ↖ ↘ ↙)
        for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            hit_pieces = []
            move_x, move_y = piece_x + dx, piece_y + dy

            while 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"

                if move_pos in board.pieces:
                    hit_pieces.append(move_pos)  # Add piece to be removed

                move_x += dx
                move_y += dy

            # Cannonball must hit at least one piece
            if hit_pieces:
                targets.extend(hit_pieces)

        return targets
