# Game loop and state management
import pygame
import random
import time
from bird import Bird
from base import Base
from pipe import Pipe
from cloud import Cloud
from utils import check_collision, passed_pipe, Button
from leaderboard import top_scores, add_score
from power import Power

class Game:
    def __init__(self):
        # create screen
        pygame.init()
        self.width = 400
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Anivia SkillShot Dodging")
        self.clock = pygame.time.Clock()
        self.state = "menu" # possible states: menu, info, leaderboard, playing, game_over

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

        # game is running
        self.running = True

        # buttons
        font = pygame.font.SysFont("Arial", 30)
        self.info_button = Button(0, 0, 40, 40, "i", pygame.font.SysFont("Segoe Script", 30))
        self.start_button = Button(self.width//2 - 60, 250, 120, 50, "Start", font)
        self.leaderboard_button = Button(self.width//2 - 60, 350, 120, 50, "Leaderboard", font)
        self.back_button = Button(0, self.height - 40, 90, 40, "Back", font)
        self.quit_button = Button(self.width//2 - 60, 450, 120, 50, "Quit", font)
        self.restart_button = Button(self.width//2 - 60, 350, 120, 50, "Restart", font)
        self.menu_button = Button(self.width//2 - 60, 450, 120, 50, "Menu", font)

        # variables to get name for leaderboard
        self.name_input_active = False
        self.player_name = ""
        self.input_font = pygame.font.SysFont("Arial", 30)

        # list of active buffs + debuffs
        self.active_powers = []
        self.active_powers_names = []

        # helper variable for buffs + debuffs
        self.x2points = False
        self.invisible = False
        self.manual = False
        self.tiny_gap = False
        
        # load and scale modifier icons
        ICON_SIZE = (32, 32)  # (width, height)

        self.modifier_icons = {
            "invincible": pygame.transform.scale(pygame.image.load("assets/images/invincible.png").convert_alpha(), ICON_SIZE),
            "shield": pygame.transform.scale(pygame.image.load("assets/images/shield.png").convert_alpha(), ICON_SIZE),
            "slowmo": pygame.transform.scale(pygame.image.load("assets/images/slowmo.png").convert_alpha(), ICON_SIZE),
            "x2points": pygame.transform.scale(pygame.image.load("assets/images/x2points.png").convert_alpha(), ICON_SIZE),
            "jump_boost": pygame.transform.scale(pygame.image.load("assets/images/jump_boost.png").convert_alpha(), ICON_SIZE),
            "rev_grav": pygame.transform.scale(pygame.image.load("assets/images/rev_grav.png").convert_alpha(), ICON_SIZE),
            "manual": pygame.transform.scale(pygame.image.load("assets/images/manual.png").convert_alpha(), ICON_SIZE),
            "heavy": pygame.transform.scale(pygame.image.load("assets/images/heavy.png").convert_alpha(), ICON_SIZE),
            "tiny_gap": pygame.transform.scale(pygame.image.load("assets/images/tiny_gap.png").convert_alpha(), ICON_SIZE),
            "fast_pipes": pygame.transform.scale(pygame.image.load("assets/images/fast_pipes.png").convert_alpha(), ICON_SIZE),
            "disappearing_pipes": pygame.transform.scale(pygame.image.load("assets/images/disappearing_pipes.png").convert_alpha(), ICON_SIZE),
        }

        # dictionary of explanations
        self.modifier_info = {
            "invincible": "Cannot collide with objects while active.",
            "shield": "Protects you from one hit, on hit: invincible for 2 seconds.",
            "slowmo": "Pipe move speed reduced.",
            "x2points": "Double points for passing pipes.",
            "jump_boost": "Flap power increased.",
            "rev_grav": "Gravity acts upwards, jumping pushes you down.",
            "manual": "Use up and down arrows to move respectively.",
            "heavy": "Gravity increased.",
            "tiny_gap": "Smaller gaps in pipes.",
            "fast_pipes": "Pipe move speed increased.",
            "disappearing_pipes": "Pipes vanish and appear again when close to you.",
        }


    def run(self):
        # main game loop skeleton
        while self.running:
            self.clock.tick(60)  # 60 FPS
            self.handle_events() # handle events

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "leaderboard":
                self.draw_leaderboard()
            elif self.state == "info":
                self.draw_info()
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
                if self.info_button.is_clicked(event):
                    self.state = "info"
                if self.quit_button.is_clicked(event):
                    self.running = False
            elif self.state == "leaderboard":
                if self.back_button.is_clicked(event):
                    self.state = "menu"
            elif self.state == "info":
                if self.back_button.is_clicked(event):
                    self.state = "menu"
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN and not self.manual:
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

        if self.manual and self.state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.bird.y -= 5   # move up
                self.bird.rect.centery = self.bird.y
            if keys[pygame.K_DOWN]:
                self.bird.y += 5   # move down
                self.bird.rect.centery = self.bird.y

    def update(self):
        if not self.manual:
            self.bird.move(self.base.y)
        self.base.move()

        for pipe in self.passed_pipes + self.pipes:
            pipe.move(self.base.speed)
            # reset pipe when it goes off screen
            if pipe.x < -50:
                self.passed_pipes.remove(pipe)
                if self.tiny_gap:
                    self.pipes.append(Pipe(self.width, self.base.y, 100))
                else:
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

        if check_collision(self.bird, self.pipes, self.base.y, self.height) and self.bird.shield and not self.bird.invincible:
            index = next((i for i, p in enumerate(self.active_powers) if p.type == "shield"), None)
            if index is not None:
                self.active_powers.pop(index)
                self.active_powers_names.pop(index)
            self.remove_power("shield")
            
            self.active_powers.append(Power("invincible", 2))
            self.active_powers_names.append("invincible")
            self.apply_power("invincible")

        elif check_collision(self.bird, self.pipes, self.base.y, self.height) and not self.bird.invincible:
            self.state = "game_over"
            self.name_input_active = True # add input box to game over screen

            # reset modifiers
            self.active_powers = []
            self.active_powers_names = []
            self.x2points = False
            self.invisible = False
            self.manual = False
            self.tiny_gap = False

        for pipe in self.pipes:
            if self.bird.x < pipe.x:
                break
            if passed_pipe(self.bird, pipe):
                if self.x2points:
                    self.score += 2
                else:
                    self.score += 1
                self.pipes.remove(pipe)
                self.passed_pipes.append(pipe)

                prob = 0.25

                if self.score > 500:
                    prob = 0.4
                elif self.score > 100:
                    prob = 0.3

                if len(self.active_powers) < 1 + self.score//30: 
                    # maximum possible new powerups
                    max_new = min(
                        (1 + self.score // 30) - len(self.active_powers),
                        11 - len(self.active_powers)
                    )

                    count = 0
                    while count < max_new and random.random() < min(prob + count*0.05, 0.7):
                        available = [
                            p for p in ["invincible", "shield", "slowmo", "x2points",
                                        "jump_boost", "rev_grav", "manual",
                                        "heavy", "tiny_gap", "fast_pipes",
                                        "disappearing_pipes"]
                            if p not in self.active_powers_names
                        ]

                        if not available:  # no unique powers left
                            break

                        chosen = random.choice(available)
                        duration = 9999 if chosen == "shield" else 8
                        self.active_powers.append(Power(chosen, duration))
                        self.active_powers_names.append(chosen)
                        self.apply_power(chosen)

                        count += 1

        for power in self.active_powers:
            if power.expired():
                self.remove_power(power.type)
                self.active_powers.remove(power)
                self.active_powers_names.remove(power.type)

    def apply_power(self, pwr):
        if pwr == "invincible":
            self.bird.invincible = True
        elif pwr == "shield":
            self.bird.shield = True
        elif pwr == "slowmo":
            self.base.speed /= 2
        elif pwr == "x2points":
            self.x2points = True
        elif pwr == "jump_boost":
            self.bird.jump_str *= 1.35
        elif pwr == "rev_grav":
            self.bird.gravity *= -1
            self.bird.jump_str *= -1
        elif pwr == "manual":
            self.manual = True
        elif pwr == "heavy":
            self.bird.gravity *= 2
        elif pwr == "tiny_gap":
            self.tiny_gap = True
        elif pwr == "fast_pipes":
            self.base.speed *= 1.5
        elif pwr == "disappearing_pipes":
            self.invisible = True        

    def remove_power(self, pwr):
        if pwr == "invincible":
            self.bird.invincible = False
        elif pwr == "shield":
            self.bird.shield = False
        elif pwr == "slowmo":
            self.base.speed *= 2
        elif pwr == "x2points":
            self.x2points = False
        elif pwr == "jump_boost":
            self.bird.jump_str /= 1.35
        elif pwr == "rev_grav":
            self.bird.gravity *= -1
            self.bird.jump_str *= -1
        elif pwr == "manual":
            self.manual = False
        elif pwr == "heavy":
            self.bird.gravity /= 2
        elif pwr == "tiny_gap":
            self.tiny_gap = False
        elif pwr == "fast_pipes":
            self.base.speed /= 1.5
        elif pwr == "disappearing_pipes":
            self.invisible = False   

    def draw(self):
        self.screen.fill((135, 206, 250))  # sky blue
        for cloud in self.clouds:
            cloud.draw(self.screen)
        self.bird.draw(self.screen)
        self.base.draw(self.screen)
        for pipe in self.passed_pipes + self.pipes:
            if self.invisible and pipe.x > 60 and pipe.x < 300:
                continue
            else:
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

        # draw active modifier icons
        x, y = 10, 10   # start position (top-left corner)
        spacing = 42    # space between icons

        for i, modifier in enumerate(self.active_powers):
            if modifier.type in self.modifier_icons:
                time_left = modifier.time_left()

                if time_left <= 2:
                    # blink on/off every 0.3s
                    if int(time.time() * 3) % 2 == 0:
                        continue  # skip drawing this frame 
                
                self.screen.blit(self.modifier_icons[modifier.type], (x, y + i * spacing))
        
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
        self.info_button.draw(self.screen)
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
        self.back_button.draw(self.screen)

        pygame.display.update()

    def draw_info(self):
        self.screen.fill((135, 206, 250))

        # transparent overlay for readability
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((50, 50, 50))
        self.screen.blit(overlay, (0, 0))

        # title
        font = pygame.font.SysFont("Arial", 40, bold=True)
        title = font.render("Modifier Info", True, (255, 255, 255))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 20))

        # draw icons + text in a vertical list
        y = 75
        spacing = 45
        text_font = pygame.font.SysFont("Arial", 15)

        for name, icon in self.modifier_icons.items():
            # icon
            self.screen.blit(icon, (10, y))

            # description
            description = self.modifier_info.get(name, "")
            text_surface = text_font.render(f"{description}", True, (255, 255, 255))
            self.screen.blit(text_surface, (45, y + 5))

            y += spacing

        # back button
        self.back_button.draw(self.screen)

        hint1 = "-Shield lasts for 1 hit, other modifiers last for 8 seconds"
        hint2 = "-Icons will start blinking 2 seconds before expiring"

        surf1 = text_font.render(hint1, True, (255, 255, 255))
        surf2 = text_font.render(hint2, True, (255, 255, 255))

        # position next to back button
        a = self.back_button.rect.right + 5  

        # align hint1 with top half
        b1 = self.back_button.rect.top + self.back_button.rect.height // 4 - surf1.get_height() // 2
        # align hint2 with bottom half
        b2 = self.back_button.rect.bottom - self.back_button.rect.height // 4 - surf2.get_height() // 2

        self.screen.blit(surf1, (a, b1))
        self.screen.blit(surf2, (a, b2))


        pygame.display.update()