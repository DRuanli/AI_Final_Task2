import os
import time
from typing import Union, Tuple, Optional
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from rich.live import Live

from game_board import GameBoard
from player import HumanPlayer, ComputerPlayer
from ai_engine import AIEngine


class GameController:
    """
    Controls the game flow and manages interactions between components.
    Handles the main game loop, player turns, and game state.
    """

    def __init__(self) -> None:
        """Initialize the game controller and components."""
        self.board: GameBoard = GameBoard()
        self.ai_engine: AIEngine = AIEngine(depth_limit=3)  # Depth limit explained in AIEngine class
        self.human_player: HumanPlayer = HumanPlayer('X')
        self.computer_player: ComputerPlayer = ComputerPlayer('O', self.ai_engine)
        self.current_player: Union[HumanPlayer, ComputerPlayer] = self.human_player  # Human goes first
        self.console = Console()

    def clear_screen(self) -> None:
        """Clear the console screen for a clean display."""
        # Use the GameBoard's clear_screen method
        self.board.clear_screen()

    def display_welcome(self) -> None:
        """Display animated welcome message and game instructions."""
        self.clear_screen()

        # Animated title with typing effect
        title = "9x9 Tic-Tac-Toe with Heuristic Alpha-Beta Search"
        for i in range(len(title) + 1):
            self.clear_screen()
            self.console.print(Panel(
                Text(title[:i], style="bold yellow"),
                box=box.ROUNDED,
                border_style="bright_blue"
            ))
            time.sleep(0.01)  # Fast animation

        # Add animated game rules
        rules = [
            ("Game Rules:", "bold green"),
            ("• You are [bold red]X[/bold red], and the computer is [bold blue]O[/bold blue]", ""),
            ("• Get [bold yellow]4 in a row[/bold yellow] (horizontally, vertically, or diagonally) to win!", ""),
            ("• Enter moves as [bold cyan]row,column[/bold cyan] (e.g., '3,4')", ""),
            ("• Both row and column should be between 1 and 9", "")
        ]

        for rule, style in rules:
            self.console.print(rule, style=style)
            time.sleep(0.2)  # Slight delay between rules

        # Animated prompt
        prompt_text = "\nPress [bold green]Enter[/bold green] to start the game..."
        for i in range(3):  # Blinking effect
            self.console.print(prompt_text, style="bold")
            time.sleep(0.3)
            self.clear_screen()
            self.console.print(Panel(
                Text(title, style="bold yellow"),
                box=box.ROUNDED,
                border_style="bright_blue"
            ))
            for rule, style in rules:
                self.console.print(rule, style=style)
            time.sleep(0.3)

        self.console.print(prompt_text, style="bold")
        input()

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = self.computer_player if self.current_player == self.human_player else self.human_player

    def display_game_status(self) -> None:
        """Display current game status with player turn highlighted."""
        # Create player turn indicator with appropriate styling
        turn_text = Text()
        turn_text.append("Player's turn: ", style="bright_white")

        if self.current_player.symbol == 'X':
            turn_text.append("X", style="bold white on red")
        else:
            turn_text.append("O", style="bold white on blue")

        self.console.print(Panel(
            turn_text,
            box=box.ROUNDED,
            border_style="bright_blue"
        ))

        # Display the board
        self.board.display()

    def display_game_result(self, result: str) -> None:
        """
        Display game result with animation.

        Args:
            result (str): The game result message
        """
        # Animate the result announcement
        for i in range(3):  # Flash effect
            self.clear_screen()
            self.board.display()
            self.console.print()

            # Create the result panel with appropriate styling
            if "won" in result:
                if "You" in result:
                    style = "bold green"
                    border_style = "green"
                else:
                    style = "bold red"
                    border_style = "red"
            else:  # Draw
                style = "bold yellow"
                border_style = "yellow"

            self.console.print(Panel(
                Text(result, style=style),
                box=box.HEAVY,
                border_style=border_style
            ))

            time.sleep(0.3)

            if i < 2:  # Skip the last blank screen
                self.clear_screen()
                self.board.display()
                time.sleep(0.2)

    def play_game(self) -> None:
        """
        Main game loop with enhanced visuals.
        Controls the flow of the game, including turns, win checking, and game end.
        """
        self.display_welcome()
        game_over: bool = False

        while not game_over:
            self.clear_screen()
            self.display_game_status()

            # Get the move from the current player
            row, col = self.current_player.make_move(self.board)

            # Check for win
            if self.board.check_win(self.current_player.symbol):
                self.clear_screen()
                self.board.display()

                if self.current_player == self.human_player:
                    result = "🎉 Congratulations! You won! 🎉"
                else:
                    result = "The computer won! Better luck next time."

                self.display_game_result(result)
                game_over = True
                continue

            # Check for draw
            if self.board.is_full():
                self.clear_screen()
                self.board.display()

                self.display_game_result("It's a draw!")
                game_over = True
                continue

            # Switch to the other player
            self.switch_player()

        # Ask to play again with styled prompt
        self.console.print()
        play_again = Prompt.ask("[bold]Play again?[/bold]",
                                choices=["y", "n"],
                                default="y")

        if play_again.lower() == 'y':
            self.__init__()  # Reset the game
            self.play_game()


def main() -> None:
    """
    Entry point for the application.
    Creates and starts the game controller.
    """
    game: GameController = GameController()
    game.play_game()


if __name__ == "__main__":
    main()