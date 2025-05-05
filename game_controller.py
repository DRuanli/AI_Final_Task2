import os
import time
from typing import Union, Tuple, Optional
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

    def clear_screen(self) -> None:
        """Clear the console screen for a clean display."""
        # For Windows
        if os.name == 'nt':
            os.system('cls')
        # For Mac and Linux
        else:
            os.system('clear')

    def display_welcome(self) -> None:
        """Display welcome message and game instructions."""
        self.clear_screen()
        print("=" * 50)
        print("9x9 Tic-Tac-Toe with Heuristic Alpha-Beta Search")
        print("=" * 50)
        print("You are 'X', and the computer is 'O'.")
        print("Get 4 in a row (horizontally, vertically, or diagonally) to win!")
        print("Enter moves as 'row,column' (e.g., '3,4').")
        print("Both row and column should be between 1 and 9.")
        print("=" * 50)
        input("Press Enter to start the game...")

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = self.computer_player if self.current_player == self.human_player else self.human_player

    def play_game(self) -> None:
        """
        Main game loop.
        Controls the flow of the game, including turns, win checking, and game end.
        """
        self.display_welcome()
        game_over: bool = False

        while not game_over:
            self.clear_screen()
            print(f"Player's turn: {self.current_player.symbol}")
            self.board.display()

            # Get the move from the current player
            row, col = self.current_player.make_move(self.board)

            # Check for win
            if self.board.check_win(self.current_player.symbol):
                self.clear_screen()
                self.board.display()
                if self.current_player == self.human_player:
                    print("Congratulations! You won!")
                else:
                    print("The computer won! Better luck next time.")
                game_over = True
                continue

            # Check for draw
            if self.board.is_full():
                self.clear_screen()
                self.board.display()
                print("It's a draw!")
                game_over = True
                continue

            # Switch to the other player
            self.switch_player()

        # Ask to play again
        play_again: str = input("\nPlay again? (y/n): ").lower().strip()
        if play_again == 'y':
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