# Pipe obstacle logic
import pygame
from utils import get_random_pipe

class Pipe:
    def __init__(self, x, base_height, gap=150):
        self.x = x
        self.width = 52 
        self.top_height, self.gap = get_random_pipe( base_height, gap)

    def move(self, speed):
        self.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, (34,139,34), (self.x, 0, self.width, self.top_height)) # top pipe
        
        pygame.draw.rect(screen, (34,139,34), (self.x, self.top_height + self.gap, self.width, 600)) # bottom pipe