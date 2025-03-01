from examples.assets.utils import get_path
from pygame_wrapper import GameObject, RectF
import pygame


class MusicPlayer(GameObject):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.music.load(get_path("audio/bg.mp3"))
        pygame.mixer.music.set_volume(0.25)

    def on_init(self):
        pygame.mixer.music.play(-1)
        return super().on_init()

    def on_update(self, dt):
        return super().on_update(dt)
