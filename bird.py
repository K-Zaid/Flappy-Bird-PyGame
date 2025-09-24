# Bird class with jump and gravity mechanics
import pygame

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.gravity = 0.25 # velocity change of gravity
        self.jump_str = -6 # jump strength 

        self.width = 50
        self.height = 50

        # Load bird frames (replace with your actual sprite paths)
        self.frames = [
            pygame.transform.scale(pygame.image.load("assets/images/frame_0.png").convert_alpha(), (self.width,self.height)),
            pygame.transform.scale(pygame.image.load("assets/images/frame_1.png").convert_alpha(), (self.width,self.height)),
            pygame.transform.scale(pygame.image.load("assets/images/frame_2.png").convert_alpha(), (self.width,self.height)),
            pygame.transform.scale(pygame.image.load("assets/images/frame_3.png").convert_alpha(), (self.width,self.height)),
            pygame.transform.scale(pygame.image.load("assets/images/frame_4.png").convert_alpha(), (self.width,self.height)),
            pygame.transform.scale(pygame.image.load("assets/images/frame_5.png").convert_alpha(), (self.width,self.height))
        ]
        self.frame_index = 0
        self.animation_counter = 0  # controls how fast it animates

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=(self.x-10, self.y))

    def jump(self):
        self.velocity = self.jump_str # bird flap

    def move(self): 
        self.velocity += self.gravity 
        self.y += self.velocity # new position
        self.rect.centery = self.y

        self.animation_counter += 1
        if self.animation_counter >= 7:  # change frame every 7 ticks
            self.animation_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)