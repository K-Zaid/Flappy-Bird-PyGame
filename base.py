# Ground / scrolling background logic
import pygame

class Base:
    def __init__(self, y, speed, width):
        self.y = y
        self.speed = speed # speed of scrollibg
        self.width = width
        self.x1 = 0
        self.x2 = width  # width of base image

    def move(self):
        self.x1 -= self.speed
        self.x2 -= self.speed
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width
        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self, screen):
        pygame.draw.rect(screen, (222, 184, 135), (self.x1, self.y, self.width, 100)) 
        pygame.draw.rect(screen, (222, 184, 135), (self.x2, self.y, self.width, 100)) # brown rectangles