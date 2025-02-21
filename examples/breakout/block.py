import pygame
from pygame import Rect
from pygame_wrapper import GameObject
from pygame_wrapper.rectf import RectF


class Block(GameObject):
    width = 50
    height = 25

    def __init__(self, game, pos, color):
        super().__init__(game, RectF(pos.x, pos.y, Block.width, Block.height))
        self.color = color

    def on_render(self, screen):
        # fill
        pygame.draw.rect(screen, self.color, self.rect.to_pygame())

        # border
        pygame.draw.rect(screen, (0, 0, 0), self.rect.to_pygame(), 2)
        return super().on_render(screen)
