from typing import override
from examples.breakout.types import GameState
from pygame_wrapper import GameObject, RectF
import pygame
from pygame import Vector2
import random
import math

from pygame_wrapper.update import Update


class Ball(GameObject):
    def __init__(self, game, pos=Vector2()):
        super().__init__(game, RectF(pos.x, pos.y, 20, 20))
        self.color = (200, 64, 64)
        self.speed = 250
        angle = math.radians(random.randrange(45, 135))
        self.direction = Vector2(math.cos(angle), -math.sin(angle))
        self.max_bounce_rand = 0.1

    @override
    def on_render(self, screen: pygame.Surface):
        center = self.rect.center
        width = self.rect.width
        height = self.rect.height

        # fill
        pygame.draw.circle(screen, self.color, center, width/2)

        # reflection
        pygame.draw.circle(screen, (220, 84, 84), center -
                           Vector2(width/8, height/8), width/4)

        # border
        pygame.draw.circle(screen, (0, 0, 0), center, width/2, 2)
        return super().on_render(screen)

    @override
    def on_update(self, u: Update):
        dt = u.delta
        if self.game.state == GameState.STARTED:
            sw, sh = self.game.width, self.game.height
            d = self.direction * self.speed * dt
            np = Vector2(self.rect.topleft) + d
            if np.x <= 0:
                np.x = 0
                # left wall
                self.bounce(normal=Vector2(1, 0))
            elif np.x >= sw-self.rect.width/2:
                np.x = sw-self.rect.width/2
                # right wall
                self.bounce(normal=Vector2(-1, 0))
            if np.y <= 0:
                np.y = 0
                # top wall
                self.bounce(normal=Vector2(0, 1))
            elif np.y >= sh-self.rect.height/2:
                np.y = sh-self.rect.height/2
                # bottom wall
                self.bounce(normal=Vector2(0, -1))
            self.rect.move_to_ip(np.x, np.y)
        return super().on_update(dt)

    def bounce(self, collision_point=None, normal=None, surface_rect=None):
        """
        Bounce the ball off a surface.

        If a collision_point is provided, the bounce angle is modulated based
        on its offset from the center of surface_rect (suitable for paddle/blocks).
        Otherwise, the reflection is computed using the provided collision normal,
        which is appropriate for screen borders.

        Parameters:
          collision_point: (optional) pygame.math.Vector2 where the ball struck.
          normal: (optional) pygame.math.Vector2 collision normal.
          surface_rect: (optional) pygame.Rect corresponding to the surface hit.
        """
        # For surfaces like screen borders, use normal-based reflection.
        if collision_point is None:
            if normal is None:
                raise ValueError(
                    "Provide a collision normal for a border bounce.")
            self.direction = self.direction.reflect(normal)
        else:
            if surface_rect is None:
                raise ValueError(
                    "A surface_rect is required when using collision_point.")
            # For short surfaces, compute the relative hit position.
            relative = (collision_point.x - surface_rect.centerx) / \
                (surface_rect.width / 2)
            relative = max(-1, min(1, relative))  # Clamp between -1 and 1.
            max_angle = math.radians(60)  # Maximum deflection of 60°.
            bounce_angle = relative * max_angle
            # Assume the ball should always bounce upward from the paddle.
            new_dx = math.sin(bounce_angle)
            new_dy = -math.cos(bounce_angle)
            self.direction = pygame.math.Vector2(new_dx, new_dy).normalize()
