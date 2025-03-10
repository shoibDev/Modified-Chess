from .base import Piece
from .king import King


class Flinger(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []

        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # King moves (1 step in any direction)
        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dx, dy in king_moves:
            move_x, move_y = piece_x + dx, piece_y + dy
            if 0 <= move_x < 8 and 0 <= move_y < 8:
                move_pos = f"{chr(move_x + ord('a'))}{8 - move_y}"
                if move_pos not in board.pieces:
                    valid_moves.append(move_pos)

        return valid_moves

    def get_sling_moves(self, board) -> list:
        sling_moves = []

        piece_x = ord(self.position[0]) - ord('a')
        piece_y = 8 - int(self.position[1])

        # Check all 8 adjacent squares for friendly pieces
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            adj_x, adj_y = piece_x + dx, piece_y + dy

            if not (0 <= adj_x < 8 and 0 <= adj_y < 8):
                continue

            adj_pos = f"{chr(adj_x + ord('a'))}{8 - adj_y}"

            if adj_pos in board.pieces and board.pieces[adj_pos].color == self.color:
                # Sling in both directions
                for direction_multiplier in [1, -1]:
                    sling_dx = dx * direction_multiplier
                    sling_dy = dy * direction_multiplier

                    new_x, new_y = adj_x, adj_y

                    while True:
                        new_x += sling_dx
                        new_y += sling_dy

                        # Check if still on the board
                        if not (0 <= new_x < 8 and 0 <= new_y < 8):
                            break

                        sling_pos = f"{chr(new_x + ord('a'))}{8 - new_y}"

                        # Skip the flinger's own position
                        if sling_pos == self.position:
                            continue

                        if sling_pos in board.pieces:
                            target_piece = board.pieces[sling_pos]
                            if target_piece.color != self.color:
                                if not isinstance(target_piece, King):
                                    # Valid capture (enemy non-King)
                                    sling_moves.append((adj_pos, sling_pos))
                                # Continue to check beyond Kings
                            # Fly over friendlies without stopping
                        else:
                            # Valid empty landing spot
                            sling_moves.append((adj_pos, sling_pos))

        return sling_moves