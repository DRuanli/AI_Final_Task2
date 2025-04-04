class GameBoard:
    """
    Class representing the 9x9 Tic-Tac-Toe game board.
    Handles board state management and win condition checking.
    """

    def __init__(self):
        """Initialize an empty 9x9 board."""
        self.board = [[' ' for _ in range(9)] for _ in range(9)]
        self.size = 9
        self.win_length = 4  # Number of consecutive pieces needed to win

    def make_move(self, row, col, symbol):
        """
        Place a symbol ('X' or 'O') at the specified position.

        Args:
            row (int): Row index (0-8)
            col (int): Column index (0-8)
            symbol (str): Player symbol ('X' or 'O')

        Returns:
            bool: True if move was successful, False if position is already taken
        """
        if 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' ':
            self.board[row][col] = symbol
            return True
        return False

    def check_win(self, symbol):
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

    def is_full(self):
        """
        Check if the board is full.

        Returns:
            bool: True if all positions are filled, False otherwise
        """
        return all(self.board[row][col] != ' ' for row in range(self.size) for col in range(self.size))

    def get_empty_positions(self):
        """
        Return a list of empty positions.

        Returns:
            list: List of (row, col) tuples representing empty positions
        """
        return [(row, col) for row in range(self.size) for col in range(self.size) if self.board[row][col] == ' ']

    def display(self):
        """Display the board in the console."""
        # Display column numbers
        print("   " + " ".join(str(i + 1) for i in range(self.size)))
        print("  +" + "-" * self.size * 2 + "+")

        # Display board with row numbers
        for i in range(self.size):
            print(f"{i + 1} |", end="")
            for j in range(self.size):
                print(f"{self.board[i][j]}|", end="")
            print()
            if i < self.size - 1:
                print("  |" + "-" * self.size * 2 + "|")

        print("  +" + "-" * self.size * 2 + "+")

    def get_board_copy(self):
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