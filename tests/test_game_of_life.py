import unittest
from src.game_of_life import GameOfLife

class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.game = GameOfLife()

    def test_toggle_cell(self):
        """Test toggling a cell on and off"""
        self.assertEqual(self.game.get_cell(1, 1), 0)

        self.game.toggle_cell(1, 1)
        self.assertEqual(self.game.get_cell(1, 1), 1)

        self.game.toggle_cell(1, 1)
        self.assertEqual(self.game.get_cell(1, 1), 0)

    def test_count_neighbors(self):
        """Test counting neighbors for a cell"""
        self.game.toggle_cell(0, 0)
        self.game.toggle_cell(1, 0)
        self.game.toggle_cell(0, 1)

        self.assertEqual(self.game.count_neighbors(0, 0), 2)  # Corner cell
        self.assertEqual(self.game.count_neighbors(1, 1), 3)  # Middle cell
        self.assertEqual(self.game.count_neighbors(2, 2), 0)  # Far away cell

    def test_next_generation_rule1(self):
        """Test rule 1: Any live cell with fewer than two live neighbors dies"""
        self.game.toggle_cell(1, 1)
        self.game.next_generation()
        self.assertEqual(self.game.get_cell(1, 1), 0)  # Cell should die

    def test_next_generation_rule2(self):
        """Test rule 2: Any live cell with two or three live neighbors lives"""
        self.game.toggle_cell(0, 0)
        self.game.toggle_cell(1, 0)
        self.game.toggle_cell(0, 1)
        self.game.toggle_cell(1, 1)

        self.game.next_generation()
        self.assertEqual(self.game.get_cell(0, 0), 1)
        self.assertEqual(self.game.get_cell(1, 0), 1)
        self.assertEqual(self.game.get_cell(0, 1), 1)
        self.assertEqual(self.game.get_cell(1, 1), 1)

    def test_next_generation_rule3(self):
        """Test rule 3: Any live cell with more than three live neighbors dies"""
        self.game.toggle_cell(1, 1)  # Center cell

        self.game.toggle_cell(0, 0)
        self.game.toggle_cell(1, 0)
        self.game.toggle_cell(2, 0)
        self.game.toggle_cell(0, 1)

        self.game.next_generation()
        self.assertEqual(self.game.get_cell(1, 1), 0)

    def test_next_generation_rule4(self):
        """Test rule 4: Any dead cell with exactly three live neighbors becomes alive"""
        self.game.toggle_cell(0, 0)
        self.game.toggle_cell(1, 0)
        self.game.toggle_cell(0, 1)

        self.game.next_generation()
        self.assertEqual(self.game.get_cell(1, 1), 1)

    def test_previous_generation(self):
        """Test going back to previous generations"""
        self.assertEqual(self.game.current_gen, 0)

        self.game.toggle_cell(1, 1)
        self.game.next_generation()
        self.assertEqual(self.game.current_gen, 1)

        self.game.previous_generation()
        self.assertEqual(self.game.current_gen, 0)
        self.assertEqual(self.game.get_cell(1, 1), 1)  # Cell should be back

if __name__ == '__main__':
    unittest.main()
