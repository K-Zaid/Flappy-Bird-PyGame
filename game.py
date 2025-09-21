# Game loop and state management
import pygame
from bird import Bird
from base import Base
from pipe import Pipe
from utils import check_collision, passed_pipe

class Game:
    def __init__(self):
        # create screen
        pygame.init()
        self.width = 400
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Anivia SkillShot Dodging")
        self.clock = pygame.time.Clock()

        # create game objects
        self.bird = Bird(50, self.height//2)
        self.base = Base(self.height - 100, 5, self.width)
        self.pipes = [Pipe(self.width, self.base.y)]

        # helper variables
        self.passed_pipes = []
        self.score = 0

        self.running = True

    def run(self):
        # main game loop skeleton
        while self.running:
            self.clock.tick(60)  # 60 FPS
            self.handle_events() # handle events
            self.update() # move bird, pipes, base & check collisions
            self.draw() # draw everything

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bird.jump()

    def update(self):
        self.bird.move()
        self.base.move()

        for pipe in self.passed_pipes + self.pipes:
            pipe.move(self.base.speed)
            # reset pipe when it goes off screen
            if pipe.x < -50:
                self.passed_pipes.remove(pipe)
                self.pipes.append(Pipe(self.width, self.base.y))

        if check_collision(self.bird, self.pipes, self.base.y, self.height):
                print("Game Over")
                print("Score: " + str(self.score))
                self.running = False

        for pipe in self.pipes:
            if self.bird.x < pipe.x:
                break
            if passed_pipe(self.bird, pipe):
                self.score += 1
                self.pipes.remove(pipe)
                self.passed_pipes.append(pipe)

                
        

    def draw(self):
        self.screen.fill((135, 206, 250))  # sky blue
        self.bird.draw(self.screen)
        self.base.draw(self.screen)
        for pipe in self.passed_pipes + self.pipes:
            pipe.draw(self.screen)
        pygame.display.update()