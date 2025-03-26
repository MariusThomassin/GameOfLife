import pygame
import sys
from src.game_of_life import GameOfLife
from src.ui import GameUI

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")

    game = GameOfLife()
    ui = GameUI(game, screen)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            ui.handle_event(event)

        ui.update()
        ui.draw()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
