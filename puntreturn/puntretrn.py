import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
OPPONENT_WIDTH = 50
OPPONENT_HEIGHT = 50
FIELD_LINE_SPACING = 100  # Increased spacing
TOP_SECTION_HEIGHT = int(SCREEN_HEIGHT * 0.15)  # 15% of screen height

# Colors
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Opponents")

# Fonts with adjustable sizes
title_font_size = 34
score_font_size = 20
high_score_font_size = 20

title_font = pygame.font.Font(None, title_font_size)
score_font = pygame.font.Font(None, score_font_size)
high_score_font = pygame.font.Font(None, high_score_font_size)

# Load images
player_image = pygame.image.load("/Users/abhiaremanda/Desktop/Projects/python/player_sprite.jpg")
opponent_image = pygame.image.load("/Users/abhiaremanda/Desktop/Projects/python/defender.jpg")

# Scale images to fit the desired sizes
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
opponent_image = pygame.transform.scale(opponent_image, (OPPONENT_WIDTH, OPPONENT_HEIGHT))

# Sprite classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT
        self.speed = 15
        

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > TOP_SECTION_HEIGHT:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Opponent(pygame.sprite.Sprite):
    def __init__(self, x, y, direction="down"):
        super().__init__()
        self.image = opponent_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = direction

    def update(self):
        global speed_multiplier
        drift_speed = max(1, int(speed_multiplier))

        if self.direction == "down":
            self.rect.y += int(player.speed * speed_multiplier)
        elif self.direction == "left":
            self.rect.x += drift_speed
            if self.rect.x >= 0:
                self.direction = "down"
        elif self.direction == "right":
            self.rect.x -= drift_speed
            if self.rect.x + OPPONENT_WIDTH <= SCREEN_WIDTH:
                self.direction = "down"

        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        if self.direction == "down":
            if self.rect.x < player.rect.x:
                self.rect.x += drift_speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= drift_speed

# Functions
def initialize_game():
    global player, player_group, opponents_group, score, high_score, speed_multiplier, last_time
    player = Player()
    player_group = pygame.sprite.Group(player)
    opponents_group = pygame.sprite.Group()
    score = 0
    high_score = 0
    speed_multiplier = 1
    last_time = pygame.time.get_ticks()

def spawn_opponents():
    y = -OPPONENT_HEIGHT
    for _ in range(random.randint(2, 5)):
        x = random.randint(0, SCREEN_WIDTH - OPPONENT_WIDTH)
        opponent = Opponent(x, y)
        opponents_group.add(opponent)
        y -= random.randint(FIELD_LINE_SPACING, FIELD_LINE_SPACING * 3)

    if score >= 100:
        side_opponent_left = Opponent(-OPPONENT_WIDTH, random.randint(TOP_SECTION_HEIGHT, SCREEN_HEIGHT - OPPONENT_HEIGHT), direction="left")
        side_opponent_right = Opponent(SCREEN_WIDTH, random.randint(TOP_SECTION_HEIGHT, SCREEN_HEIGHT - OPPONENT_HEIGHT), direction="right")
        opponents_group.add(side_opponent_left, side_opponent_right)

def handle_collisions():
    global in_game, high_score
    if pygame.sprite.spritecollideany(player, opponents_group):
        if score > high_score:
            high_score = int(score)
        in_game = False

def draw_game():
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, TOP_SECTION_HEIGHT))
    title_text = title_font.render("Punt Return", True, WHITE)
    screen.blit(title_text, (10, 10))
    score_text = score_font.render(f"Score: {int(score)} yards", True, WHITE)
    screen.blit(score_text, (10, 50))
    high_score_text = high_score_font.render(f"High Score: {high_score} yards", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))
    for y in range(TOP_SECTION_HEIGHT, SCREEN_HEIGHT, FIELD_LINE_SPACING):
        pygame.draw.line(screen, WHITE, (0, y), (SCREEN_WIDTH, y), 2)
    player_group.draw(screen)
    opponents_group.draw(screen)
    pygame.display.flip()

def show_menu():
    screen.fill(BLACK)
    title_text = title_font.render("Punt Return", True, WHITE)
    screen.blit(title_text, (10, 10))
    high_score_text = high_score_font.render(f"High Score: {high_score} yards", True, WHITE)
    screen.blit(high_score_text, (SCREEN_WIDTH - 200, 10))
    menu_rects = draw_menu_items()
    pygame.display.flip()
    return menu_rects

def draw_menu_items():
    menu_font = pygame.font.Font(None, 36)
    menu_items = ["Try Again", "Quit"]
    menu_rects = []
    y = SCREEN_HEIGHT // 2 - 50
    for item in menu_items:
        text = menu_font.render(item, True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(text, rect)
        menu_rects.append(rect)
        y += 50
    return menu_rects

def handle_menu_events(menu_rects):
    global in_game, running, score, speed_multiplier, last_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if menu_rects[0].collidepoint(mouse_pos):
                score = 0
                speed_multiplier = 1
                last_time = pygame.time.get_ticks()
                player.rect.centerx = SCREEN_WIDTH // 2
                player.rect.bottom = SCREEN_HEIGHT
                opponents_group.empty()
                in_game = True
            elif menu_rects[1].collidepoint(mouse_pos):
                running = False

def main():
    global in_game, running, score, speed_multiplier, last_time, player_group, opponents_group

    initialize_game()

    running = True
    in_game = True
    clock = pygame.time.Clock()

    while running:
        if in_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            player_group.update()
            opponents_group.update()

            handle_collisions()

            draw_game()

            if len(opponents_group) == 0 or all(opponent.rect.top > FIELD_LINE_SPACING * 3 for opponent in opponents_group):
                spawn_opponents()

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - last_time) / 1000.0

            score += 5 * elapsed_time
            last_time = current_time

            speed_multiplier = 1 + int(score) // 100 * 0.15

            clock.tick(30)
        else:
            menu_rects = show_menu()
            handle_menu_events(menu_rects)

    pygame.quit()

if __name__ == "__main__":
    main()
