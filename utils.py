# Helper functions and classes
import pygame
import random

def check_collision(bird, pipes, base_height, screen_height):
    # bird rectangle
    bird_rect = pygame.Rect(bird.x, bird.y, 34, 24)  # Adjust width/height for sprite size

    # ground/ceiling collision
    if bird.y <= 0 or bird.y + 24 >= base_height:
        return True

    # pipe collision
    for pipe in pipes:
        # top pipe
        top_rect = pygame.Rect(pipe.x, 0, 52, pipe.top_height)
        # bottom pipe
        bottom_rect = pygame.Rect(pipe.x, pipe.top_height + pipe.gap, 52, screen_height)

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True

    return False


def get_random_pipe(base_height, gap=150):
    # pipe must leave space between ceiling and base
    max_pipe_height = base_height - gap - 50
    min_pipe_height = 50

    top_height = random.randint(min_pipe_height, max_pipe_height)
    return top_height, gap


def passed_pipe(bird, pipe):
    return pipe.x + 52 < bird.x

class Button:
    def __init__(self, x, y, w, h, text, font, color=(255,255,255), hover_color=(200,200,200)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.hover_color if is_hover else self.color
        pygame.draw.rect(screen, color, self.rect)

        # draw text centered
        text_surface = self.font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            if self.rect.collidepoint(event.pos):
                return True
        return False