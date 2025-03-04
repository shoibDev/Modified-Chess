from pieces.base import Piece
from pieces.king import King
from pieces.zombie import Zombie
from pieces.peon import Peon
from pieces.flinger import Flinger
from pieces.cannon import Cannon

class MoveGenerator:
    @staticmethod
    def clone_board(board):
        from Board import Board
        new_board = Board()
        new_board.turn = board.turn
        # Initialize debug attribute
        new_board.last_move = ""
        for pos, piece in board.pieces.items():
            new_piece = type(piece)(piece.color, piece.position)
            new_board.add_piece(new_piece)
        return new_board

    @staticmethod
    def apply_move(board, from_pos: str, to_pos: str) -> None:
        # Remove and get the moving piece from the old position.
        moving_piece = board.pieces.pop(from_pos, None)
        if not moving_piece:
            return  # No piece at from_pos

        # Remove any piece at the target location (capture) using pop.
        board.pieces.pop(to_pos, None)

        # Update the grid: clear the old position.
        old_file = ord(from_pos[0]) - ord('a')
        old_rank = int(from_pos[1]) - 1
        board.grid[7 - old_rank][old_file] = '.'

        # Update the piece's internal position.
        moving_piece.position = to_pos

        # Add the piece at its new location (which also updates the grid).
        board.add_piece(moving_piece)

    @staticmethod
    def apply_special_move(board, move_tuple, mover_type: str) -> None:
        from Board import Board  # Local import to avoid circular dependency
        if mover_type == 'flinger':
            from_pos, landing_spot = move_tuple

            # Remove the slung piece from its original location.
            slung_piece = board.pieces.pop(from_pos, None)
            if not slung_piece:
                return

            # Clear the grid cell for the original location.
            old_file = ord(from_pos[0]) - ord('a')
            old_rank = int(from_pos[1]) - 1
            board.grid[7 - old_rank][old_file] = '.'

            if landing_spot in board.pieces:
                # Capture scenario: landing spot is occupied by an enemy.
                enemy_file = ord(landing_spot[0]) - ord('a')
                enemy_rank = int(landing_spot[1]) - 1
                board.grid[7 - enemy_rank][enemy_file] = '.'
                # Remove the enemy piece.
                board.pieces.pop(landing_spot, None)
                # The slung piece is also destroyed; do not re-add.
            else:
                # No enemy at landing spot; move the slung piece.
                slung_piece.position = landing_spot
                board.add_piece(slung_piece)

        elif mover_type == 'cannon':
            # For cannon moves, remove every target and update the grid.
            for target_pos in move_tuple:
                board.pieces.pop(target_pos, None)
                target_file = ord(target_pos[0]) - ord('a')
                target_rank = int(target_pos[1]) - 1
                board.grid[7 - target_rank][target_file] = '.'

    @staticmethod
    def flip_turn(turn: str) -> str:
        return 'b' if turn == 'w' else 'w'

    @staticmethod
    def generate_successor_boards(current_board) -> list:
        """Generate succesor boards, and this has debugging lines"""
        from Board import Board
        successors = []

        for pos, piece in current_board.pieces.items():
            if piece.color != current_board.turn:
                continue

            # Normal moves
            moves = piece.get_valid_moves(current_board)
            for move in moves:
                new_board = MoveGenerator.clone_board(current_board)
                MoveGenerator.apply_move(new_board, pos, move)
                new_board.last_move = f"{piece.__class__.__name__} moved from {pos} to {move}"
                new_board.apply_zombie_contagion()
                new_board.apply_peon_promotion()
                new_board.refresh_grid()
                new_board.turn = MoveGenerator.flip_turn(new_board.turn)
                successors.append(new_board)

            # Special moves for Flinger
            if isinstance(piece, Flinger):
                sling_moves = piece.get_sling_moves(current_board)
                for move_tuple in sling_moves:
                    new_board = MoveGenerator.clone_board(current_board)
                    MoveGenerator.apply_special_move(new_board, move_tuple, 'flinger')
                    new_board.last_move = f"Flinger sling: {move_tuple[0]} -> {move_tuple[1]}"
                    new_board.apply_zombie_contagion()
                    new_board.refresh_grid()
                    new_board.apply_peon_promotion()
                    new_board.turn = MoveGenerator.flip_turn(new_board.turn)
                    successors.append(new_board)

            # Special moves for Cannon
            if isinstance(piece, Cannon):
                cannonball_moves = piece.get_cannonball_moves(current_board)
                for direction, targets in cannonball_moves:
                    new_board = MoveGenerator.clone_board(current_board)
                    MoveGenerator.apply_special_move(new_board, targets, 'cannon')
                    new_board.last_move = f"Cannon fires diagonally {direction}, removing targets: {targets}"
                    new_board.apply_zombie_contagion()
                    new_board.apply_peon_promotion()
                    new_board.turn = MoveGenerator.flip_turn(new_board.turn)
                    successors.append(new_board)
        return successors
