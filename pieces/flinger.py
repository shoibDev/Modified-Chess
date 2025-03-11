from .base import Piece
from .king import King


class Flinger(Piece):
    def get_valid_moves(self, board) -> list:
        """The Flinger moves like a King but cannot capture (cannot land on occupied squares)."""
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
                if new_pos not in board.pieces:
                    valid_moves.append(new_pos)
        return valid_moves

    def get_sling_moves(self, board) -> list:
        sling_moves = []
        fx = ord(self.position[0]) - ord('a')
        fy = 8 - int(self.position[1])

        # All 8 adjacent directions.
        adjacent_dirs = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]

        for dx, dy in adjacent_dirs:
            ax, ay = fx + dx, fy + dy
            if not (0 <= ax < 8 and 0 <= ay < 8):
                continue
            adj_pos = f"{chr(ax + ord('a'))}{8 - ay}"
            # Check for an adjacent friendly piece.
            if adj_pos in board.pieces and board.pieces[adj_pos].color == self.color:
                # Compute the vector from A to F.
                vx = fx - ax
                vy = fy - ay
                # Start at the Flinger’s square.
                nx, ny = fx, fy
                while 0 <= nx < 8 and 0 <= ny < 8:
                    nx += vx
                    ny += vy
                    if not (0 <= nx < 8 and 0 <= ny < 8):
                        break
                    new_pos = f"{chr(nx + ord('a'))}{8 - ny}"
                    if new_pos == self.position:
                        continue  # Skip Flinger's square.
                    # Check landing square:
                    if new_pos in board.pieces:
                        occupant = board.pieces[new_pos]
                        # If enemy and not a King, record as capture move.
                        if occupant.color != self.color and not isinstance(occupant, King):
                            sling_moves.append((adj_pos, new_pos))
                        # Do not break—continue flying over even if this square is occupied.
                    else:
                        # Empty square is valid.
                        sling_moves.append((adj_pos, new_pos))
        return sling_moves
