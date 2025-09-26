# Cloud class
import pygame
import random

class Cloud:
    def __init__(self, screen_width, screen_height):
        # Random spawn on the right side
        self.x = screen_width + random.randint(0, 200)
        self.y = random.randint(30, screen_height // 5)  # only in top fifth of screen
        self.speed = random.uniform(1, 2.5)  # slower than base/pipes

        # Random size cloud (ellipse)
        self.width = random.randint(40, 100)
        self.height = random.randint(20, 50)

        # light fluffy white-gray color
        self.color = (255, 255, 255) if random.random() > 0.3 else (230, 230, 230)

    def move(self):
        self.x -= self.speed

    def off_screen(self):
        return self.x + 3*self.width < 0

    def draw(self, screen):
        # simple cloud: multiple ellipses overlapping
        pygame.draw.ellipse(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, self.color, (self.x + self.width // 3, self.y - 10, self.width, self.height))
        pygame.draw.ellipse(screen, self.color, (self.x + self.width // 2, self.y, self.width, self.height))