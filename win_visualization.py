import time


class WinVisualizer:
    """
    Class to handle visualization of win patterns in the Tic-Tac-Toe game.
    Highlights winning lines and provides visual feedback for wins.
    """

    def __init__(self, board):
        """
        Initialize the visualizer with a game board.

        Args:
            board: The game board to visualize
        """
        self.board = board
        self.win_positions = []

        # ANSI color codes
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.BLUE = '\033[94m'
        self.YELLOW = '\033[93m'
        self.CYAN = '\033[96m'
        self.MAGENTA = '\033[95m'
        self.RESET = '\033[0m'
        self.BOLD = '\033[1m'
        self.BG_RED = '\033[41m'
        self.BG_GREEN = '\033[42m'

    def find_win_positions(self, symbol):
        """
        Find positions that form a winning line for the given symbol.

        Args:
            symbol: The player symbol to check ('X' or 'O')

        Returns:
            bool: True if a winning line was found, False otherwise
        """
        win_length = 4  # Number of consecutive pieces needed to win
        self.win_positions = []

        # Check horizontally
        for row in range(self.board.size):
            for col in range(self.board.size - win_length + 1):
                if all(self.board.board[row][col + i] == symbol for i in range(win_length)):
                    self.win_positions = [(row, col + i) for i in range(win_length)]
                    return True

        # Check vertically
        for row in range(self.board.size - win_length + 1):
            for col in range(self.board.size):
                if all(self.board.board[row + i][col] == symbol for i in range(win_length)):
                    self.win_positions = [(row + i, col) for i in range(win_length)]
                    return True

        # Check diagonally (top-left to bottom-right)
        for row in range(self.board.size - win_length + 1):
            for col in range(self.board.size - win_length + 1):
                if all(self.board.board[row + i][col + i] == symbol for i in range(win_length)):
                    self.win_positions = [(row + i, col + i) for i in range(win_length)]
                    return True

        # Check diagonally (top-right to bottom-left)
        for row in range(self.board.size - win_length + 1):
            for col in range(win_length - 1, self.board.size):
                if all(self.board.board[row + i][col - i] == symbol for i in range(win_length)):
                    self.win_positions = [(row + i, col - i) for i in range(win_length)]
                    return True

        return False

    def display_win_animation(self, symbol):
        """
        Display a winning animation highlighting the winning line.

        Args:
            symbol: The player symbol that won ('X' or 'O')
        """
        if not self.win_positions:
            self.find_win_positions(symbol)

        if not self.win_positions:
            return

        background = self.BG_RED if symbol == 'X' else self.BG_GREEN

        for _ in range(3):  # Flash the winning line 3 times
            # Display board with highlighted winning positions
            print("   " + " ".join(str(i + 1) for i in range(self.board.size)))
            print("  +" + "-" * self.board.size * 2 + "+")

            for i in range(self.board.size):
                print(f"{i + 1} |", end="")
                for j in range(self.board.size):
                    if (i, j) in self.win_positions:
                        # Highlight winning position
                        print(f"{background}{self.BOLD}{self.board.board[i][j]}{self.RESET}|", end="")
                    else:
                        # Regular position
                        if self.board.board[i][j] == 'X':
                            print(f"{self.RED}{self.BOLD}X{self.RESET}|", end="")
                        elif self.board.board[i][j] == 'O':
                            print(f"{self.GREEN}{self.BOLD}O{self.RESET}|", end="")
                        else:
                            print(f" |", end="")
                print()
                print("  |" + "-" * self.board.size * 2 + "|") if i < self.board.size - 1 else None

            print("  +" + "-" * self.board.size * 2 + "+")
            time.sleep(0.5)  # Wait before toggling highlight

            # Display normal board between flashes
            if _ < 2:  # Skip last normal display
                self.board.display()
                time.sleep(0.3)

        # Show a congratulatory message
        winner = "YOU" if symbol == 'X' else "COMPUTER"
        message = f"{self.MAGENTA}{self.BOLD}★★★ {winner} WIN! ★★★{self.RESET}"
        print("\n" + "=" * len(message))
        print(message)
        print("=" * len(message) + "\n")