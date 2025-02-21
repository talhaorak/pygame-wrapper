import pygame
from pygame import Vector2
from examples.breakout.types import GameState, Colors
from pygame_wrapper import Game
from pygame_wrapper.config import GameConfig
from .ball import Ball
from .player import Player
from .block import Block


class BreakoutGame(Game):
    def on_init(self):

        sw, sh = self.width, self.height
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 36)

        uw, uh = sw/6, sh/6
        self.state = GameState.IDLE
        player = Player(self)
        player.set_position(sw/2 - player.rect.width/2, 5*uh)
        self.player = player

        ball = Ball(self)
        ball.set_position(player.rect.centerx - ball.rect.width /
                          2, player.rect.top - ball.rect.height)
        self.ball = ball
        self.add_game_object(self.player)
        self.add_game_object(self.ball)

        # blocks 10 x 5
        row_count, col_count = 5, 10
        x_offset, y_offset = sw//2 - (col_count * (Block.width+2))//2, uh
        blocks = []
        colors_list = [Colors.RED, Colors.GREEN,
                       Colors.BLUE, Colors.YELLOW, Colors.CYAN]

        for row in range(row_count):
            for col in range(col_count):
                block = Block(self, Vector2(x_offset + col * (Block.width+2),
                                            y_offset + row * (Block.height+2)), colors_list[row].value)
                blocks.append(block)
                self.add_game_object(block)

        self.curtain = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.curtain.fill((0, 0, 0, 196))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_running = False
            elif self.state == GameState.IDLE and event.key == pygame.K_SPACE:
                self.state = GameState.STARTED

    def on_update(self, dt):
        if self.state == GameState.STARTED:
            if self.ball.rect.bottom >= self.height:
                self.set_game_over()
            self.check_collisions()

    def check_collisions(self):
        player_cp = self.ball.rect.colliderect_point(self.player.rect)
        if player_cp is not None:
            self.ball.bounce(collision_point=player_cp,
                             surface_rect=self.player.rect)

        for block in self.game_objects:
            if not isinstance(block, Block):
                continue
            block_cp = self.ball.rect.colliderect_point(block.rect)
            if block_cp is not None:
                block_cp_vec = Vector2(block_cp)
                self.ball.bounce(collision_point=block_cp_vec,
                                 surface_rect=block.rect)
                self.remove_game_object(block)

    def on_post_render(self):
        if self.state == GameState.IDLE:
            self.screen.blit(self.curtain, (0, 0))
            font_tex = self.font.render(
                "Press <space> to start", True, Colors.WHITE.value)
            text_rec = font_tex.get_rect(
                center=(self.width//2, self.height//2))
            self.screen.blit(font_tex, text_rec)
        elif self.state == GameState.GAMEOVER:
            self.screen.blit(self.curtain, (0, 0))
            font_tex = self.font.render("Game Over", True, Colors.WHITE.value)
            text_rec = font_tex.get_rect(
                center=(self.width//2, self.height//2))
            self.screen.blit(font_tex, text_rec)

    def set_game_over(self):
        self.state = GameState.GAMEOVER
        self.ball.set_enabled(False)
        self.player.set_enabled(False)


if __name__ == "__main__":
    config = GameConfig(
        width=800,
        height=600,
        caption='Breakout Game',
        fps=60,
    )
    game = BreakoutGame(config)
    game.run()
