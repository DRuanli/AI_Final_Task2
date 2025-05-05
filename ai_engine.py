import random
import time
from typing import List, Tuple, Optional, Union, Any
from game_board import GameBoard  # Assuming this is imported


class AIEngine:
    """
    Implements the heuristic alpha-beta search algorithm for finding optimal moves.
    Combines minimax with alpha-beta pruning and a custom heuristic function.
    """

    def __init__(self, depth_limit: int = 3) -> None:
        """
        Initialize the AI engine with a specified depth limit.

        The depth limit of 3 was chosen as a balance between:
        1. Search depth: Deeper searches provide better AI decisions
        2. Performance: 9x9 board has many possible positions to evaluate (much larger than 3x3)
        3. User experience: Keeping response time reasonable (under 5 seconds)

        Rationale for depth limit choice:
        - Depth 2: Too shallow for 9x9 board, AI misses obvious winning moves
        - Depth 3: Good balance of speed and intelligence for a 9x9 board
        - Depth 4: Significantly slower without proportional improvement in play quality
           (on average 10x slower than depth 3 due to branching factor)

        Args:
            depth_limit (int): Maximum depth for the alpha-beta search
        """
        self.depth_limit = depth_limit
        self.player_symbol = None
        self.opponent_symbol = None

    def get_best_move(self, board: GameBoard, player_symbol: str) -> Tuple[int, int]:
        """
        Find the best move using alpha-beta search.

        Args:
            board: The current game board
            player_symbol (str): Symbol of the player making the move

        Returns:
            tuple: (row, col) of the best move
        """
        self.player_symbol = player_symbol
        self.opponent_symbol = 'O' if player_symbol == 'X' else 'X'

        # Start alpha-beta search
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')

        # Add a small delay to make it seem like the computer is "thinking"
        time.sleep(0.5)

        empty_positions = board.get_empty_positions()

        # Sort moves to try center positions first (typically stronger in Tic-Tac-Toe)
        # This improves alpha-beta pruning efficiency
        empty_positions.sort(key=lambda pos: -self._position_value(pos))

        for row, col in empty_positions:
            # Try this move
            board_copy = board.get_board_copy()
            board_copy.make_move(row, col, player_symbol)

            # Evaluate this move using h-minimax with alpha-beta pruning
            score = self.minimax(board_copy, self.depth_limit - 1, False, alpha, beta)

            # Update best move if needed
            if score > best_score:
                best_score = score
                best_move = (row, col)

            alpha = max(alpha, best_score)

        # If no good move found (should not happen), pick a random one
        return best_move if best_move else random.choice(empty_positions)

    def _position_value(self, pos: Tuple[int, int]) -> int:
        """
        Helper function to value positions for move ordering.
        Center positions are more valuable in Tic-Tac-Toe.

        Args:
            pos: (row, col) tuple

        Returns:
            int: Position value for sorting
        """
        row, col = pos
        # Distance from center (4,4) - lower is better
        center_distance = abs(row - 4) + abs(col - 4)
        return -center_distance

    def minimax(self, board: GameBoard, depth: int, is_maximizing: bool, alpha: float, beta: float) -> float:
        """
        Minimax algorithm with alpha-beta pruning and heuristic evaluation.

        Args:
            board: The current game board
            depth (int): Current depth in the search tree
            is_maximizing (bool): True if maximizing player's turn, False for minimizing
            alpha (float): Alpha value for pruning
            beta (float): Beta value for pruning

        Returns:
            float: The score of the best move
        """
        # Terminal conditions
        if board.check_win(self.player_symbol):
            return 1000 + depth  # Win for AI (prefer quick wins)

        if board.check_win(self.opponent_symbol):
            return -1000 - depth  # Win for opponent (prefer delaying losses)

        if board.is_full():
            return 0  # Draw

        if depth == 0:
            return self.evaluate_board(board)  # Heuristic evaluation at leaf nodes

        empty_positions = board.get_empty_positions()

        # Sort moves for better pruning
        empty_positions.sort(key=lambda pos: -self._position_value(pos))

        if is_maximizing:
            max_eval = float('-inf')
            for row, col in empty_positions:
                board_copy = board.get_board_copy()
                board_copy.make_move(row, col, self.player_symbol)
                eval_score = self.minimax(board_copy, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in empty_positions:
                board_copy = board.get_board_copy()
                board_copy.make_move(row, col, self.opponent_symbol)
                eval_score = self.minimax(board_copy, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def evaluate_board(self, board: GameBoard) -> int:
        """
        Heuristic evaluation function for non-terminal states.

        This heuristic evaluates the board based on several strategic factors:
        1. Pattern recognition: Counting pieces in potential winning lines (most important)
        2. Board control: Extra value for controlling center and strategic positions
        3. Blocking: Defensive scoring to prevent opponent wins

        Rationale for the heuristic design:
        - Near-win patterns (3 in a row with empty space) are highly valued (50 points)
          as they represent immediate threats
        - Developing positions (2 in a row with empty spaces) have moderate value (10 points)
          as they create future opportunities
        - Center control provides positional advantage (3 points per position)
          as center positions connect to more potential winning lines
        - Blocking opponent's winning moves is almost as valuable as creating your own
          but slightly less (-40 vs +50) to prefer offensive play when possible

        Returns:
            int: Score representing board position quality
        """
        score = 0

        # Evaluate all possible winning lines
        score += self.evaluate_lines(board)

        # Consider center control
        # The center 3x3 region offers more opportunities for winning lines
        center_region = [(3, 3), (3, 4), (3, 5),
                         (4, 3), (4, 4), (4, 5),
                         (5, 3), (5, 4), (5, 5)]
        for row, col in center_region:
            if board.board[row][col] == self.player_symbol:
                score += 3  # Bonus for controlling center positions
            elif board.board[row][col] == self.opponent_symbol:
                score -= 3  # Penalty for opponent controlling center

        return score

    def evaluate_lines(self, board: GameBoard) -> int:
        """
        Evaluate the board by counting potential winning lines.

        Args:
            board: The current game board

        Returns:
            int: Score based on line analysis
        """
        score = 0
        win_length = 4  # Length needed to win

        # Check rows
        for row in range(9):
            for col in range(9 - win_length + 1):
                window = [board.board[row][col + i] for i in range(win_length)]
                score += self.evaluate_window(window)

        # Check columns
        for col in range(9):
            for row in range(9 - win_length + 1):
                window = [board.board[row + i][col] for i in range(win_length)]
                score += self.evaluate_window(window)

        # Check diagonals (top-left to bottom-right)
        for row in range(9 - win_length + 1):
            for col in range(9 - win_length + 1):
                window = [board.board[row + i][col + i] for i in range(win_length)]
                score += self.evaluate_window(window)

        # Check diagonals (top-right to bottom-left)
        for row in range(9 - win_length + 1):
            for col in range(win_length - 1, 9):
                window = [board.board[row + i][col - i] for i in range(win_length)]
                score += self.evaluate_window(window)

        return score

    def evaluate_window(self, window: List[str]) -> int:
        """
        Evaluate a window of 4 positions.

        Args:
            window (list): List of 4 board positions

        Returns:
            int: Score for this window
        """
        score = 0
        player_count = window.count(self.player_symbol)
        opponent_count = window.count(self.opponent_symbol)
        empty_count = window.count(' ')

        # If both players have pieces in this window, it's not a winning line
        if player_count > 0 and opponent_count > 0:
            return 0

        # Prioritize winning moves
        if player_count == 3 and empty_count == 1:
            score += 50  # Near win
        elif player_count == 2 and empty_count == 2:
            score += 10  # Potential future win
        elif player_count == 1 and empty_count == 3:
            score += 1  # Early development

        # Block opponent's winning moves
        if opponent_count == 3 and empty_count == 1:
            score -= 40  # Block opponent's near win
        elif opponent_count == 2 and empty_count == 2:
            score -= 8  # Block opponent's developing threat

        return score