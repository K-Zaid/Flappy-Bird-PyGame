# Helper functions
import pygame
import random

def check_collision(bird, pipes, base_height, screen_height):
    # Bird rectangle
    bird_rect = pygame.Rect(bird.x, bird.y, 34, 24)  # Adjust width/height for sprite size

    # Ground/ceiling collision
    if bird.y <= 0 or bird.y + 24 >= base_height:
        return True

    # Pipe collision
    for pipe in pipes:
        # Top pipe
        top_rect = pygame.Rect(pipe.x, 0, 52, pipe.top_height)
        # Bottom pipe
        bottom_rect = pygame.Rect(pipe.x, pipe.top_height + pipe.gap, 52, screen_height)

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True

    return False


def get_random_pipe(base_height, gap=150):
    # The pipe must leave space between ceiling and base
    max_pipe_height = base_height - gap - 50
    min_pipe_height = 50

    top_height = random.randint(min_pipe_height, max_pipe_height)
    return top_height, gap


def passed_pipe(bird, pipe):
    return pipe.x + 52 < bird.x