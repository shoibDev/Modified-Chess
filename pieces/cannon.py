from .base import Piece

class Cannon(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []
        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])
        # Move like a one-step Rook
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces:  # Can only move to an empty square
                    valid_moves.append(move_pos)
        return valid_moves

    def get_cannonball_moves(self, board) -> list:
        """
        Returns a list of cannonball moves.
        Each move is a tuple: ((dx, dy), targets)
        """
        moves = []
        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])
        # Diagonal directions
        for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            hit_pieces = []
            move_x, move_y = piece_x + dx, piece_y + dy
            while 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos in board.pieces:
                    hit_pieces.append(move_pos)
                move_x += dx
                move_y += dy
            # Only add this move if at least one piece is hit.
            if hit_pieces:
                moves.append(((dx, dy), hit_pieces))
        return moves