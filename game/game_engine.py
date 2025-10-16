import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.winning_score = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, sounds=None):
        self.ball.move(self.player, self.ai, sounds)

        # Check scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
            if sounds: sounds["score"]()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
            if sounds: sounds["score"]()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner = "Player" if self.player_score >= self.winning_score else "AI"
            text = self.font.render(f"{winner} Wins!", True, WHITE)
            screen.blit(text, (self.width // 2 - 80, self.height // 2 - 60))

            info = self.font.render("Press 3/5/7 for Best Of or ESC to Quit", True, (200, 200, 200))
            screen.blit(info, (self.width // 2 - 230, self.height // 2))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            return True
                        elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                            self.winning_score = int(chr(event.key))
                            self.player_score = 0
                            self.ai_score = 0
                            self.ball.reset()
                            waiting = False
            return False
        return False