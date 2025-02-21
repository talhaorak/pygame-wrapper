from pygame_wrapper import GameObject, RectF
import pygame


class ParallaxLayer(GameObject):
    def __init__(self, game, image, pos=(0, 0), speed=1):
        super().__init__(game, RectF(pos[0], pos[1], game.width, game.height))
        self.image = image
        self.speed = speed
        self.offset = 0

    def on_render(self, screen):
        screen.blit(pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y))
        screen.blit(pygame.transform.scale(self.image, (self.rect.width,
                    self.rect.height)), (self.rect.x + self.rect.width, self.rect.y))

        return super().on_render(screen)

    def on_update(self, dt):
        self.offset += self.speed
        if self.offset > self.rect.width:
            self.offset = 0

        self.rect.x = -self.offset

        return super().on_update(dt)
