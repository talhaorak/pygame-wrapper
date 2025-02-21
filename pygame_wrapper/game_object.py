from pygame import Vector2
import pygame

from pygame_wrapper.game import Game
from pygame_wrapper.update import Update
from .rectf import RectF
from typing import Optional


class GameObject:
    def __init__(self, game: Game, rect: RectF = RectF(0, 0, 0, 0), parent: Optional['GameObject'] = None):

        self.children: list[GameObject] = []
        self.game = game
        self.parent = parent
        self.rect = rect
        self.is_enabled = True

    def add_child(self, child: 'GameObject') -> None:
        """
        Adds a child game object
        """
        child.parent = self
        self.children.append(child)

    def remove_child(self, child: 'GameObject') -> None:
        """
        Removes a game object from children
        """
        child.parent = None
        self.children.remove(child)

    def set_position(self, x, y) -> None:
        """
        Moves the game object's rect
        """
        self.rect.move_ip(x, y)

    def set_enabled(self, yes: bool) -> None:
        """
        Set if the game object continue receive update events
        """
        self.is_enabled = yes

    def position(self) -> Vector2:
        """
        Game object's topleft as pygame.Vector2
        """
        return Vector2(self.rect.topleft)

    def on_init(self):
        """
        Object initialization 
        """
        for child in self.children:
            child.on_init()

    def on_event(self, event: pygame.event.Event) -> None:
        """
        pygame event handler
        """
        for child in self.children:
            child.on_event(event)

    def on_update(self, u: Update) -> None:
        """
        Method for specifying update events
        """
        for child in self.children:
            if child.is_enabled:
                child.on_update(u)

    def on_render(self, screen: pygame.Surface) -> None:
        """
        Method for drawing stuff
        """
        for child in self.children:
            child.on_render(screen)

    def on_cleanup(self) -> None:
        """
        Method for handling clean up logic
        """
        for child in self.children:
            child.on_cleanup()
