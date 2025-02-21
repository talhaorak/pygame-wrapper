from typing import override
import pygame
from pygame_wrapper import GameObject, RectF
from pygame import Vector2

from pygame_wrapper.update import Update
from .types import GameState


class Player(GameObject):
    def __init__(self, game, pos=Vector2()):
        super().__init__(game, rect=RectF(pos.x, pos.y, 75, 10))
        self.speed = 200
        self.dir = 0

    @override
    def on_render(self, screen: pygame.Surface):
        # fill
        pygame.draw.rect(screen, (128, 128, 196), self.rect.to_pygame())

        # border
        pygame.draw.rect(screen, (0, 0, 0), self.rect.to_pygame(), 1)

        return super().on_render(screen)

    @override
    def on_event(self, event: pygame.event.Event):
        keys = pygame.key.get_pressed()
        left_pressed = keys[pygame.K_a]
        right_pressed = keys[pygame.K_d]
        if left_pressed:
            self.dir = -1
        elif right_pressed:
            self.dir = 1
        else:
            self.dir = 0
        return super().on_event(event)

    @override
    def on_update(self, u: Update):
        dt = u.delta
        if self.dir != 0:
            if dt == 0:
                dt = 1
            dx = self.dir * self.speed * dt
            nx = self.rect.x + dx

            if nx <= 0:
                nx = 0
            elif nx + self.rect.width >= self.game.width:
                nx = self.game.width - self.rect.width
            dx = nx - self.rect.x
            self.rect.move_ip(dx, 0)
            if self.game.state == GameState.IDLE:
                self.game.ball.rect.move_ip(dx, 0)
        return super().on_update(dt)
