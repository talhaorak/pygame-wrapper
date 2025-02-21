from collections import deque
from examples.assets.utils import get_path
import pygame
from pygame_wrapper.game_object import GameObject
from pygame_wrapper.rectf import RectF
from pygame_wrapper.update import Update


class Airplane(GameObject):
    def __init__(self, game, rect: RectF):
        img = pygame.transform.scale(pygame.image.load(
            get_path("img/airplane.png")), (rect.width, rect.height))
        img = pygame.transform.rotate(img, -15)
        dark = pygame.Surface(
            (img.get_width(), img.get_height()), flags=pygame.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        img.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self.img = img

        trail_length = 20
        self.trail_positions = deque(maxlen=trail_length)
        center = rect.to_pygame().center
        self.trail_positions.append((center[0], center[1] + 8))
        super().__init__(game, rect)

    def on_init(self):
        # trail

        self.trail_surf = pygame.Surface(
            (self.game.width, self.game.height), flags=pygame.SRCALPHA)

    def on_render(self, screen):
        # draw trail
        self.trail_surf.fill((0, 0, 0, 0))
        if len(self.trail_positions) >= 2:
            num_segments = len(self.trail_positions) - 1
            for i in range(num_segments):
                start = self.trail_positions[i]
                end = self.trail_positions[i + 1]
                # pygame.draw.circle(screen, (255, 255, 255, 255),
                #                    start, 6)

                if num_segments > 1:
                    alpha = int(255 * (i / num_segments))
                else:
                    alpha = 255
                pygame.draw.aaline(self.trail_surf, (255, 255, 255, alpha),
                                   start, end)
        screen.blit(self.trail_surf, (0, 0))

        # draw airplane
        screen.blit(self.img, self.rect.topleft)
        # fade_rect = pygame.Surface(
        #     (self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
        # fade_rect.fill((0, 0, 0, 10))

        return super().on_render(screen)

    def on_update(self, u: Update):
        self.rect.move_ip(1, -0.5)
        # add trail each second
        if u.ticks % 10 == 0:
            center = self.rect.to_pygame().center
            self.trail_positions.append((center[0], center[1] + 8))

        return super().on_update(u)
