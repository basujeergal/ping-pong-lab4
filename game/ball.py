import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self, player, ai, sounds=None):
        """Move the ball and check collisions."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if sounds: sounds["wall"]()

        # Paddle collision
        ball_rect = self.rect()
        if ball_rect.colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x = abs(self.velocity_x)
            self.velocity_y += random.choice([-1, 0, 1])
            if sounds: sounds["paddle"]()
        elif ball_rect.colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x = -abs(self.velocity_x)
            self.velocity_y += random.choice([-1, 0, 1])
            if sounds: sounds["paddle"]()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)