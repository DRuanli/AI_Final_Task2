import pygame
import sys


class PyGameView:
    """
    Pygame-based visualization for the 9x9 Tic-Tac-Toe game.
    Provides a graphical interface for the game.
    """

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    LIGHT_BLUE = (173, 216, 230)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    def __init__(self, board_size=9):
        """Initialize pygame and create window."""
        pygame.init()

        # Screen dimensions
        self.cell_size = 60
        self.board_size = board_size
        self.width = self.cell_size * board_size + 200  # Extra space for info panel
        self.height = self.cell_size * board_size

        # Create screen
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("9x9 Tic-Tac-Toe")

        # Fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 16)

        # Load sounds (optional)
        try:
            self.move_sound = pygame.mixer.Sound('move.wav')
            self.win_sound = pygame.mixer.Sound('win.wav')
            self.sound_enabled = True
        except:
            self.sound_enabled = False

    def draw_board(self, board):
        """
        Draw the game board on the screen.

        Args:
            board: The game board to draw
        """
        # Fill background
        self.screen.fill(self.WHITE)

        # Draw grid
        for i in range(self.board_size + 1):
            # Vertical lines
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.board_size * self.cell_size),
                2 if i % 3 == 0 else 1  # Thicker lines every 3 cells
            )

            # Horizontal lines
            pygame.draw.line(
                self.screen,
                self.BLACK,
                (0, i * self.cell_size),
                (self.board_size * self.cell_size, i * self.cell_size),
                2 if i % 3 == 0 else 1  # Thicker lines every 3 cells
            )

        # Draw X's and O's
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell_content = board.board[row][col]
                if cell_content != ' ':
                    self.draw_symbol(row, col, cell_content)

        # Draw info panel
        self.draw_info_panel()

    def draw_symbol(self, row, col, symbol):
        """
        Draw a symbol (X or O) at the specified position.

        Args:
            row (int): Row index
            col (int): Column index
            symbol (str): Symbol to draw ('X' or 'O')
        """
        center_x = col * self.cell_size + self.cell_size // 2
        center_y = row * self.cell_size + self.cell_size // 2

        if symbol == 'X':
            # Draw X
            offset = self.cell_size // 4
            pygame.draw.line(
                self.screen,
                self.RED,
                (center_x - offset, center_y - offset),
                (center_x + offset, center_y + offset),
                4
            )
            pygame.draw.line(
                self.screen,
                self.RED,
                (center_x + offset, center_y - offset),
                (center_x - offset, center_y + offset),
                4
            )
        else:
            # Draw O
            pygame.draw.circle(
                self.screen,
                self.GREEN,
                (center_x, center_y),
                self.cell_size // 4,
                4
            )

    def draw_info_panel(self):
        """Draw the information panel on the right side of the board."""
        # Draw panel background
        panel_rect = pygame.Rect(
            self.board_size * self.cell_size,
            0,
            200,
            self.height
        )
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, panel_rect)
        pygame.draw.rect(self.screen, self.BLACK, panel_rect, 2)

        # Draw title
        title = self.font.render("Tic-Tac-Toe", True, self.BLACK)
        self.screen.blit(
            title,
            (self.board_size * self.cell_size + 20, 20)
        )

        # Draw instructions
        instructions = [
            "Get 4 in a row to win!",
            "Click to place your mark.",
            "Press 'R' to restart.",
            "Press 'ESC' to quit."
        ]

        for i, text in enumerate(instructions):
            instruction = self.small_font.render(text, True, self.BLACK)
            self.screen.blit(
                instruction,
                (self.board_size * self.cell_size + 20, 70 + i * 30)
            )

    def display_message(self, message, color=BLACK):
        """
        Display a message on the info panel.

        Args:
            message (str): Message to display
            color (tuple): RGB color tuple
        """
        # Clear previous message area
        message_rect = pygame.Rect(
            self.board_size * self.cell_size + 20,
            self.height - 100,
            160,
            80
        )
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, message_rect)

        # Render message (potentially on multiple lines)
        lines = message.split('\n')
        for i, line in enumerate(lines):
            text = self.font.render(line, True, color)
            self.screen.blit(
                text,
                (self.board_size * self.cell_size + 20, self.height - 100 + i * 30)
            )

        pygame.display.flip()

    def highlight_win(self, start_pos, end_pos):
        """
        Highlight the winning line.

        Args:
            start_pos (tuple): (row, col) of start position
            end_pos (tuple): (row, col) of end position
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Convert to pixel coordinates
        start_x = start_col * self.cell_size + self.cell_size // 2
        start_y = start_row * self.cell_size + self.cell_size // 2
        end_x = end_col * self.cell_size + self.cell_size // 2
        end_y = end_row * self.cell_size + self.cell_size // 2

        # Draw highlight line
        pygame.draw.line(
            self.screen,
            self.RED,
            (start_x, start_y),
            (end_x, end_y),
            5
        )

        pygame.display.flip()

        # Play win sound if enabled
        if self.sound_enabled:
            self.win_sound.play()

    def get_cell_from_pos(self, pos):
        """
        Convert mouse position to board cell coordinates.

        Args:
            pos (tuple): (x, y) mouse position

        Returns:
            tuple: (row, col) board coordinates, or None if click was outside board
        """
        x, y = pos

        # Check if click was within board boundaries
        if x < 0 or x >= self.board_size * self.cell_size or y < 0 or y >= self.height:
            return None

        # Convert to board coordinates
        row = y // self.cell_size
        col = x // self.cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return (row, col)

        return None

    def play_move_sound(self):
        """Play sound effect for move if enabled."""
        if self.sound_enabled:
            self.move_sound.play()

    def update(self):
        """Update the display."""
        pygame.display.flip()

    def quit(self):
        """Clean up pygame resources."""
        pygame.quit()