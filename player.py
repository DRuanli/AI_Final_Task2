from abc import ABC, abstractmethod
from typing import Tuple
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
import time
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
        self.console = Console()

    @abstractmethod
    def make_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Make a move on the board.

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

    def make_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Get move from user input with enhanced UI.

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        while True:
            try:
                # Use rich prompt for better UI
                move_text = Text()
                move_text.append("Enter your move (", style="bright_white")
                move_text.append("row,col", style="bold yellow")
                move_text.append(") [1-9,1-9]: ", style="bright_white")

                self.console.print(move_text, end="")
                move = input()

                row, col = map(int, move.split(','))
                # Adjust to 0-indexed
                row -= 1
                col -= 1

                if 0 <= row < 9 and 0 <= col < 9:
                    if board.make_move(row, col, self.symbol):
                        return row, col
                    else:
                        self.console.print("Position already taken. Try again.", style="bold red")
                else:
                    self.console.print("Invalid position. Row and column must be between 1 and 9.",
                                       style="bold red")
            except ValueError:
                self.console.print("Invalid input. Enter as 'row,col' (e.g., '3,4').",
                                   style="bold red")


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

    def make_move(self, board: GameBoard) -> Tuple[int, int]:
        """
        Use AI to determine and make the best move with animated "thinking".

        Args:
            board: The game board to make a move on

        Returns:
            tuple: (row, col) coordinates of the move
        """
        # Animated thinking effect
        thinking_text = Text("Computer is thinking", style="bold blue")
        with self.console.status(thinking_text, spinner="dots") as status:
            # Simulate "thinking" time
            time.sleep(1.5)

            # Get the best move from AI engine
            row, col = self.ai_engine.get_best_move(board, self.symbol)

        # Make the move with animation
        board.make_move(row, col, self.symbol)

        # Display move information
        move_info = Text()
        move_info.append("Computer placed at: ", style="bright_white")
        move_info.append(f"{row + 1},{col + 1}", style="bold yellow")
        self.console.print(move_info)

        time.sleep(0.5)  # Brief pause to let player see the message
        return row, col