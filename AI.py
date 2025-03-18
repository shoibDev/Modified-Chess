import numpy as np
from pieces import Flinger, Peon, Cannon, King, Zombie, Knight
from collections import defaultdict
from Board import Board
import time

K_PST = np.array([
    [-2.00, -1.70, -1.80, -2.30, -2.30, -1.80, -1.70, -2.00],
    [-1.60, -1.30, -1.40, -1.90, -1.90, -1.40, -1.30, -1.60],
    [-1.20, -0.90, -1.00, -1.50, -1.50, -1.00, -0.90, -1.20],
    [-0.80, -0.50, -0.60, -1.10, -1.10, -0.60, -0.50, -0.80],
    [-0.40, -0.10, -0.20, -0.70, -0.70, -0.20, -0.10, -0.40],
    [0.00, 0.30, 0.20, -0.30, -0.30, 0.20, 0.30, 0.00],
    [0.20, 0.50, 0.40, -0.10, -0.10, 0.40, 0.50, 0.20],
    [0.30, 0.60, 0.50, 0.00, 0.00, 0.50, 0.60, 0.30]
], dtype=float)


Q_PST = np.array([
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.05, 0.15, 0.25, 0.35, 0.35, 0.25, 0.15, 0.05],
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [-0.10, 0.00, 0.10, 0.20, 0.20, 0.10, 0.00, -0.10],
    [-0.20, -0.10, 0.00, 0.10, 0.10, 0.00, -0.10, -0.20],
    [-0.30, -0.20, -0.10, 0.00, 0.00, -0.10, -0.20, -0.30],
    [-0.40, -0.30, -0.20, -0.10, -0.10, -0.20, -0.30, -0.40]
], dtype=float)

R_PST = np.array([
    [0.15, 0.20, 0.25, 0.30, 0.30, 0.25, 0.20, 0.15],
    [0.20, 0.25, 0.30, 0.35, 0.35, 0.30, 0.25, 0.20],
    [0.10, 0.15, 0.20, 0.25, 0.25, 0.20, 0.15, 0.10],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [-0.05, 0.00, 0.05, 0.10, 0.10, 0.05, 0.00, -0.05],
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [-0.20, -0.15, -0.10, -0.05, -0.05, -0.10, -0.15, -0.20]
], dtype=float)


B_PST = np.array([
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.10, 0.15, 0.20, 0.25, 0.25, 0.20, 0.15, 0.10],
    [0.05, 0.10, 0.15, 0.20, 0.20, 0.15, 0.10, 0.05],
    [0.00, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05, 0.00],
    [-0.10, -0.05, 0.00, 0.05, 0.05, 0.00, -0.05, -0.10],
    [-0.30, -0.25, -0.20, -0.15, -0.15, -0.20, -0.25, -0.30]
], dtype=float)


N_PST = np.array([
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90],
    [-0.50, -0.30, 0.00, 0.10, 0.10, 0.00, -0.30, -0.50],
    [-0.30, -0.10, 0.20, 0.30, 0.30, 0.20, -0.10, -0.30],
    [-0.20, 0.00, 0.30, 0.40, 0.40, 0.30, 0.00, -0.20],
    [-0.30, -0.10, 0.20, 0.30, 0.30, 0.20, -0.10, -0.30],
    [-0.50, -0.30, 0.00, 0.10, 0.10, 0.00, -0.30, -0.50],
    [-0.70, -0.50, -0.20, -0.10, -0.10, -0.20, -0.50, -0.70],
    [-0.90, -0.70, -0.40, -0.30, -0.30, -0.40, -0.70, -0.90]
], dtype=float)


P_PST = np.array([
    [2.00, 2.10, 2.20, 2.30, 2.30, 2.20, 2.10, 2.00],
    [1.60, 1.70, 1.80, 1.90, 1.90, 1.80, 1.70, 1.60],
    [1.20, 1.30, 1.40, 1.50, 1.50, 1.40, 1.30, 1.20],
    [0.80, 0.90, 1.00, 1.10, 1.10, 1.00, 0.90, 0.80],
    [0.50, 0.60, 0.70, 0.80, 0.80, 0.70, 0.60, 0.50],
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
], dtype=float)


Z_PST = np.array([
    [1.80, 2.00, 2.20, 2.40, 2.40, 2.20, 2.00, 1.80],
    [1.50, 1.70, 1.90, 2.10, 2.10, 1.90, 1.70, 1.50],
    [1.20, 1.40, 1.60, 1.80, 1.80, 1.60, 1.40, 1.20],
    [0.90, 1.10, 1.30, 1.50, 1.50, 1.30, 1.10, 0.90],
    [0.60, 0.80, 1.00, 1.20, 1.20, 1.00, 0.80, 0.60],
    [0.30, 0.50, 0.70, 0.90, 0.90, 0.70, 0.50, 0.30],
    [0.10, 0.30, 0.50, 0.70, 0.70, 0.50, 0.30, 0.10],
    [0.00, 0.20, 0.40, 0.60, 0.60, 0.40, 0.20, 0.00]
], dtype=float)


F_PST = np.array([
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.40, 0.50, 0.60, 0.70, 0.70, 0.60, 0.50, 0.40],
    [0.30, 0.40, 0.50, 0.60, 0.60, 0.50, 0.40, 0.30],
    [0.20, 0.30, 0.40, 0.50, 0.50, 0.40, 0.30, 0.20],
    [0.10, 0.20, 0.30, 0.40, 0.40, 0.30, 0.20, 0.10],
    [0.00, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.00],
    [-0.10, 0.00, 0.10, 0.20, 0.20, 0.10, 0.00, -0.10],
    [-0.15, -0.05, 0.05, 0.15, 0.15, 0.05, -0.05, -0.15]
], dtype=float)


C_PST = np.array([
    [-0.50, -0.30, -0.10, 0.00, 0.00, -0.10, -0.30, -0.50],
    [-0.40, -0.20, 0.00, 0.10, 0.10, 0.00, -0.20, -0.40],
    [-0.20, 0.00, 0.20, 0.30, 0.30, 0.20, 0.00, -0.20],
    [0.00, 0.20, 0.40, 0.50, 0.50, 0.40, 0.20, 0.00],
    [0.10, 0.30, 0.50, 0.60, 0.60, 0.50, 0.30, 0.10],
    [0.00, 0.20, 0.40, 0.50, 0.50, 0.40, 0.20, 0.00],
    [-0.20, 0.00, 0.20, 0.30, 0.30, 0.20, 0.00, -0.20],
    [-0.30, -0.10, 0.10, 0.20, 0.20, 0.10, -0.10, -0.30]
], dtype=float)

PIECE_VALUES = {
    'K': 10000,
    'Q': 9.5,
    'R': 5,
    'B': 7.25,
    'N': 3,
    'P': 1.2,
    'F': 4,
    'C': 11,
    'Z': 8
}

PST = {
    'K': K_PST,
    'Q': Q_PST,
    'R': R_PST,
    'B': B_PST,
    'N': N_PST,
    'P': P_PST,
    'F': F_PST,
    'C': C_PST,
    'Z': Z_PST
}


class AI:
    def __init__(self, depth=4, ai_color='w', remaining_time = 6000, move_count = 0):
        self.depth = depth
        self.ai_color = ai_color
        self.opponent_color = 'b' if ai_color == 'w' else 'w'

        self.capture_bonus = 6
        self.remaining_time = remaining_time
        self.move_count = move_count

    def evaluate(self, board: Board) -> int:
        ai_score = opp_score = 0
        kings = {'w': None, 'b': None}

        # Track pawns to ensure they're moving
        ai_pawns = []
        opp_pawns = []


        for pos, piece in board.pieces.items():
            piece_type = "N" if isinstance(piece, Knight) else piece.__class__.__name__[0]
            value = PIECE_VALUES[piece_type]
            file = ord(pos[0]) - ord('a')
            rank = int(pos[1]) - 1

            pst = PST[piece_type][7 - rank][file] if piece.color == 'b' else PST[piece_type][rank][file]

            if piece.color == self.ai_color:
                ai_score += value + pst
                if piece_type == 'P' or piece_type == 'Z':
                    ai_pawns.append((pos, rank))
            else:
                opp_score += value + pst
                if piece_type == 'P' or piece_type == 'Z':
                    opp_pawns.append((pos, rank))

            if piece_type == 'K':
                kings[piece.color] = pos

        if not kings.get(self.ai_color):
            return -100000
        if not kings.get(self.opponent_color):
            return 100000

        # Bonus for advanced pawns and zombies
        ai_score += self.evaluate_pawn_advancement(ai_pawns, self.ai_color)
        opp_score += self.evaluate_pawn_advancement(opp_pawns, self.opponent_color)

        ai_score += self.evaluate_king_safety(board, kings[self.ai_color], self.ai_color)
        ai_score += self.evaluate_mobility(board, self.ai_color)
        ai_score += self.evaluate_pawn_structure(board, self.ai_color)
        ai_score += self.evaluate_capture_opportunities(board, self.ai_color)

        opp_score += self.evaluate_king_safety(board, kings[self.opponent_color], self.opponent_color)
        opp_score += self.evaluate_mobility(board, self.opponent_color)
        opp_score += self.evaluate_pawn_structure(board, self.opponent_color)
        opp_score += self.evaluate_capture_opportunities(board, self.opponent_color)

        return ai_score - opp_score

    def evaluate_pawn_advancement(self, pawns, color):
        """Reward pawns and zombies that have advanced further toward promotion"""
        score = 0
        for pos, rank in pawns:
            # For white pawns, higher rank means more advanced
            if color == 'w':
                advancement = rank * 0.15  # Increased bonus for advancement
                # Extra bonus for pawns on 6th and 7th ranks
                if rank >= 5:  # 6th rank or higher
                    advancement += 0.3
                if rank >= 6:  # 7th rank
                    advancement += 0.5
            # For black pawns, lower rank means more advanced
            else:
                advancement = (7 - rank) * 0.15
                if rank <= 2:  # 3rd rank or lower
                    advancement += 0.3
                if rank <= 1:  # 2nd rank
                    advancement += 0.5

            score += advancement

        return score

    def evaluate_king_safety(self, board, king_pos, color):
        if not king_pos:
            return 0

        k_file = ord(king_pos[0]) - ord('a')
        k_rank = int(king_pos[1]) - 1
        score = 0
        pawn_shield = 0
        enemy_threats = 0

        # Adjacent squares calculation
        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            af = k_file + dx
            ar = k_rank + dy
            if 0 <= af < 8 and 0 <= ar < 8:
                pos = f"{chr(af + ord('a'))}{ar + 1}"
                if pos in board.pieces and board.pieces[pos].color == color:
                    pawn_shield += 1

        # Pawn shield penalty
        if pawn_shield < 2:
            score -= (2 - pawn_shield) * 5

        # Enemy threats with piece value weighting
        enemy_color = 'b' if color == 'w' else 'w'
        for piece in board.pieces.values():
            if piece.color == enemy_color:
                if king_pos in piece.get_valid_moves(board):
                    enemy_threats += PIECE_VALUES.get(piece.__class__.__name__[0], 1)
                if isinstance(piece, Cannon):
                    for _, targets in piece.get_cannonball_moves(board):
                        if king_pos in targets:
                            enemy_threats += PIECE_VALUES['C']

        score -= enemy_threats * 2  # Reduced multiplier for better balance

        # Open file check
        king_file = king_pos[0]
        if not any(p.position[0] == king_file for p in board.pieces.values()
                   if isinstance(p, Peon) and p.color == color):
            score -= 5

        return score

    def evaluate_mobility(self, board, color):
        """Calculate mobility with bonuses for controlling center"""
        mobility = 0
        center_squares = ['d4', 'd5', 'e4', 'e5']

        for piece in board.pieces.values():
            if piece.color == color:
                moves = piece.get_valid_moves(board)

                # Basic mobility score
                mobility += len(moves) * 0.3

                # Bonus for controlling center
                center_control = sum(1 for move in moves if move in center_squares)
                mobility += center_control * 0.2

                # Extra mobility for pawns and zombies to encourage their movement
                if isinstance(piece, Peon) or isinstance(piece, Zombie):
                    mobility += len(moves) * 0.4

        return mobility

    def evaluate_pawn_structure(self, board, color):
        """Evaluate pawn structure for specified color"""
        score = 0
        pawns = defaultdict(list)
        enemy_pawns = defaultdict(list)

        for pos, piece in board.pieces.items():
            if isinstance(piece, Peon):
                if piece.color == color:
                    pawns[pos[0]].append(int(pos[1]))
                else:
                    enemy_pawns[pos[0]].append(int(pos[1]))

        for file, ranks in pawns.items():
            ranks.sort()
            # Doubled pawns
            if len(ranks) > 1:
                score -= (len(ranks) - 1) * 2

            # Isolation check
            left = chr(ord(file) - 1)
            right = chr(ord(file) + 1)
            isolated = not (pawns.get(left) or pawns.get(right))
            if isolated:
                score -= 3

            # Passed pawn detection
            front_rank = max(ranks) if color == 'w' else min(ranks)
            blocked = False
            for f in [file, left, right]:
                if f in enemy_pawns:
                    if color == 'w':
                        if any(r >= front_rank for r in enemy_pawns[f]):
                            blocked = True
                    else:
                        if any(r <= front_rank for r in enemy_pawns[f]):
                            blocked = True
            if not blocked:
                score += 4 + abs(front_rank - (4 if color == 'w' else 5))

        return score

    def evaluate_capture_opportunities(self, board, color):
        score = 0
        for captured_piece in board.captured:
            piece_type = "N" if isinstance(captured_piece, Knight) else captured_piece.__class__.__name__[0]
            piece_value = PIECE_VALUES.get(piece_type, 1)
            if captured_piece.color != color:
                score += piece_value * self.capture_bonus  # Small bonus for capturing enemies
            else:
                score -= piece_value * 100  # Now completely outweighs any possible gain
        return score

    def sort_moves(self, moves, parent_board):
        def move_priority(move):
            priority = 0
            is_self_checkmate = move.is_checkmate()

            # 1. Capture Bonus: Prioritize capturing high-value pieces
            captured_piece = move.captured[0] if move.captured else None
            if captured_piece:
                piece_type = captured_piece.__class__.__name__[0]
                priority += PIECE_VALUES.get(piece_type, 1) * 1.5

                if piece_type == 'Z':
                    priority += 1000


            # 4. Check Threat: Reward moves that put the enemy king in check
            enemy_king_pos = None
            for pos, piece in move.pieces.items():
                if piece.color == self.opponent_color and isinstance(piece, King):
                    enemy_king_pos = pos
                    break
            if enemy_king_pos:
                for pos, piece in move.pieces.items():
                    if piece.color == self.ai_color and enemy_king_pos in piece.get_valid_moves(move):
                        priority += 200  # Check bonus

            # 5. **PENALTY for Self-Checkmate!**
            if is_self_checkmate:
                priority -= 10000  # Drastically reduce priority

            return priority

        return sorted(moves, key=move_priority, reverse=True)

    def alpha_beta_minimax(self, board, depth, alpha, beta, maximizing, start_time, allowed_time):
        if (time.time() - start_time) * 1000 >= allowed_time:
            return self.evaluate(board)
        if depth == 0 or board.is_checkmate():
            return self.evaluate(board)

        moves = board.generate_successors()
        if maximizing:
            max_eval = -float('inf')
            for move in moves:
                if (time.time() - start_time) * 1000 >= allowed_time:
                    return self.evaluate(board)
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, False, start_time, allowed_time)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                if (time.time() - start_time) * 1000 >= allowed_time:
                    return self.evaluate(board)
                eval_score = self.alpha_beta_minimax(move, depth - 1, alpha, beta, True, start_time, allowed_time)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval

    def choose_best_move(self, board):
        possible_moves = list(board.generate_successors())

        # --- Opening Book Moves Based on Move Number ---
        if self.ai_color == 'w':
            if self.move_count == 0:
                for new_board in possible_moves:
                    if 'e3' in new_board.pieces and new_board.pieces['e3'].__class__.__name__[0] == 'Z':
                        return new_board
            elif self.move_count == 2:
                for new_board in possible_moves:
                    if 'f3' in new_board.pieces and new_board.pieces['f3'].__class__.__name__[0] == 'K':
                        return new_board
            elif self.move_count == 4:
                for new_board in possible_moves:
                    if 'b5' in new_board.pieces and new_board.pieces['b5'].__class__.__name__[0] == 'B':
                        return new_board
        else:
            if self.move_count == 1:
                for new_board in possible_moves:
                    if 'f6' in new_board.pieces and new_board.pieces['f6'].__class__.__name__[0] == 'K':
                        return new_board
            elif self.move_count == 3:
                for new_board in possible_moves:
                    if 'e6' in new_board.pieces and new_board.pieces['e6'].__class__.__name__[0] == 'Z':
                        return new_board
            elif self.move_count == 5:
                for new_board in possible_moves:
                    if 'b6' in new_board.pieces and new_board.pieces['b6'].__class__.__name__[0] == 'P':
                        return new_board

        allowed_time = self.remaining_time - 500 if self.remaining_time > 500 else self.remaining_time
        start_time = time.time()
        best_move = None
        depth = 1  # Start shallow
        time_exceeded = False

        sorted_moves = self.sort_moves(possible_moves, board) if hasattr(self, "sort_moves") else possible_moves

        while (time.time() - start_time) * 1000 < allowed_time:
            current_best_move = None
            current_best_score = -float('inf')
            alpha = -float('inf')
            beta = float('inf')
            is_maximizing = (board.turn == self.ai_color)

            for move in sorted_moves:
                if (time.time() - start_time) * 1000 >= allowed_time:
                    time_exceeded = True
                    break
                score = self.alpha_beta_minimax(move, depth, alpha, beta, not is_maximizing, start_time, allowed_time)
                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move
                    alpha = max(alpha, score)

            if time_exceeded:
                break
            if current_best_move is not None:
                best_move = current_best_move
            depth += 1

        return best_move
