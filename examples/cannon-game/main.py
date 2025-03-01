from typing import override
import pygame
from pygame_wrapper import Game, GameObject
from pygame_wrapper.config import GameConfig
from pygame_wrapper.rectf import RectF
from pygame_wrapper.update import Update
from pygame_wrapper.colors import Colors
from typing import Optional
import random
import math


class CannonGame(Game):
    @override
    def on_init(self):
        self.world = World(self)
        self.players = [
            Player(self, "Player 1", (10, 650)),
            Player(self, "Player 2", (964, 650))
        ]
        self.turn = self.players[0]
        self.add_game_object(self.world)
        for player in self.players:
            self.add_game_object(player)

        self.cannon_ball: Optional[CannonBall] = None

    @override
    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_running = False
            elif event.key == pygame.K_SPACE:
                if self.cannon_ball is None:
                    self.shoot()
        return super().on_event(event)

    @override
    def on_update(self, u: Update):
        if self.cannon_ball is not None:
            if self.cannon_ball.rect.colliderect(self.world.ground_rect):
                self.kill_cannon_ball(self.cannon_ball)

        pass

    @override
    def on_render(self):
        pass

    def kill_cannon_ball(self, cannon_ball: 'CannonBall'):
        self.remove_game_object(cannon_ball)
        self.cannon_ball = None

    def shoot(self):
        cb_pos = self.turn.TIP_POS
        angle = self.turn.cannon_angle
        speed = self.turn.power
        cannon_ball = CannonBall(self, cb_pos, angle, speed)
        self.add_game_object(cannon_ball)
        self.turn = self.players[1] if self.turn == self.players[0] else self.players[0]
        self.cannon_ball = cannon_ball


class World(GameObject):
    @override
    def on_init(self):
        self.cloud = Cloud(self.game, (200, 50))
        self.add_child(self.cloud)
        self.cloud2 = Cloud(self.game, (600, 100))
        self.add_child(self.cloud2)
        self.wind_speed = pygame.Vector2(0.1, 0)
        self.sky_color = pygame.color.THECOLORS['deepskyblue']

        self.ground_rect = pygame.Rect(0, 700, 1024, 86)
        super().on_init()

    @override
    def on_render(self, screen):
        # Create a surface from screen
        surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # Draw the sky first
        surf.fill(self.sky_color)
        # Draw the ground
        pygame.draw.rect(surf, (139, 69, 19), self.ground_rect)
        # Draw the sun
        pygame.draw.circle(surf, (255, 255, 0), (100, 100), 20)
        super().on_render(surf)
        screen.blit(surf, (0, 0))

    @override
    def on_update(self, u: Update):
        for child in self.children:
            if isinstance(child, Cloud):
                child.rect.move_ip(self.wind_speed.x, self.wind_speed.y)
                if child.rect.left > 1024:
                    child.rect.right = 0
                elif child.rect.right < 0:
                    child.rect.left = 1024
        super().on_update(u)


class Cloud(GameObject):
    def __init__(self, game, position):
        """Initialize the Cloud with a position and pre-render its appearance."""

        width = 200  # Width of the cloud surface
        height = 100  # Height of the cloud surface
        super().__init__(game, RectF(position[0], position[1], width, height))
        # Create a surface with per-pixel alpha for transparency
        self.surface = pygame.Surface(
            (width, height), pygame.SRCALPHA)

        # Define base x-positions for cloud clusters
        cluster_bases = [50, 100, 150]
        for base_x in cluster_bases:
            # Randomize cluster center for a natural look
            cluster_center = (
                base_x + random.randint(-10, 10),
                50 + random.randint(-10, 10)
            )

            for i in range(10):
                # Random offsets from cluster center
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-20, 20)
                ellipse_center = (
                    cluster_center[0] + offset_x,
                    cluster_center[1] + offset_y
                )
                # Random ellipse dimensions (elongated horizontally)
                ellipse_width = random.randint(30, 60)
                ellipse_height = random.randint(20, 40)
                # Random alpha for transparency
                alpha = random.randint(30, 150)
                color = (255, 255, 255, alpha)  # White with varying alpha
                # Calculate bounding rectangle for the ellipse
                left = int(ellipse_center[0] - ellipse_width / 2)
                top = int(ellipse_center[1] - ellipse_height / 2)
                rect = (left, top, ellipse_width, ellipse_height)
                # Draw ellipse on the cloud surface
                pygame.draw.ellipse(self.surface, color, rect)

    def on_render(self, screen):
        """Render the cloud on the provided Pygame surface."""
        screen.blit(self.surface, self.rect.topleft)


class Player(GameObject):
    CANNON_LENGTH = 50
    CANNON_HEIGHT = 10

    def __init__(self, game: CannonGame, name: str, pos: tuple[int, int]):
        rect = RectF(pos[0], pos[1], 50, 50)
        super().__init__(game, rect)
        self.name = name
        self.cannon_angle = 90
        self.power = 1
        self.hp = 100

        self.PIVOT_POS = self.rect.center
        self.TIP_POS = (self.PIVOT_POS[0] + Player.CANNON_LENGTH,
                        self.PIVOT_POS[1] - Player.CANNON_HEIGHT / 2)
        # Create original cannon surface
        cannon_surface = pygame.Surface(
            (Player.CANNON_LENGTH, Player.CANNON_HEIGHT), pygame.SRCALPHA)

        cannon_surface.fill(Colors.GRAY.value)
        self.cannon_surface = cannon_surface

    @override
    def on_key_pressed(self, keys):
        if self.game.turn == self:
            if keys[pygame.K_UP]:
                self.power = min(100, self.power + 0.1)
            elif keys[pygame.K_DOWN]:
                self.power = max(1, self.power - 0.1)

            self.cannon_angle += 1 * \
                (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT])
            self.cannon_angle = max(45, min(135, self.cannon_angle))
        return super().on_key_pressed(keys)

    def on_render(self, screen: pygame.Surface) -> None:
        # draw the base
        pygame.draw.rect(screen, (0, 200, 0), self.rect.to_pygame())

        if self.game.turn == self:
            self._render_cannon(screen)

        # draw the name
        font = pygame.font.Font(None, 24 if self.game.turn == self else 18)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.rect.centerx, self.rect.bottom + 10))
        screen.blit(text, text_rect)

    def _render_cannon(self, screen) -> None:

        self.cannon_surface.fill(Colors.GRAY.value)
        #  Draw a rect to represent the power
        pygame.draw.rect(self.cannon_surface, Colors.RED.value,
                         (0, 0, self.power, Player.CANNON_HEIGHT))

        # Rotate the cannon
        rotated_cannon = pygame.transform.rotate(
            self.cannon_surface, self.cannon_angle)  # Negative for clockwise rotation

        # Get the original center and pivot position relative to it
        orig_center = (Player.CANNON_LENGTH / 2, Player.CANNON_HEIGHT / 2)
        # Left center in original surface
        pivot_local = (0, Player.CANNON_HEIGHT / 2)
        # Right center in original surface
        tip_local = (Player.CANNON_LENGTH, Player.CANNON_HEIGHT / 2)
        vector_to_pivot = (pivot_local[0] - orig_center[0],
                           pivot_local[1] - orig_center[1])  # (-w/2, 0)
        tip_vector = (tip_local[0] - orig_center[0],
                      tip_local[1] - orig_center[1])

        # Rotate the vector
        rad = math.radians(-self.cannon_angle)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)
        rotated_vector_x = vector_to_pivot[0] * \
            cos_val - vector_to_pivot[1] * sin_val
        rotated_vector_y = vector_to_pivot[0] * \
            sin_val + vector_to_pivot[1] * cos_val

        tip_rot_x = tip_vector[0] * cos_val - tip_vector[1] * sin_val
        tip_rot_y = tip_vector[0] * sin_val + tip_vector[1] * cos_val

        # Position the rotated surface so the pivot stays at PIVOT_POS
        rotated_rect = rotated_cannon.get_rect()
        pivot_in_rotated = (rotated_rect.width / 2 + rotated_vector_x,
                            rotated_rect.height / 2 + rotated_vector_y)

        tip_in_rotated = (rotated_rect.width / 2 + tip_rot_x,
                          rotated_rect.height / 2 + tip_rot_y)
        blit_pos = (self.PIVOT_POS[0] - pivot_in_rotated[0],
                    self.PIVOT_POS[1] - pivot_in_rotated[1])
        tip_pos = (blit_pos[0] + tip_in_rotated[0],
                   blit_pos[1] + tip_in_rotated[1])
        self.TIP_POS = tip_pos

        screen.blit(rotated_cannon, blit_pos)

        # draw the pivot
        pygame.draw.circle(screen, Colors.RED.value, self.PIVOT_POS, 5)

        # draw the angle
        pygame.draw.arc(screen, Colors.RED.value, (self.rect.left - 50, self.rect.top -
                                                   50, 100, 100),  math.radians(-self.cannon_angle), 0)

        # draw the angle text
        font = pygame.font.Font(None, 18)
        text = font.render(str(self.cannon_angle), True, (255, 255, 255))
        text_rect = text.get_rect(
            center=(self.rect.centerx, self.rect.top - 30))
        screen.blit(text, text_rect)


class CannonBall(GameObject):
    def __init__(self, game: CannonGame, pos: tuple[int, int], angle: float, speed: float):
        super().__init__(game, RectF(pos[0], pos[1], 10, 10))
        self.angle = angle
        self.speed = speed/5
        self.gravity = 0.1

    @override
    def on_render(self, screen):
        pygame.draw.circle(screen, Colors.BLACK.value, self.rect.center, 5)
        return super().on_render(screen)

    @override
    def on_update(self, u):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * \
            math.sin(math.radians(self.angle)) - self.gravity
        self.gravity += 0.1
        if self.rect.y > 800:
            self.kill()
        return super().on_update(u)

    def kill(self):
        self.game.kill_cannon_ball(self)


if __name__ == '__main__':
    config = GameConfig(
        width=1024,
        height=786,
        caption='Basic Example',
        fps=120,
        bg_color=(30, 30, 30)
    )
    game = CannonGame(config)
    game.run()
