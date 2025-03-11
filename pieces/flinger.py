from .base import Piece
from .king import King


class Flinger(Piece):
    def get_valid_moves(self, board) -> list:
        valid_moves = []
        fx = ord(self.position[0]) - ord('a')
        fy = 8 - int(self.position[1])

        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dx, dy in king_moves:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                new_pos = f"{chr(nx + ord('a'))}{8 - ny}"
                # Flinger can't move onto occupied squares
                if new_pos not in board.pieces:
                    valid_moves.append(new_pos)
        return valid_moves

    def get_sling_moves(self, board) -> list:
        sling_moves = []
        fx = ord(self.position[0]) - ord('a')
        fy = 8 - int(self.position[1])

        # Directions for adjacency (8 squares around the Flinger).
        adjacent_dirs = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dx, dy in adjacent_dirs:
            # Adjacent square coordinates
            ax, ay = fx + dx, fy + dy
            # Check if it's on the board
            if not (0 <= ax < 8 and 0 <= ay < 8):
                continue

            adj_pos = f"{chr(ax + ord('a'))}{8 - ay}"
            # If there's a friendly piece at (ax, ay), we can sling it
            if adj_pos in board.pieces and board.pieces[adj_pos].color == self.color:
                # Vector from the adjacent piece -> Flinger = (fx - ax, fy - ay)
                vx = fx - ax
                vy = fy - ay

                # Start from the Flinger's square, then move one step in (vx, vy),
                # continuing until we exit the board or hit an enemy (not a King).
                nx, ny = fx, fy
                while True:
                    nx += vx
                    ny += vy
                    # Off the board?
                    if not (0 <= nx < 8 and 0 <= ny < 8):
                        break

                    new_pos = f"{chr(nx + ord('a'))}{8 - ny}"

                    # If we land on the Flinger's own square again, skip it
                    # (Though practically we won't re-encounter the same spot if vx,vy != (0,0))
                    if new_pos == self.position:
                        continue

                    if new_pos in board.pieces:
                        target_piece = board.pieces[new_pos]
                        # If it's an enemy (not a King), capture
                        if target_piece.color != self.color and not isinstance(target_piece, King):
                            sling_moves.append((adj_pos, new_pos))  # Capture + slung piece destroyed
                        break
                    else:
                        # It's empty -> valid landing
                        sling_moves.append((adj_pos, new_pos))
             
        return sling_moves
