# 9x9 Tic-Tac-Toe with Heuristic Alpha-Beta Search

## Project Overview
This application implements an advanced 9x9 Tic-Tac-Toe game where players compete against an AI opponent powered by heuristic alpha-beta search. The game features a polished console-based user interface with visual enhancements and an intelligent computer opponent that employs strategic decision-making.

## Features
- 9x9 game board (significantly larger than traditional 3x3)
- Win condition: 4 pieces in a row (horizontally, vertically, or diagonally)
- Interactive console-based UI with color highlighting and animations
- Intelligent AI opponent using heuristic alpha-beta pruning
- Clean object-oriented architecture

## Technical Implementation
This project demonstrates the implementation of advanced AI search techniques:
- **Alpha-Beta Pruning**: An optimization of minimax search that eliminates branches that cannot influence the final decision
- **Heuristic Evaluation**: A sophisticated board evaluation function that considers patterns, board control, and blocking strategies
- **Depth-Limited Search**: Allows the AI to look ahead a configurable number of moves while maintaining reasonable performance

## Requirements
- Python 3.8 or higher
- Rich library (`pip install rich`)

## How to Run
1. Ensure all Python files are in the same directory
2. Run the game using: `python main.py`

## Game Instructions
- You play as 'X' and the computer plays as 'O'
- Enter moves as "row,column" (e.g., "3,4") where both values are between 1-9
- Get 4 pieces in a row (horizontally, vertically, or diagonally) to win
- The game board is visually enhanced with colors and highlights

## Code Structure
The project follows a Model-View-Controller architecture:
- **Model**: `GameBoard`, `Player`, `HumanPlayer`, `ComputerPlayer`
- **View**: `GameUI`
- **Controller**: `GameController`, `AIEngine`

### Key Files
- `main.py`: Entry point for the application
- `game_controller.py`: Orchestrates game flow and player interactions
- `game_board.py`: Manages board state and win conditions
- `player.py`: Defines player behaviors (abstract, human, and computer)
- `ai_engine.py`: Implements the heuristic alpha-beta search algorithm
- `ui.py`: Handles all display and user input functionality

## Design Decisions

### Depth Limit Selection
The AI uses a depth limit of 3 for the alpha-beta search, chosen to balance:
- Search depth (deeper searches provide better decisions)
- Performance (9x9 board has many possible positions)
- User experience (response time under 5 seconds)

### Heuristic Function Design
The evaluation function considers multiple strategic factors:
- Pattern recognition: Valuing patterns that could lead to wins
- Board control: Extra value for center and strategic positions
- Blocking: Defensive scoring to prevent opponent wins
