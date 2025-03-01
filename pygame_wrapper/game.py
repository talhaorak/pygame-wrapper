import pygame
import sys

from pygame_wrapper.config import GameConfig
from pygame_wrapper.update import Update


class Game:
    def __init__(self, config: GameConfig):
        pygame.init()
        self.config = config
        flags = pygame.DOUBLEBUF | pygame.HWACCEL
        self.screen = pygame.display.set_mode(
            (config.width, config.height), flags=flags)
        pygame.display.set_caption(config.caption)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.ticks = 0
        self.game_objects = []  # Hold custom GameObject instances

    @property
    def width(self) -> int:
        """
        Returns the screen width
        """
        return self.screen.get_width()

    @property
    def height(self) -> int:
        """
        Returns the screen height
        """
        return self.screen.get_height()

    def add_game_object(self, game_object) -> None:
        """
        Adds a game object into the game objects list
        """
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object) -> None:
        """
        Removes given game object from the list
        """
        self.game_objects.remove(game_object)

    def on_init(self) -> None:
        """
        Called once before entering the main loop.
        Override for custom initialization.
        """
        pass

    def on_event(self, event: pygame.event.Event) -> None:
        """
        Called for each pygame event.
        Override to handle custom events.
        """
        pass

    def on_key_pressed(self, keys: list[bool]) -> None:
        """
        Called when a key is pressed.
        Override to handle custom key events.
        """
        pass

    def on_update(self, u: Update) -> None:
        """
        Called every frame to update game state.
        dt: elapsed time (seconds) since the last frame.
        Override to update your game logic.
        """
        pass

    def on_render(self) -> None:
        """
        Called every frame before the game objects, to render the game.
        Override to perform custom drawing.
        """
        pass

    def on_post_render(self) -> None:
        """
        Called every frame after the render of game objects
        """
        pass

    def on_cleanup(self) -> None:
        """
        Called once after exiting the main loop.
        Override for any cleanup operations.
        """
        pass

    def run(self) -> None:
        """
        Main game loop.
        """
        self.on_init()
        for obj in self.game_objects:
            obj.on_init()

        while self.is_running:
            # Event handling
            self._check_events()

            # Update
            self._update()

            # Render
            self._render()

            self.ticks += 1

        self._cleanup()

        pygame.quit()
        sys.exit()

    def _check_events(self):
        keys = pygame.key.get_pressed()
        if len(keys) > 0:
            self.on_key_pressed(keys)
            for obj in self.game_objects:
                obj.on_key_pressed(keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            else:
                self.on_event(event)
                for obj in self.game_objects:
                    obj.on_event(event)

    def _update(self) -> None:
        update = Update(
            time=pygame.time.get_ticks(),
            delta=self.clock.tick(self.config.fps) / 1000.0,
            ticks=self.ticks
        )
        self.on_update(update)

        for obj in self.game_objects:
            if obj.is_enabled:
                obj.on_update(update)

    def _render(self) -> None:
        self.screen.fill(self.config.bg_color)
        self.on_render()
        for obj in self.game_objects:
            obj.on_render(self.screen)
        self.on_post_render()
        pygame.display.flip()

    def _cleanup(self) -> None:
        self.on_cleanup()
        for obj in self.game_objects:
            obj.on_cleanup()
