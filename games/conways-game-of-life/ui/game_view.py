import pygame

from game.config import (
    CELL_SIZE,
    BACKGROUND_COLOR,
    GRID_COLOR,
    ALIVE_COLOR,
)


class GameView:
    def __init__(self, screen, world):
        self.screen = screen
        self.world = world

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        self.draw_grid()
        self.draw_creatures()

    def draw_grid(self):
        for x in range(self.world.width):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (x * CELL_SIZE, 0),
                (x * CELL_SIZE, self.world.height * CELL_SIZE),
            )

        for y in range(self.world.height):
            pygame.draw.line(
                self.screen,
                GRID_COLOR,
                (0, y * CELL_SIZE),
                (self.world.width * CELL_SIZE, y * CELL_SIZE),
            )

    def draw_creatures(self):
        for y in range(self.world.height):
            for x in range(self.world.width):

                creature = self.world.get_creature(x, y)

                if creature is not None:
                    pygame.draw.rect(
                        self.screen,
                        ALIVE_COLOR,
                        (
                            x * CELL_SIZE + 1,
                            y * CELL_SIZE + 1,
                            CELL_SIZE - 2,
                            CELL_SIZE - 2,
                        ),
                    )