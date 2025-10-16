import pygame
import numpy as np
from game.game_engine import GameEngine

# ------------------- Initialize pygame ------------------- #
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)  # stereo

# ------------------- Screen settings ------------------- #
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# ------------------- Colors ------------------- #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------------------- Clock ------------------- #
clock = pygame.time.Clock()
FPS = 60

# ------------------- Sound Generator (Stereo) ------------------- #
def play_tone(frequency=440, duration_ms=150, volume=0.5):
    sample_rate = 44100
    n_samples = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, False)
    wave = np.sin(frequency * 2 * np.pi * t)
    wave = (wave * 32767 * volume).astype(np.int16)
    stereo_wave = np.column_stack((wave, wave))  # make stereo
    sound = pygame.sndarray.make_sound(stereo_wave)
    sound.play()

sounds = {
    "paddle": lambda: play_tone(440, 120),
    "wall": lambda: play_tone(880, 100),
    "score": lambda: play_tone(220, 300)
}

# ------------------- Game Engine ------------------- #
engine = GameEngine(WIDTH, HEIGHT)

# ------------------- Main loop ------------------- #
def main():
    running = True
    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update(sounds)
        engine.render(SCREEN)

        # Check game over
        if engine.check_game_over(SCREEN):
            pass  # Game over handled inside method

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()