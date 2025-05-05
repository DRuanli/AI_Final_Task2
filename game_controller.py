import time
from typing import Union, Tuple, Optional
from game_board import GameBoard
from player import HumanPlayer, ComputerPlayer
from ai_engine import AIEngine
from ui import GameUI


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
        self.ui = GameUI()

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = self.computer_player if self.current_player == self.human_player else self.human_player

    def get_human_move(self) -> Tuple[int, int]:
        """
        Get and validate a move from the human player.

        Returns:
            tuple: (row, col) coordinates of the valid move
        """
        while True:
            row, col = self.ui.prompt_for_move()

            if self.board.board[row][col] == ' ':
                # Valid move
                self.board.make_move(row, col, self.human_player.symbol)
                return row, col
            else:
                self.ui.console.print("Position already taken. Try again.", style="bold red")

    def get_computer_move(self) -> Tuple[int, int]:
        """
        Get the computer's move using the AI engine.

        Returns:
            tuple: (row, col) coordinates of the computer's move
        """
        # Show thinking animation
        self.ui.display_computer_thinking()

        # Get the best move from AI engine
        row, col = self.ai_engine.get_best_move(self.board, self.computer_player.symbol)

        # Make the move
        self.board.make_move(row, col, self.computer_player.symbol)

        # Display move information
        self.ui.display_computer_move(row, col)

        return row, col

    def play_game(self) -> None:
        """
        Main game loop.
        Controls the flow of the game, including turns, win checking, and game end.
        """
        self.ui.display_welcome()
        game_over: bool = False

        while not game_over:
            self.ui.clear_screen()
            self.ui.display_game_status(self.current_player.symbol)
            self.ui.display_board(self.board.board, self.board.last_move)

            # Get the move from the current player
            if self.current_player == self.human_player:
                row, col = self.get_human_move()
            else:
                row, col = self.get_computer_move()

            # Check for win
            if self.board.check_win(self.current_player.symbol):
                self.ui.clear_screen()
                self.ui.display_board(self.board.board, (row, col))

                is_human_win = self.current_player == self.human_player
                self.ui.display_win_announcement(is_human_win, self.board.board)
                game_over = True
                continue

            # Check for draw
            if self.board.is_full():
                self.ui.clear_screen()
                self.ui.display_board(self.board.board, (row, col))

                self.ui.display_draw_announcement(self.board.board)
                game_over = True
                continue

            # Switch to the other player
            self.switch_player()

        # Ask to play again
        if self.ui.prompt_play_again():
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