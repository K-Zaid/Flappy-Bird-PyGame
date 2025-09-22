# Bird class with jump and gravity mechanics
import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.25 # velocity change of gravity
        self.jump_str = -6 # jump strength 

    def jump(self):
        self.velocity = self.jump_str # bird flap

    def move(self): 
        self.velocity += self.gravity 
        self.y += self.velocity # new position

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 34, 24))  # simple yellow rectangle