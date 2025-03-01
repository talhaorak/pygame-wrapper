import math
from examples.assets.airplane import Airplane
from examples.assets.utils import get_path
import pygame
from pygame import Vector2
from examples.assets.music_player import MusicPlayer
from examples.assets.parallax_layer import ParallaxLayer
from examples.breakout.types import GameState, Colors
from pygame_wrapper import Game
from pygame_wrapper.config import GameConfig
import os

from pygame_wrapper.rectf import RectF
from pygame_wrapper.update import Update


class AssetsExample(Game):
    def on_init(self):

        # load images
        clouds_img = pygame.image.load(get_path("img/1.png"))
        self.clouds = ParallaxLayer(self, clouds_img, speed=0.5)
        self.add_game_object(self.clouds)
        for i in range(1, 5):
            clouds_img = pygame.image.load(get_path(f"img/{i + 1}.png"))
            self.clouds = ParallaxLayer(self, clouds_img, speed=i)
            self.add_game_object(self.clouds)

        self.airplane = Airplane(self, RectF(0, 300, 32, 32))
        self.add_game_object(self.airplane)

        # load music
        pygame.mixer.init()
        player = MusicPlayer(self)
        self.add_game_object(player)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_running = False

    def on_render(self):
        self.screen.fill((0, 0, 0))


if __name__ == "__main__":
    config = GameConfig(
        width=1365,
        height=768,
        caption='Assets Example',
        fps=120,
    )
    game = AssetsExample(config)
    game.run()
