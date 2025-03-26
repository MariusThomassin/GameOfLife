import pygame
import time

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hover = False

    def draw(self, surface):
        color = (150, 150, 150) if self.hover else (100, 100, 100)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)

        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

    def handle_click(self):
        self.action()

class GameUI:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.cell_size = 20
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.drag_start = None
        self.playing_forward = False
        self.playing_backward = False
        self.animation_speed = 1.0  # Animations per second
        self.last_update_time = 0

        # Create buttons
        button_width = 50
        button_height = 30
        button_margin = 10
        button_y = self.screen.get_height() - button_height - 10

        self.buttons = [
            Button(10, button_y, button_width, button_height, "<", self.step_backward),
            Button(10 + button_width + button_margin, button_y, button_width, button_height, "->", self.step_forward),
            Button(10 + (button_width + button_margin) * 2, button_y, button_width, button_height, "<=", self.toggle_play_backward),
            Button(10 + (button_width + button_margin) * 3, button_y, button_width, button_height, "=>", self.toggle_play_forward),
            Button(10 + (button_width + button_margin) * 4, button_y, button_width, button_height, "-", self.decrease_speed),
            Button(10 + (button_width + button_margin) * 5, button_y, button_width, button_height, "+", self.increase_speed)
        ]

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                pos = pygame.mouse.get_pos()

                for button in self.buttons:
                    if button.check_hover(pos):
                        button.handle_click()
                        return

                if pos[1] < self.screen.get_height() - 50:
                    self.dragging = True
                    self.drag_start = pos
            elif event.button == 3:  # Right mouse button for toggling cell
                grid_x, grid_y = self.screen_to_grid(pygame.mouse.get_pos())
                self.game.toggle_cell(grid_x, grid_y)
            elif event.button == 4:  # Mouse wheel up - zoom in
                self.cell_size = min(100, self.cell_size + 2)
            elif event.button == 5:  # Mouse wheel down - zoom out
                self.cell_size = max(5, self.cell_size - 2)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button release
                if self.dragging:
                    self.dragging = False
                    current_pos = pygame.mouse.get_pos()
                    if (abs(current_pos[0] - self.drag_start[0]) < 5 and
                        abs(current_pos[1] - self.drag_start[1]) < 5):

                        grid_x, grid_y = self.screen_to_grid(current_pos)
                        self.game.toggle_cell(grid_x, grid_y)

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                dx = event.pos[0] - self.drag_start[0]
                dy = event.pos[1] - self.drag_start[1]
                self.offset_x += dx
                self.offset_y += dy
                self.drag_start = event.pos

            pos = pygame.mouse.get_pos()
            for button in self.buttons:
                button.check_hover(pos)

        elif event.type == pygame.VIDEORESIZE:
            # Update button positions when window is resized
            button_y = event.h - 40
            button_width = 50
            button_margin = 10
            for i, button in enumerate(self.buttons):
                button.rect.x = 10 + (button_width + button_margin) * i
                button.rect.y = button_y

    def screen_to_grid(self, pos):
        """Convert screen coordinates to grid coordinates"""
        grid_x = (pos[0] - self.offset_x) // self.cell_size
        grid_y = (pos[1] - self.offset_y) // self.cell_size
        return grid_x, grid_y

    def grid_to_screen(self, grid_x, grid_y):
        """Convert grid coordinates to screen coordinates"""
        screen_x = grid_x * self.cell_size + self.offset_x
        screen_y = grid_y * self.cell_size + self.offset_y
        return screen_x, screen_y

    def update(self):
        current_time = time.time()
        if (self.playing_forward or self.playing_backward) and current_time - self.last_update_time >= 1.0 / self.animation_speed:
            if self.playing_forward:
                self.game.next_generation()
            elif self.playing_backward:
                self.game.previous_generation()
            self.last_update_time = current_time

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Calculate visible area
        screen_width, screen_height = self.screen.get_size()
        min_x = (0 - self.offset_x) // self.cell_size - 1
        max_x = (screen_width - self.offset_x) // self.cell_size + 1
        min_y = (0 - self.offset_y) // self.cell_size - 1
        max_y = (screen_height - self.offset_y) // self.cell_size + 1

        # Draw grid lines
        for x in range(min_x, max_x + 1):
            screen_x = x * self.cell_size + self.offset_x
            pygame.draw.line(self.screen, (40, 40, 40), (screen_x, 0), (screen_x, screen_height))

        for y in range(min_y, max_y + 1):
            screen_y = y * self.cell_size + self.offset_y
            pygame.draw.line(self.screen, (40, 40, 40), (0, screen_y), (screen_width, screen_y))

        # Draw live cells
        for (x, y), state in self.game.grid.items():
            if state == 1:
                screen_x, screen_y = self.grid_to_screen(x, y)
                if (0 <= screen_x <= screen_width and 0 <= screen_y <= screen_height and
                    screen_x + self.cell_size >= 0 and screen_y + self.cell_size >= 0):
                    pygame.draw.rect(self.screen, (255, 255, 255),
                                     (screen_x, screen_y, self.cell_size, self.cell_size))

        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        # Draw generation counter and speed
        font = pygame.font.SysFont(None, 24)
        gen_text = font.render(f"Generation: {self.game.current_gen}", True, (255, 255, 255))
        speed_text = font.render(f"Speed: {self.animation_speed:.1f} gen/s", True, (255, 255, 255))

        self.screen.blit(gen_text, (10, 10))
        self.screen.blit(speed_text, (10, 40))

    def step_forward(self):
        self.game.next_generation()

    def step_backward(self):
        self.game.previous_generation()

    def toggle_play_forward(self):
        self.playing_forward = not self.playing_forward
        if self.playing_forward:
            self.playing_backward = False
            self.last_update_time = time.time()

    def toggle_play_backward(self):
        self.playing_backward = not self.playing_backward
        if self.playing_backward:
            self.playing_forward = False
            self.last_update_time = time.time()

    def increase_speed(self):
        self.animation_speed = min(100.0, self.animation_speed + 0.5)

    def decrease_speed(self):
        self.animation_speed = max(0.5, self.animation_speed - 0.5)
