import pygame
from pygame_wrapper import Game, GameObject

class BasicGame(Game):
    def on_init(self):
        self.my_object = BasicObject(self)
        self.add_game_object(self.my_object)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.running = False

    def on_update(self, dt):
        pass

    def on_render(self):
        pass

class BasicObject(GameObject):
    def __init__(self, game):
        super().__init__(game)
        self.position = [self.game.screen.get_width()/2, self.game.screen.get_height()/2]
        self.color = (255, 0, 0)
        self.rect = pygame.Rect(*self.position, 50, 50)
        self.dir = [1, 1] 
        self.speed = 100

    def on_update(self, dt):
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
        self.rect.x += self.dir[0] * self.speed * dt
        self.rect.y += self.dir[1] * self.speed * dt

    def on_render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

if __name__ == '__main__':
    settings = {
        'width': 800,
        'height': 600,
        'caption': 'Basic Pygame Wrapper Example',
        'fps': 120,
        'bg_color': (30, 30, 30)
    }
    game = BasicGame(settings)
    game.run()

