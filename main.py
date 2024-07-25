#Get code from Youtube. https://www.youtube.com/watch?v=xQ5UCzFKR58&list=PL30AETbxgR-fAbwiuU1vDl3owNUPUuVrz&index=6
import pygame
from pygame import mixer
import os
import random

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# High score management
HIGH_SCORE_FILE = 'high_score.txt'
high_score = 0

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(score))

# Global constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Assets
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
            mixer.music.load('Jump Sound.mp3')
            mixer.music.play()
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score, font, player
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    high_score = load_high_score()
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def draw_high_score():
        global high_score
        text = font.render("High Score: " + str(high_score), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, 40)
        SCREEN.blit(text, textRect)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                if points > high_score:
                    high_score = points
                    save_high_score(high_score)
                mixer.music.load('Death sound.mp3')
                mixer.music.play()
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        score()
        draw_high_score()  # Correct call to draw_high_score

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    # Load background music
    mixer.music.load('gamesound.mp3')
    mixer.music.play(-1)  # Loop indefinitely
        
    global high_score, font
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            instructions = [
                "Instructions:",
                "Press UP arrow to Jump",
                "Press DOWN arrow to Duck",
                "Avoid obstacles to keep running"
            ]
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)

            for i, line in enumerate(instructions):
                instruction_text = font.render(line, True, (0, 0, 0))
                instruction_rect = instruction_text.get_rect()
                instruction_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 + (i * 40))
                SCREEN.blit(instruction_text, instruction_rect)
        else:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            SCREEN.blit(text, textRect)
            score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
            score_rect = score_text.get_rect()
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score_text, score_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main()

menu(death_count=0)