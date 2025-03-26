import unittest
import pygame
from unittest.mock import MagicMock, patch
from src.ui import Button, GameUI
from src.game_of_life import GameOfLife

class TestButton(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.action = MagicMock()
        self.button = Button(10, 10, 50, 30, "Test", self.action)

    def test_button_initialization(self):
        """Test button initialization"""
        self.assertEqual(self.button.rect.x, 10)
        self.assertEqual(self.button.rect.y, 10)
        self.assertEqual(self.button.rect.width, 50)
        self.assertEqual(self.button.rect.height, 30)
        self.assertEqual(self.button.text, "Test")
        self.assertEqual(self.button.action, self.action)
        self.assertFalse(self.button.hover)

    def test_check_hover(self):
        """Test button hover detection"""
        self.assertTrue(self.button.check_hover((30, 25)))
        self.assertTrue(self.button.hover)

        self.assertFalse(self.button.check_hover((100, 100)))
        self.assertFalse(self.button.hover)

    def test_handle_click(self):
        """Test button click handling"""
        self.button.handle_click()
        self.action.assert_called_once()

class TestGameUI(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.screen = pygame.Surface((800, 600))
        self.game = GameOfLife()
        self.ui = GameUI(self.game, self.screen)

    def test_initialization(self):
        """Test UI initialization"""
        self.assertEqual(self.ui.cell_size, 20)
        self.assertEqual(self.ui.offset_x, 0)
        self.assertEqual(self.ui.offset_y, 0)
        self.assertFalse(self.ui.dragging)
        self.assertIsNone(self.ui.drag_start)
        self.assertFalse(self.ui.playing_forward)
        self.assertFalse(self.ui.playing_backward)
        self.assertEqual(self.ui.animation_speed, 1.0)
        self.assertEqual(len(self.ui.buttons), 6)

    def test_screen_to_grid_conversion(self):
        """Test screen to grid coordinate conversion"""
        grid_x, grid_y = self.ui.screen_to_grid((100, 80))
        self.assertEqual(grid_x, 5)  # 100 // 20 = 5
        self.assertEqual(grid_y, 4)  # 80 // 20 = 4

        self.ui.offset_x = 30
        self.ui.offset_y = 15
        grid_x, grid_y = self.ui.screen_to_grid((100, 80))
        self.assertEqual(grid_x, 3)  # (100 - 30) // 20 = 3
        self.assertEqual(grid_y, 3)  # (80 - 15) // 20 = 3

    def test_grid_to_screen_conversion(self):
        """Test grid to screen coordinate conversion"""
        screen_x, screen_y = self.ui.grid_to_screen(5, 4)
        self.assertEqual(screen_x, 100)  # 5 * 20 + 0 = 100
        self.assertEqual(screen_y, 80)   # 4 * 20 + 0 = 80

        self.ui.offset_x = 30
        self.ui.offset_y = 15
        screen_x, screen_y = self.ui.grid_to_screen(5, 4)
        self.assertEqual(screen_x, 130)  # 5 * 20 + 30 = 130
        self.assertEqual(screen_y, 95)   # 4 * 20 + 15 = 95

    def test_step_forward(self):
        """Test step forward function"""
        with patch.object(self.game, 'next_generation') as mock_next:
            self.ui.step_forward()
            mock_next.assert_called_once()

    def test_step_backward(self):
        """Test step backward function"""
        with patch.object(self.game, 'previous_generation') as mock_prev:
            self.ui.step_backward()
            mock_prev.assert_called_once()

    def test_toggle_play_forward(self):
        """Test toggling play forward"""
        self.assertFalse(self.ui.playing_forward)
        self.ui.toggle_play_forward()
        self.assertTrue(self.ui.playing_forward)
        self.assertFalse(self.ui.playing_backward)

        # Toggle it off
        self.ui.toggle_play_forward()
        self.assertFalse(self.ui.playing_forward)

    def test_toggle_play_backward(self):
        """Test toggling play backward"""
        self.assertFalse(self.ui.playing_backward)
        self.ui.toggle_play_backward()
        self.assertTrue(self.ui.playing_backward)
        self.assertFalse(self.ui.playing_forward)

        self.ui.toggle_play_backward()
        self.assertFalse(self.ui.playing_backward)

    def test_speed_adjustment(self):
        """Test speed increase and decrease"""
        initial_speed = self.ui.animation_speed

        self.ui.increase_speed()
        self.assertEqual(self.ui.animation_speed, initial_speed + 0.5)

        self.ui.decrease_speed()
        self.assertEqual(self.ui.animation_speed, initial_speed)

        self.ui.animation_speed = 0.5
        self.ui.decrease_speed()
        self.assertEqual(self.ui.animation_speed, 0.5)  # Should not go below 0.5

        self.ui.animation_speed = 99.5
        self.ui.increase_speed()
        self.assertEqual(self.ui.animation_speed, 100.0)  # Should not go above 100.0

if __name__ == '__main__':
    unittest.main()
