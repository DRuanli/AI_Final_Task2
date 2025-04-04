import os
import time
import pygame
import sys
from game_board import GameBoard
from player import HumanPlayer, ComputerPlayer
from ai_engine import AIEngine
from pygame_view import PyGameView


class GameController:
    """
    Controls the game flow and manages interactions between components.
    Handles the main game loop, player turns, and game state.
    """

    def __init__(self, use_pygame=True):
        """
        Initialize the game controller and components.

        Args:
            use_pygame (bool): If True, use pygame visualization; otherwise use console
        """
        self.board = GameBoard()
        self.ai_engine = AIEngine(depth_limit=3)  # Depth limit explained in AIEngine class
        self.human_player = HumanPlayer('X')
        self.computer_player = ComputerPlayer('O', self.ai_engine)
        self.current_player = self.human_player  # Human goes first
        self.use_pygame = use_pygame

        if self.use_pygame:
            self.view = PyGameView()

    def clear_screen(self):
        """Clear the console screen for a clean display."""
        # Only used in console mode
        if not self.use_pygame:
            # For Windows
            if os.name == 'nt':
                os.system('cls')
            # For Mac and Linux
            else:
                os.system('clear')

    def display_welcome(self):
        """Display welcome message and game instructions."""
        if self.use_pygame:
            self.view.draw_board(self.board)
            self.view.display_message("Your turn (X)")
            self.view.update()
        else:
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

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = self.computer_player if self.current_player == self.human_player else self.human_player

    def find_winning_line(self, symbol):
        """
        Find the coordinates of the winning line.
        Used for highlighting in pygame mode.

        Args:
            symbol (str): Symbol to check for win

        Returns:
            tuple: ((start_row, start_col), (end_row, end_col)) or None if no win
        """
        # Check horizontally
        for row in range(self.board.size):
            for col in range(self.board.size - self.board.win_length + 1):
                if all(self.board.board[row][col + i] == symbol for i in range(self.board.win_length)):
                    return ((row, col), (row, col + self.board.win_length - 1))

        # Check vertically
        for row in range(self.board.size - self.board.win_length + 1):
            for col in range(self.board.size):
                if all(self.board.board[row + i][col] == symbol for i in range(self.board.win_length)):
                    return ((row, col), (row + self.board.win_length - 1, col))

        # Check diagonally (top-left to bottom-right)
        for row in range(self.board.size - self.board.win_length + 1):
            for col in range(self.board.size - self.board.win_length + 1):
                if all(self.board.board[row + i][col + i] == symbol for i in range(self.board.win_length)):
                    return ((row, col), (row + self.board.win_length - 1, col + self.board.win_length - 1))

        # Check diagonally (top-right to bottom-left)
        for row in range(self.board.size - self.board.win_length + 1):
            for col in range(self.board.win_length - 1, self.board.size):
                if all(self.board.board[row + i][col - i] == symbol for i in range(self.board.win_length)):
                    return ((row, col), (row + self.board.win_length - 1, col - (self.board.win_length - 1)))

        return None

    def play_game_console(self):
        """
        Console-based main game loop.
        Controls the flow of the game, including turns, win checking, and game end.
        """
        self.display_welcome()
        game_over = False

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
        play_again = input("\nPlay again? (y/n): ").lower().strip()
        if play_again == 'y':
            self.__init__(use_pygame=False)  # Reset the game
            self.play_game_console()

    def play_game_pygame(self):
        """
        Pygame-based main game loop.
        Handles game flow with visual interface and mouse input.
        """
        self.display_welcome()
        game_over = False
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_r:
                        # Restart game
                        self.__init__(use_pygame=True)
                        return self.play_game_pygame()

                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    # Human player's turn
                    if self.current_player == self.human_player:
                        cell = self.view.get_cell_from_pos(event.pos)
                        if cell:
                            row, col = cell
                            if self.board.make_move(row, col, self.human_player.symbol):
                                self.view.play_move_sound()
                                self.view.draw_board(self.board)

                                # Check for win
                                if self.board.check_win(self.human_player.symbol):
                                    winning_line = self.find_winning_line(self.human_player.symbol)
                                    if winning_line:
                                        self.view.highlight_win(*winning_line)
                                    self.view.display_message("You won!", self.view.GREEN)
                                    game_over = True
                                # Check for draw
                                elif self.board.is_full():
                                    self.view.display_message("It's a draw!")
                                    game_over = True
                                else:
                                    # Switch to computer's turn
                                    self.switch_player()
                                    self.view.display_message("Computer's turn...")
                                    self.view.update()

                                    # Give a small delay so the message is visible
                                    pygame.time.delay(500)

                                    # Computer makes a move
                                    row, col = self.computer_player.make_move(self.board)
                                    self.view.play_move_sound()
                                    self.view.draw_board(self.board)

                                    # Check for win
                                    if self.board.check_win(self.computer_player.symbol):
                                        winning_line = self.find_winning_line(self.computer_player.symbol)
                                        if winning_line:
                                            self.view.highlight_win(*winning_line)
                                        self.view.display_message("Computer won!", self.view.RED)
                                        game_over = True
                                    # Check for draw
                                    elif self.board.is_full():
                                        self.view.display_message("It's a draw!")
                                        game_over = True
                                    else:
                                        # Switch back to human
                                        self.switch_player()
                                        self.view.display_message("Your turn (X)")

            # Always redraw to avoid any visual glitches
            if not game_over:
                self.view.draw_board(self.board)

            if game_over:
                self.view.display_message(
                    "Game Over!\nPress 'R' to restart\nor 'ESC' to quit",
                    self.view.BLACK
                )

            self.view.update()
            clock.tick(30)  # Cap at 30 FPS to avoid excessive CPU usage

    def play_game(self):
        """Start the game in appropriate mode."""
        if self.use_pygame:
            self.play_game_pygame()
        else:
            self.play_game_console()


def main(use_pygame=True):
    """
    Entry point for the application.
    Creates and starts the game controller.

    Args:
        use_pygame (bool): If True, use pygame visualization; otherwise use console
    """
    game = GameController(use_pygame)
    game.play_game()


if __name__ == "__main__":
    main()