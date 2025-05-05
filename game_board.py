from typing import List, Tuple, Optional
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box
import os
import time


class GameBoard:
    """
    Class representing the 9x9 Tic-Tac-Toe game board.
    Handles board state management and win condition checking with enhanced visuals.
    """

    def __init__(self) -> None:
        """Initialize an empty 9x9 board."""
        self.board: List[List[str]] = [[' ' for _ in range(9)] for _ in range(9)]
        self.size: int = 9
        self.win_length: int = 4  # Number of consecutive pieces needed to win
        self.console = Console()
        self.last_move: Optional[Tuple[int, int]] = None  # Track last move for highlighting

    def make_move(self, row: int, col: int, symbol: str) -> bool:
        """
        Place a symbol ('X' or 'O') at the specified position with animation effect.

        Args:
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            symbol (str): Player symbol ('X' or 'O')

        Returns:
            bool: True if move was successful, False if position is already taken
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' ':
            # Store last move for highlighting
            self.last_move = (row, col)

            # Set the position on the board
            self.board[row][col] = symbol

            # Animate the move
            self.animate_move(row, col, symbol)
            return True
        return False

    def animate_move(self, row: int, col: int, symbol: str) -> None:
        """
        Create a simple animation effect for a new move.

        Args:
            row (int): Row index of the move
            col (int): Column index of the move
            symbol (str): Player symbol placed
        """
        # Flash the new move with different highlight colors
        highlight_styles = [
            "bold white on green",
            "bold white on yellow",
            "bold white on green"
        ]

        # Clear screen between animation frames
        for style in highlight_styles:
            self.clear_screen()
            self.display_with_highlight(row, col, style)
            time.sleep(0.2)

        # Reset to normal display
        self.clear_screen()
        self.display()

    def clear_screen(self) -> None:
        """Clear the console screen for clean display updates."""
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For Mac and Linux
        else:
            os.system('clear')

    def display_with_highlight(self, highlight_row: int, highlight_col: int, highlight_style: str) -> None:
        """
        Display the board with a highlighted cell.

        Args:
            highlight_row (int): Row index of cell to highlight
            highlight_col (int): Column index of cell to highlight
            highlight_style (str): Rich style string for the highlighted cell
        """
        # Column numbers with styling
        cols = Text("   ")
        for i in range(self.size):
            cols.append(f" {i + 1} ", style="bold cyan")
        self.console.print(cols)

        # Top border
        border = Text("  ╔")
        border.append("═══" * self.size, style="bright_blue")
        border.append("╗")
        self.console.print(border)

        # Board cells with highlighted move
        for i in range(self.size):
            # Row number and left border
            row = Text(f"{i + 1} ║", style="bold cyan")

            for j in range(self.size):
                cell = self.board[i][j]

                # Determine cell style
                if i == highlight_row and j == highlight_col:
                    # Highlighted cell (newest move)
                    cell_style = highlight_style
                elif cell == 'X':
                    cell_style = "bold white on red"
                elif cell == 'O':
                    cell_style = "bold white on blue"
                else:
                    cell_style = "dim white on grey15"

                # Add cell with its style
                if cell == ' ':
                    row.append("   ", style=cell_style)
                else:
                    row.append(f" {cell} ", style=cell_style)

            # Add right border
            row.append("║")
            self.console.print(row)

        # Bottom border
        border = Text("  ╚")
        border.append("═══" * self.size, style="bright_blue")
        border.append("╝")
        self.console.print(border)

    def display(self) -> None:
        """Display the board in the console with rich formatting."""
        # Standard display or highlight the last move if there is one
        if self.last_move:
            self.display_with_highlight(self.last_move[0], self.last_move[1], "bold white on green")
        else:
            self.display_with_highlight(-1, -1, "")  # No highlight

    def check_win(self, symbol: str) -> bool:
        """
        Check if the specified symbol has 4 in a row (horizontally, vertically, or diagonally).

        Args:
            symbol (str): Player symbol to check for win

        Returns:
            bool: True if the player has won, False otherwise
        """
        # Check horizontally
        for row in range(self.size):
            for col in range(self.size - self.win_length + 1):
                if all(self.board[row][col + i] == symbol for i in range(self.win_length)):
                    return True

        # Check vertically
        for row in range(self.size - self.win_length + 1):
            for col in range(self.size):
                if all(self.board[row + i][col] == symbol for i in range(self.win_length)):
                    return True

        # Check diagonally (top-left to bottom-right)
        for row in range(self.size - self.win_length + 1):
            for col in range(self.size - self.win_length + 1):
                if all(self.board[row + i][col + i] == symbol for i in range(self.win_length)):
                    return True

        # Check diagonally (top-right to bottom-left)
        for row in range(self.size - self.win_length + 1):
            for col in range(self.win_length - 1, self.size):
                if all(self.board[row + i][col - i] == symbol for i in range(self.win_length)):
                    return True

        return False

    def is_full(self) -> bool:
        """
        Check if the board is full.

        Returns:
            bool: True if all positions are filled, False otherwise
        """
        return all(self.board[row][col] != ' ' for row in range(self.size) for col in range(self.size))

    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """
        Return a list of empty positions.

        Returns:
            list: List of (row, col) tuples representing empty positions
        """
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == ' ']

    def get_board_copy(self) -> "GameBoard":
        """
        Return a deep copy of the board.

        Returns:
            GameBoard: A new GameBoard object with the same state
        """
        board_copy = GameBoard()
        for row in range(self.size):
            for col in range(self.size):
                board_copy.board[row][col] = self.board[row][col]
        return board_copy