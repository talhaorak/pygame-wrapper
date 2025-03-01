from typing import override
import pygame
from pygame_wrapper import Game, GameObject
from pygame_wrapper.config import GameConfig
from pygame_wrapper.rectf import RectF
from pygame_wrapper.update import Update


class BasicGame(Game):
    def on_init(self):
        self.my_object = BasicObject(self)
        self.add_game_object(self.my_object)

    @override
    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.is_running = False

    @override
    def on_update(self, dt):
        pass

    @override
    def on_render(self):
        pass


class BasicObject(GameObject):
    def __init__(self, game):
        super().__init__(game, RectF(game.width//2, game.height//2, 50, 50))
        self.color = (255, 0, 0)
        self.dir = [1, 1]
        self.speed = 100

    @override
    def on_update(self, u: Update):
        mr = self.rect.right
        ml = self.rect.left
        mb = self.rect.bottom
        mt = self.rect.top
        sr = self.game.screen.get_width()
        sb = self.game.screen.get_height()

        if mr >= sr or ml <= 0:
            self.dir[0] *= -1
        if mb >= sb or mt <= 0:
            self.dir[1] *= -1
        self.rect.x += self.dir[0] * self.speed * u.delta
        self.rect.y += self.dir[1] * self.speed * u.delta

    @override
    def on_render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect.to_pygame())


if __name__ == '__main__':
    config = GameConfig(
        width=800,
        height=600,
        caption='Basic Example',
        fps=120,
        bg_color=(30, 30, 30)
    )
    game = BasicGame(config)
    game.run()
