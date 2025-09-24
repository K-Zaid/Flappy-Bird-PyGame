# Game loop and state management
import pygame
from bird import Bird
from base import Base
from pipe import Pipe
from cloud import Cloud
from utils import check_collision, passed_pipe, Button
from leaderboard import top_scores, add_score

class Game:
    def __init__(self):
        # create screen
        pygame.init()
        self.width = 400
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Anivia SkillShot Dodging")
        self.clock = pygame.time.Clock()
        self.state = "menu" # possible states: menu, leaderboard, playing, game_over

        # create game objects
        self.bird = Bird(50, self.height//2 - 10)
        self.base = Base(self.height - 100, 5, self.width)
        self.pipes = [Pipe(self.width, self.base.y)]
        self.clouds = []
        self.cloud_timer = 0

        self.demo_bird = Bird(self.width//2 - 17, self.height//3)
        self.left_demo_pipe = Pipe(self.width//2 - 150, self.base.y, gap=150)
        self.right_demo_pipe = Pipe(self.width//2 + 100, self.base.y, gap=150)

        # helper variables
        self.passed_pipes = []
        self.score = 0

        self.running = True

        # buttons
        font = pygame.font.SysFont("Arial", 30)
        self.start_button = Button(self.width//2 - 60, 250, 120, 50, "Start", font)
        self.leaderboard_button = Button(self.width//2 - 60, 350, 120, 50, "Leaderboard", font)
        self.leaderboard_back_button = Button(0, self.height - 50, 120, 50, "Back", font)
        self.quit_button = Button(self.width//2 - 60, 450, 120, 50, "Quit", font)
        self.restart_button = Button(self.width//2 - 60, 350, 120, 50, "Restart", font)
        self.menu_button = Button(self.width//2 - 60, 450, 120, 50, "Menu", font)

        # variables to get name for leaderboard
        self.name_input_active = False
        self.player_name = ""
        self.input_font = pygame.font.SysFont("Arial", 30)

    def run(self):
        # main game loop skeleton
        while self.running:
            self.clock.tick(60)  # 60 FPS
            self.handle_events() # handle events

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            elif self.state == "playing":
                self.update() # move bird, pipes, base & check collisions
                self.draw() # draw everything
            elif self.state == "game_over":
                self.draw_game_over()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "menu":
                if self.start_button.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.reset_game()
                    self.state = "playing"
                if self.leaderboard_button.is_clicked(event):
                    self.state = "leaderboard"
                if self.quit_button.is_clicked(event):
                    self.running = False
            elif self.state == "leaderboard":
                if self.leaderboard_back_button.is_clicked(event):
                    self.state = "menu"
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()
            elif self.state == "game_over":
                if self.restart_button.is_clicked(event):
                    if self.name_input_active:
                        if self.player_name == "":
                            # save score to database
                            add_score("player", self.score)
                            self.name_input_active = False # disable input box
                        else:
                            # save score to database
                            add_score(self.player_name, self.score)
                            self.name_input_active = False # disable input box
                    self.reset_game()
                    self.state = "playing"
                if self.menu_button.is_clicked(event):
                    if self.name_input_active:
                        if self.player_name == "":
                            # save score to database
                            add_score("player", self.score)
                            self.name_input_active = False # disable input box
                        else:
                            # save score to database
                            add_score(self.player_name, self.score)
                            self.name_input_active = False # disable input box
                    self.state = "menu"

                if self.name_input_active:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.player_name == "":
                                self.player_name = "player"
                            # save score to database
                            add_score(self.player_name, self.score)
                            self.name_input_active = False # disable input box
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            # only allow alphanumeric characters
                            if event.unicode.isalnum():
                                self.player_name += event.unicode


    def update(self):
        self.bird.move()
        self.base.move()

        for pipe in self.passed_pipes + self.pipes:
            pipe.move(self.base.speed)
            # reset pipe when it goes off screen
            if pipe.x < -50:
                self.passed_pipes.remove(pipe)
                self.pipes.append(Pipe(self.width, self.base.y))
        
        # clouds
        self.cloud_timer += 1
        if self.cloud_timer > 90:  # spawn new cloud every 1.5s
            self.clouds.append(Cloud(self.width, self.height))
            self.cloud_timer = 0

        for cloud in self.clouds[:]:
            cloud.move()
            if cloud.off_screen():
                self.clouds.remove(cloud)

        if check_collision(self.bird, self.pipes, self.base.y, self.height):
            self.state = "game_over"
            self.name_input_active = True # add input box to game over screen

        for pipe in self.pipes:
            if self.bird.x < pipe.x:
                break
            if passed_pipe(self.bird, pipe):
                self.score += 1
                self.pipes.remove(pipe)
                self.passed_pipes.append(pipe)

    def draw(self):
        self.screen.fill((135, 206, 250))  # sky blue
        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.bird.draw(self.screen)
        self.base.draw(self.screen)
        for pipe in self.passed_pipes + self.pipes:
            pipe.draw(self.screen)

        # transparent score top middle
        score_font = pygame.font.SysFont("Arial", 40, bold=True)
        score_text = score_font.render(str(self.score), True, (255, 255, 255))
        
        # semi-transparent background for the score
        score_surface = pygame.Surface((score_text.get_width() + 20, score_text.get_height() + 10), pygame.SRCALPHA)
        score_surface.fill((0, 0, 0, 100))  # black with alpha 100 (semi-transparent)
        score_surface.blit(score_text, (10, 5))
        
        # centre score background
        self.screen.blit(score_surface, ((self.width - score_surface.get_width()) // 2, 20))

        # transparent overlay to show hitbox of bird
        rect_surface = pygame.Surface((34, 24), pygame.SRCALPHA)
        rect_surface.fill((200, 200, 200, 120)) 
        self.screen.blit(rect_surface, (self.bird.x, self.bird.y))
        
        pygame.display.update()

    def draw_menu(self):
        self.screen.fill((135, 206, 250))  # sky blue background

        # draw demo bird
        self.demo_bird.draw(self.screen)

        # draw demo pipes (one left, one right)
        self.left_demo_pipe.draw(self.screen)
        self.right_demo_pipe.draw(self.screen)

        # draw base
        self.base.draw(self.screen)

        # title
        font = pygame.font.SysFont("Arial", 40, bold=True)
        title1 = font.render("Anivia SkillShot", True, (255, 255, 255))
        title2 = font.render("Dodging", True, (255, 255, 255))

        # draw each title line
        self.screen.blit(title1, (self.width//2 - title1.get_width()//2, 80))
        self.screen.blit(title2, (self.width//2 - title2.get_width()//2, 130))

        # buttons and hint under start button
        self.start_button.draw(self.screen)

        hint_font = pygame.font.SysFont("Arial", 20)
        hint_text = hint_font.render("or press Space", True, (255, 255, 255))
        self.screen.blit(hint_text, (self.start_button.rect.centerx - hint_text.get_width()//2, self.start_button.rect.bottom + 5))

        self.leaderboard_button.draw(self.screen)
        self.quit_button.draw(self.screen)

        pygame.display.update()

    def draw_game_over(self):
        # draw last frame background as a snapshot
        background = pygame.Surface((self.width, self.height))
        background.fill((135, 206, 250))  # sky blue
        self.bird.draw(background)
        self.base.draw(background)
        for pipe in self.passed_pipes + self.pipes:
            pipe.draw(background)
        self.screen.blit(background, (0, 0))

        # make gray overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)  # 0 = transparent, 255 = opaque
        overlay.fill((50, 50, 50))  # dark gray
        self.screen.blit(overlay, (0, 0))

        # gameover text and score
        font = pygame.font.SysFont("Arial", 50)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        self.screen.blit(game_over_text, (self.width//2 - game_over_text.get_width()//2, 150))

        score_font = pygame.font.SysFont("Arial", 36)
        score_text = score_font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 220))

        # input box
        if self.name_input_active:
            input_box = pygame.Rect(self.width//2 - 100, 275, 200, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), input_box)
            pygame.draw.rect(self.screen, (0, 0, 0), input_box, 2)  # border

            # render current text
            text_surface = self.input_font.render(self.player_name, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        
        # buttons
        self.restart_button.draw(self.screen)
        self.menu_button.draw(self.screen)

        pygame.display.update()

    def reset_game(self):
        self.bird = Bird(50, self.height//2)
        self.base = Base(self.height - 100, 5, self.width)
        self.pipes = [Pipe(self.width, self.base.y)]
        self.passed_pipes = []
        self.score = 0

    def draw_leaderboard(self):
        self.screen.fill((135, 206, 250))

        # demo bird, pipes, base 
        self.demo_bird.draw(self.screen)
        self.left_demo_pipe.draw(self.screen)
        self.right_demo_pipe.draw(self.screen)
        self.base.draw(self.screen)

        # transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))

        # title
        font = pygame.font.SysFont("Arial", 50)
        title = font.render("Leaderboard", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 50))

        # get top scores
        top_ten = top_scores(8)

        score_font = pygame.font.SysFont("Arial", 36)
        for i, (name, score) in enumerate(top_ten):
            text = f"{i+1}. {name} - {score}"
            score_text = score_font.render(text, True, (255, 255, 255))
            self.screen.blit(score_text, (self.width//2 - score_text.get_width()//2, 150 + i*50))

        # back button
        self.leaderboard_back_button.draw(self.screen)

        pygame.display.update()