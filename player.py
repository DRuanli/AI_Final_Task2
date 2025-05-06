from abc import ABC, abstractmethod
from typing import Tuple
from game_board import GameBoard
from ai_engine import AIEngine


class Player(ABC):
    """
    Abstract base class for player types in the Tic-Tac-Toe game.
    Defines common interface for human and computer players.
    """

    def __init__(self, symbol: str) -> None:
        """
        Initialize a player with their game symbol.

        Args:
            symbol (str): The player's symbol on the board ('X' or 'O')
        """
        self.symbol: str = symbol

    @abstractmethod
    def get_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Get the player's move.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        pass

    def get_opponent_symbol(self) -> str:
        """Get the opponent's symbol."""
        return 'O' if self.symbol == 'X' else 'X'


class HumanPlayer(Player):
    """Human player that gets moves from user input."""

    def get_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Placeholder method for getting a human move.
        The actual implementation is handled by the game controller and UI.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        # This is just a placeholder. The actual move handling is done in GameController
        # to better separate game logic from UI interaction
        return (0, 0)


class ComputerPlayer(Player):
    """Computer player that uses AI to determine moves."""

    def __init__(self, symbol: str, ai_engine: AIEngine) -> None:
        """
        Initialize computer player with symbol and AI engine.

        Args:
            symbol (str): The player's symbol on the board ('X' or 'O')
            ai_engine: The AI engine to use for determining moves
        """
        super().__init__(symbol)
        self.ai_engine: AIEngine = ai_engine

    def get_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Use AI to determine the best move.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the best move
        """
        # Get the best move from AI engine
        row, col = self.ai_engine.get_best_move(board, self.symbol)
        return row, col