from abc import ABC, abstractmethod


class Player(ABC):
    """
    Abstract base class for player types in the Tic-Tac-Toe game.
    Defines common interface for human and computer players.
    """

    def __init__(self, symbol):
        """
        Initialize a player with their game symbol.

        Args:
            symbol (str): The player's symbol on the board ('X' or 'O')
        """
        self.symbol = symbol

    @abstractmethod
    def make_move(self, board):
        """
        Make a move on the board.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        pass

    def get_opponent_symbol(self):
        """Get the opponent's symbol."""
        return 'O' if self.symbol == 'X' else 'X'


class HumanPlayer(Player):
    """Human player that gets moves from user input."""

    def make_move(self, board):
        """
        Get move from user input.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        while True:
            try:
                move = input(f"Enter your move (row,col) [1-9,1-9]: ")
                row, col = map(int, move.split(','))
                # Adjust to 0-indexed
                row -= 1
                col -= 1

                if 0 <= row < 9 and 0 <= col < 9:
                    if board.make_move(row, col, self.symbol):
                        return row, col
                    else:
                        print("Position already taken. Try again.")
                else:
                    print("Invalid position. Row and column must be between 1 and 9.")
            except ValueError:
                print("Invalid input. Enter as 'row,col' (e.g., '3,4').")


class ComputerPlayer(Player):
    """Computer player that uses AI to determine moves."""

    def __init__(self, symbol, ai_engine):
        """
        Initialize computer player with symbol and AI engine.

        Args:
            symbol (str): The player's symbol on the board ('X' or 'O')
            ai_engine: The AI engine to use for determining moves
        """
        super().__init__(symbol)
        self.ai_engine = ai_engine

    def make_move(self, board):
        """
        Use AI to determine and make the best move.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        print("Computer is thinking...")
        row, col = self.ai_engine.get_best_move(board, self.symbol)
        board.make_move(row, col, self.symbol)
        print(f"Computer placed at: {row + 1},{col + 1}")
        return row, col