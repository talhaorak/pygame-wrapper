import pygame
import sys

class Game:
    def __init__(self, settings):
        pygame.init()
        self.settings = settings
        width = settings.get('width', 800)
        height = settings.get('height', 600)
        flags = pygame.DOUBLEBUF | pygame.HWACCEL
        self.screen = pygame.display.set_mode((width, height), flags=flags)
        pygame.display.set_caption(settings.get('caption', 'Pygame Game'))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_objects = []  # Hold custom GameObject instances

    def add_game_object(self, game_object):
        self.game_objects.append(game_object)

    def on_init(self):
        """
        Called once before entering the main loop.
        Override for custom initialization.
        """
        pass

    def on_event(self, event):
        """
        Called for each pygame event.
        Override to handle custom events.
        """
        pass

    def on_update(self, dt):
        """
        Called every frame to update game state.
        dt: elapsed time (seconds) since the last frame.
        Override to update your game logic.
        """
        pass

    def on_render(self):
        """
        Called every frame to render the game.
        Override to perform custom drawing.
        """
        pass

    def on_cleanup(self):
        """
        Called once after exiting the main loop.
        Override for any cleanup operations.
        """
        pass

    def run(self):
        """
        Main game loop.
        """
        self.on_init()
        for obj in self.game_objects:
            obj.on_init()

        while self.running:
            dt = self.clock.tick(self.settings.get('fps', 60)) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.on_event(event)
                    for obj in self.game_objects:
                        obj.on_event(event)

            self.on_update(dt)
            for obj in self.game_objects:
                obj.on_update(dt)

            self.screen.fill(self.settings.get('bg_color', (0, 0, 0)))
            self.on_render()
            for obj in self.game_objects:
                obj.on_render(self.screen)
            pygame.display.flip()

        self.on_cleanup()
        for obj in self.game_objects:
            obj.on_cleanup()
        pygame.quit()
        sys.exit()

