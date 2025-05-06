import os
import time
from typing import List, Tuple, Optional
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from rich.padding import Padding
from rich.live import Live
from rich.console import Group
from rich.align import Align


class GameUI:
    """
    Handles all UI-related functionality for the Tic-Tac-Toe game.
    """

    def __init__(self):
        """Initialize the game UI with a console."""
        self.console = Console()

    def clear_screen(self) -> None:
        """Clear the console screen for a clean display."""
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For Mac and Linux
        else:
            os.system('clear')

    def display_welcome(self) -> None:
        """Display an animated, stylish welcome message inspired by Claude Code."""
        self.clear_screen()

        # ASCII art for "TIC TAC TOE"
        title_art = """
        ████████╗██╗ ██████╗    ████████╗ █████╗  ██████╗    ████████╗ ██████╗ ███████╗
        ╚══██╔══╝██║██╔════╝    ╚══██╔══╝██╔══██╗██╔════╝    ╚══██╔══╝██╔═══██╗██╔════╝
           ██║   ██║██║            ██║   ███████║██║            ██║   ██║   ██║█████╗  
           ██║   ██║██║            ██║   ██╔══██║██║            ██║   ██║   ██║██╔══╝  
           ██║   ██║╚██████╗       ██║   ██║  ██║╚██████╗       ██║   ╚██████╔╝███████╗
           ╚═╝   ╚═╝ ╚═════╝       ╚═╝   ╚═╝  ╚═╝ ╚═════╝       ╚═╝    ╚═════╝ ╚══════╝
        """

        # Welcome message with border
        welcome_text = Text("✨ Welcome to ", style="dim white")
        welcome_text.append("ATic-Tac-Toe", style="bold color(2)")
        welcome_text.append(" preview! ✨", style="dim white")

        welcome_panel = Panel(
            welcome_text,
            box=box.ROUNDED,
            border_style="color(2)",
            padding=(1, 2)
        )

        # Display welcome banner first without animation
        self.console.print(welcome_panel)

        # Create main title panel
        title_panel = Panel(
            Text(title_art, style="color(2)"),
            box=box.HEAVY,
            border_style="color(2)",
            padding=(1, 1)
        )
        self.console.print(title_panel)

        # Subtitle with alpha-beta description
        subtitle = Panel(
            Text("9×9 with Heuristic Alpha-Beta Search", style="bold color(214)"),
            box=box.ROUNDED,
            border_style="color(214)"
        )
        self.console.print(subtitle)

        # Author information
        author_text = Text("Created by: ", style="dim white")
        author_text.append("Le Dang Nguyen - 522K0020", style="bold color(250)")
        author_panel = Panel(
            author_text,
            box=box.SIMPLE,
            border_style="bright_blue",
            width=50
        )
        self.console.print(author_panel)

        # Game rules with animated display
        self.console.print()
        rules = [
            ("Game Rules:", "bold green"),
            ("• You are [bold red]X[/bold red], and the computer is [bold blue]O[/bold blue]", ""),
            ("• Get [bold yellow]4 in a row[/bold yellow] (horizontally, vertically, or diagonally) to win!", ""),
            ("• Enter moves as [bold cyan]row,column[/bold cyan] (e.g., '3,4')", ""),
            ("• Both row and column should be between 1 and 9", "")
        ]

        for rule, style in rules:
            self.console.print(rule, style=style)
            time.sleep(0.1)

        # Simpler animated prompt without ANSI sequences
        self.console.print()

        prompt_styles = [
            "bold green",
            "bold yellow",
            "bold green"
        ]

        for style in prompt_styles:
            self.clear_screen()
            # Reprint all the content
            self.console.print(welcome_panel)
            self.console.print(title_panel)
            self.console.print(subtitle)
            self.console.print(author_panel)
            self.console.print()

            # Reprint all rules
            for rule, rule_style in rules:
                self.console.print(rule, style=rule_style)

            self.console.print()
            self.console.print(f"Press [bold {style}]Enter[/bold {style}] to start the game...", style="bold")
            time.sleep(0.5)

        # Final prompt
        self.console.print("Press [bold green]Enter[/bold green] to start the game...", style="bold")
        input()

    def display_game_status(self, current_player_symbol: str) -> None:
        """
        Display game status header with clean styling.

        Args:
            current_player_symbol (str): Symbol ('X' or 'O') of the current player
        """
        # Create a clean header with game title and player turn
        header = Panel(
            Text.assemble(
                ("9×9 Tic-Tac-Toe", "bold cyan"),
                (" | ", "dim white"),
                ("Player's turn: ", "white"),
                (current_player_symbol, f"bold white on {'red' if current_player_symbol == 'X' else 'blue'}")
            ),
            box=box.ROUNDED,
            border_style="blue",
            padding=(0, 2)
        )

        self.console.print(header)

    def display_board(self, board, last_move: Optional[Tuple[int, int]] = None) -> None:
        """
        Display the game board with enhanced visuals.

        Args:
            board: 2D list representing the board state
            last_move: Optional tuple with (row, col) of the last move made
        """
        # Define better cell visuals
        light_bg = "grey23"
        dark_bg = "grey15"

        # Column numbers with consistent styling
        cols = Text("     ")
        for i in range(len(board[0])):
            cols.append(f" {i + 1} ", style="bold cyan")
        self.console.print(cols)

        # Top border
        border = Text("    ┏")
        border.append("━━━" * len(board[0]), style="cyan")
        border.append("┓")
        self.console.print(border)

        # Board cells
        for i in range(len(board)):
            # Row number
            row = Text(f" {i + 1}  ┃", style="bold cyan")

            for j in range(len(board[i])):
                cell = board[i][j]
                bg_color = light_bg if (i + j) % 2 == 0 else dark_bg

                # Cell styling
                if last_move and i == last_move[0] and j == last_move[1]:
                    # Highlighted last move
                    cell_style = f"bold white on green"
                elif cell == 'X':
                    cell_style = f"bold white on red"
                elif cell == 'O':
                    cell_style = f"bold white on blue"
                else:
                    cell_style = f"dim white on {bg_color}"

                # Cell content
                if cell == ' ':
                    cell_content = " · "
                else:
                    cell_content = f" {cell} "

                row.append(cell_content, style=cell_style)

            # Right border
            row.append("┃")
            self.console.print(row)

        # Bottom border
        border = Text("    ┗")
        border.append("━━━" * len(board[0]), style="cyan")
        border.append("┛")
        self.console.print(border)

    def prompt_for_move(self) -> Tuple[int, int]:
        """
        Prompt the user for their move with enhanced styling that aligns with UI.

        Returns:
            tuple: (row, col) of the user's move (0-indexed)
        """
        while True:
            try:
                # Simple bordered prompt without cursor repositioning
                prompt_panel = Panel(
                    Text.assemble(
                        ("Enter your move ", "white"),
                        ("(row,col)", "bold yellow"),
                        (" [1-9,1-9]: ", "white")
                    ),
                    box=box.ROUNDED,
                    border_style="yellow",
                    padding=(0, 2)
                )

                self.console.print(prompt_panel)

                # Get input on a new line (no cursor positioning)
                move = input()

                # Process input
                row, col = map(int, move.split(','))
                # Adjust to 0-indexed
                row -= 1
                col -= 1

                if 0 <= row < 9 and 0 <= col < 9:
                    return row, col
                else:
                    self.console.print("⚠️  Invalid position. Row and column must be between 1 and 9.",
                                       style="bold red")
            except ValueError:
                self.console.print("⚠️  Invalid input. Enter as 'row,col' (e.g., '3,4').",
                                   style="bold red")
    def display_win_announcement(self, is_human_win: bool, board) -> None:
        """
        Display a stylized win announcement.

        Args:
            is_human_win (bool): True if human won, False if computer won
            board: The current board state to display
        """
        # Animation frames for the win announcement
        frames = [
            "🎮 GAME OVER 🎮",
            "✨ GAME OVER ✨",
            "🏆 GAME OVER 🏆"
        ]

        # Win message based on winner
        if is_human_win:
            win_text = "🎉 Congratulations! You Won! 🎉"
            style = "bold green"
            border_style = "green"
        else:
            win_text = "Computer Won! Better luck next time."
            style = "bold red"
            border_style = "red"

        # Animate the announcement
        for i in range(6):  # Animation loop
            self.clear_screen()
            self.display_board(board)

            frame_idx = i % len(frames)

            # Create title with current frame
            title_text = Text(frames[frame_idx], style=style)

            # Create the result panel
            result_panel = Panel(
                Group(
                    Align.center(title_text),
                    Align.center(Text(win_text, style=style))
                ),
                box=box.HEAVY,
                border_style=border_style,
                title="Result",
                padding=(1, 2)
            )

            self.console.print()
            self.console.print(result_panel)

            time.sleep(0.3)

    def display_draw_announcement(self, board) -> None:
        """
        Display a stylized draw announcement.

        Args:
            board: The current board state to display
        """
        self.clear_screen()
        self.display_board(board)

        # Create the draw panel
        draw_panel = Panel(
            Text("It's a draw! Well played by both sides.", style="bold yellow"),
            box=box.HEAVY,
            border_style="yellow",
            title="Draw",
            padding=(1, 2)
        )

        self.console.print()
        self.console.print(draw_panel)


    def display_computer_thinking(self) -> None:
        """Display an animated 'computer thinking' message."""
        thinking_text = Text("Computer is thinking", style="bold blue")
        with self.console.status(thinking_text, spinner="dots") as status:
            # Simulate "thinking" time - this will be handled by the controller
            time.sleep(1.5)

    def display_computer_move(self, row: int, col: int) -> None:
        """
        Display information about the computer's move.

        Args:
            row (int): Row index of computer's move (0-indexed)
            col (int): Column index of computer's move (0-indexed)
        """
        # Display move information
        move_info = Text()
        move_info.append("Computer placed at: ", style="bright_white")
        move_info.append(f"{row + 1},{col + 1}", style="bold yellow")
        self.console.print(move_info)

        time.sleep(0.5)  # Brief pause to let player see the message

    def prompt_play_again(self) -> bool:
        """
        Ask the user if they want to play again with styled prompt.

        Returns:
            bool: True if the user wants to play again, False otherwise
        """
        self.console.print()
        play_again = Prompt.ask("[bold]Play again?[/bold]",
                                choices=["y", "n"],
                                default="y")

        return play_again.lower() == 'y'