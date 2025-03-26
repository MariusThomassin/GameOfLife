class GameOfLife:
    def __init__(self):
        self.grid = {}  # Sparse grid representation with coordinates as keys
        self.history = []  # Store previous grid states
        self.current_gen = 0
    
    def toggle_cell(self, x, y):
        """Toggle the state of a cell (0 -> 1, 1 -> 0)"""
        coord = (x, y)
        if coord in self.grid:
            self.grid[coord] = 1 - self.grid[coord]  # Toggle between 0 and 1
        else:
            self.grid[coord] = 1
    
    def get_cell(self, x, y):
        """Get the state of a cell (0 for dead, 1 for alive)"""
        return self.grid.get((x, y), 0)
    
    def count_neighbors(self, x, y):
        """Count the number of live neighbors around a cell"""
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # Skip the cell itself
                if self.get_cell(x + dx, y + dy) == 1:
                    count += 1
        return count

    def next_generation(self):
        """Advance to the next generation following Conway's Game of Life rules"""
        self.history.append(dict(self.grid))

        new_grid = {}

        cells_to_check = set()
        for (x, y) in self.grid:
            if self.grid[(x, y)] == 1:  # If cell is alive
                cells_to_check.add((x, y))
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        cells_to_check.add((x + dx, y + dy))

        for (x, y) in cells_to_check:
            neighbors = self.count_neighbors(x, y)
            current_state = self.get_cell(x, y)

            if current_state == 1:  # Cell is alive
                if neighbors == 2 or neighbors == 3:
                    new_grid[(x, y)] = 1
            else:  # Cell is dead
                if neighbors == 3:
                    new_grid[(x, y)] = 1

        self.grid = new_grid
        self.current_gen += 1  # Increment generation counter by 1 only

    def previous_generation(self):
        """Go back to the previous generation if available"""
        if self.current_gen > 0 and self.history:
            self.grid = self.history.pop()
            self.current_gen -= 1
