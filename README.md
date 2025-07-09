# Conway's Game of Life

An interactive implementation of Conway's Game of Life with an infinite grid, time travel capabilities, and intuitive controls.

![Game of Life](https://upload.wikimedia.org/wikipedia/commons/e/e5/Gospers_glider_gun.gif)

## 📋 Overview

Conway's Game of Life is a cellular automaton devised by mathematician John Conway in 1970. This implementation features:

- Infinite grid that extends in all directions
- Time travel through generations (forward and backward)
- Adjustable simulation speed
- Pan and zoom functionality
- Clean, minimalist UI

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher
- Pygame library
- Pytest (for running tests)

### Setup

1. Clone this repository:
   ```
   git clone https://github.com/MariusThomassin/GameOfLife.git
   cd GameOfLife
   ```

2. Install dependencies:
   ```
   pip install pygame pytest
   ```

   Or using the Makefile:
   ```
   make install
   ```

## 🎮 Running the Game

### Using Python directly:
```
python main.py
```

### Using the Makefile:
```
make run
```

## 🕹️ Controls

| Action | Control |
|--------|---------|
| Toggle cell state | Left click or Right click |
| Pan the grid | Mouse drag |
| Zoom in/out | Mouse wheel |
| Advance one generation | → button |
| Go back one generation | ← button |
| Auto-play forward | ⇒ button |
| Auto-play backward | ⇐ button |
| Increase simulation speed | + button |
| Decrease simulation speed | - button |

## 📜 Rules of the Game

The Game of Life follows these simple rules:

1. Any live cell with fewer than two live neighbors dies (underpopulation)
2. Any live cell with two or three live neighbors survives
3. Any live cell with more than three live neighbors dies (overpopulation)
4. Any dead cell with exactly three live neighbors becomes alive (reproduction)

Mathematically: Next state = (S = 3) OR (E = 1 AND S = 2)
Where:
- S: Number of live neighbors (integer between 0 and 8)
- E: Current state of the cell (0 for dead, 1 for alive)

## 🧩 Project Structure

- `main.py` - Entry point that calls the main function from src
- `src/` - Source code directory
  - `main.py` - Main application logic
  - `game_of_life.py` - Core game logic and rules
  - `ui.py` - User interface and visualization
- `tests/` - Test suite
  - `test_game_of_life.py` - Tests for game logic
  - `test_ui.py` - Tests for UI components
- `Makefile` - Utility commands for running and maintaining the project

## 🔧 Development

### Running Tests
```
make test
```

### Cleaning cache files
```
make clean
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
