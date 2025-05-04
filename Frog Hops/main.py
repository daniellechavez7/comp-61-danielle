import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
TILE_SIZE = 80
ROWS = HEIGHT // TILE_SIZE
COLS = WIDTH // TILE_SIZE
FPS = 60

# Colors
TEXT_COLOR = (255, 255, 255)

# Load images
background_img = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
lilypad_img = pygame.transform.scale(pygame.image.load("lilypad.png"), (TILE_SIZE, TILE_SIZE))
food_img = pygame.transform.scale(pygame.image.load("food.png"), (40, 40))
star_img = pygame.transform.scale(pygame.image.load("star.png"), (40, 40))
title_screen_img = pygame.transform.scale(pygame.image.load("frog_title.jpg"), (WIDTH, HEIGHT))
app_icon = pygame.image.load("frogtitle.png")

# Load sounds
hop_sound = pygame.mixer.Sound("hop.wav")
splash_sound = pygame.mixer.Sound("splash.wav")
star_collect_sound = pygame.mixer.Sound("star_collect.wav")
pygame.mixer.music.load("game.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frog Hop")
pygame.display.set_icon(app_icon)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

frog_frame_index = 0
frog_frame_timer = 0
frog_frame_interval = 0.1  # seconds between frames (0.1 = 10 FPS)


# Load frog animation frames
frog_frames = []
for filename in sorted(os.listdir("frog_frames")):
    if filename.endswith(".png"):
        frame = pygame.image.load(os.path.join("frog_frames", filename)).convert_alpha()
        frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))
        frog_frames.append(frame)

class LilyPad:
    def __init__(self, row, col):
        self.row = float(row)
        self.col = float(col)
        self.speed = random.uniform(0.006, 0.012)
        self.direction = random.choice(["horizontal", "vertical"])

    def move(self):
        if self.direction == "horizontal":
            self.col += self.speed
            if self.col > COLS:
                self.col = 0
        else:
            self.row += self.speed
            if self.row > ROWS:
                self.row = 0

    def get_position(self):
        return (int(round(self.row)), int(round(self.col)))

def generate_lily_pads():
    return [LilyPad(random.randint(0, ROWS - 1), random.randint(0, COLS - 1)) for _ in range(20)]

def draw_game():
    screen.blit(background_img, (0, 0))
    for pad in lily_pads:
        pad.move()
        x = pad.col * TILE_SIZE + TILE_SIZE // 2
        y = pad.row * TILE_SIZE + TILE_SIZE // 2
        screen.blit(lilypad_img, (x - lilypad_img.get_width() // 2, y - lilypad_img.get_height() // 2))

    fx = food_pos[1] * TILE_SIZE + TILE_SIZE // 2
    fy = food_pos[0] * TILE_SIZE + TILE_SIZE // 2
    screen.blit(food_img, (fx - 20, fy - 20))

    sx = star_pos[1] * TILE_SIZE + TILE_SIZE // 2
    sy = star_pos[0] * TILE_SIZE + TILE_SIZE // 2
    screen.blit(star_img, (sx - 20, sy - 20))

    # Use the current frame from the animated frog
    frog_img = frog_frames[frog_frame_index]
    frog_rect = frog_img.get_rect(center=(frog_x, frog_y))
    screen.blit(frog_img, frog_rect.topleft)

    screen.blit(font.render(f"Score: {score}", True, TEXT_COLOR), (10, 10))
    screen.blit(font.render(f"Lives: {lives}", True, TEXT_COLOR), (WIDTH - 200, 10))
    screen.blit(font.render(f"Level: {level}", True, TEXT_COLOR), (WIDTH - 200, 50))
    screen.blit(font.render(f"High Score: {high_score}", True, TEXT_COLOR), (10, 50))

    if game_over:
        over_text = font.render("Game Over! Press R to Restart", True, TEXT_COLOR)
        screen.blit(over_text, (WIDTH // 2 - 250, HEIGHT // 2))

    pygame.display.flip()


def draw_title_screen():
    screen.blit(title_screen_img, (0, 0))
    
     # Game title
    title_text = font.render("Frog Hop!", True, TEXT_COLOR)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
    
    start_text = font.render("Press SPACE to Start", True, TEXT_COLOR)
    instruction_text = font.render("Press I for Instructions", True, TEXT_COLOR)
    quit_text = font.render("Press Q to Quit", True, TEXT_COLOR)

    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 150))
    screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT - 100))
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

def draw_instruction_screen():
    screen.fill((0, 100, 0))
    instructions = [
        "Instructions:",
        "Use arrow keys to hop.",
        "Land on lily pads to survive.",
        "Collect food for points.",
        "Catch stars to level up!",
        "Don't fall in the water!",
        "",
        "Press SPACE to go back to Title Screen"
    ]
    for i, line in enumerate(instructions):
        text = font.render(line, True, TEXT_COLOR)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50 + i * 50))
    pygame.display.flip()

def reset_game():
    global frog_row, frog_col, frog_x, frog_y, frog_target_x, frog_target_y
    global score, level, lives, frog_speed, lily_pads, food_pos, star_pos, game_over

    frog_row, frog_col = ROWS // 2, COLS // 2
    frog_x = frog_col * TILE_SIZE + TILE_SIZE // 2
    frog_y = frog_row * TILE_SIZE + TILE_SIZE // 2
    frog_target_x = frog_x
    frog_target_y = frog_y

    score = 0
    level = 1
    lives = 3
    frog_speed = 10
    game_over = False

    lily_pads = generate_lily_pads()
    food_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
    star_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

# Initial game state
title_screen = True
instruction_screen = False
score = 0
level = 1
lives = 3
frog_speed = 10
high_score = 0
game_over = False
frame_index = 0

frog_row, frog_col = ROWS // 2, COLS // 2
frog_x = frog_col * TILE_SIZE + TILE_SIZE // 2
frog_y = frog_row * TILE_SIZE + TILE_SIZE // 2
frog_target_x = frog_x
frog_target_y = frog_y

lily_pads = generate_lily_pads()
food_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
star_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

# Main loop
running = True
while running:
    dt = clock.tick(FPS) / 1000.0

    # Update frog animation timer
    frog_frame_timer += dt
    if frog_frame_timer >= frog_frame_interval:
        frog_frame_timer = 0
        frog_frame_index = (frog_frame_index + 1) % len(frog_frames)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if title_screen:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    title_screen = False
                if event.key == pygame.K_i:
                    instruction_screen = True
                    title_screen = False
                if event.key == pygame.K_q:
                    running = False


        elif instruction_screen:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                instruction_screen = False
                title_screen = True

        elif game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()

        else:
            if event.type == pygame.KEYDOWN:
                if frog_x == frog_target_x and frog_y == frog_target_y:
                    if event.key == pygame.K_UP:
                        frog_row -= 1
                    elif event.key == pygame.K_DOWN:
                        frog_row += 1
                    elif event.key == pygame.K_LEFT:
                        frog_col -= 1
                    elif event.key == pygame.K_RIGHT:
                        frog_col += 1

                    frog_target_x = frog_col * TILE_SIZE + TILE_SIZE // 2
                    frog_target_y = frog_row * TILE_SIZE + TILE_SIZE // 2

                    if frog_row < 0 or frog_row >= ROWS or frog_col < 0 or frog_col >= COLS:
                        lives -= 1
                        splash_sound.play()
                    else:
                        landed = False
                        for pad in lily_pads:
                            pad_x = pad.col * TILE_SIZE + TILE_SIZE // 2
                            pad_y = pad.row * TILE_SIZE + TILE_SIZE // 2
                            distance = ((frog_x - pad_x) ** 2 + (frog_y - pad_y) ** 2) ** 0.5
                            if distance <= 40:  # Adjust this for easier/harder landings
                                landed = True
                                break

                        if not landed:
                            lives -= 1
                            splash_sound.play()
                        else:
                            score += 1 * level
                            hop_sound.play()

                    if (frog_row, frog_col) == food_pos:
                        score += 5 * level
                        food_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
                    if (frog_row, frog_col) == star_pos:
                        score += 10 * level
                        level += 1
                        frog_speed += 1
                        star_collect_sound.play()
                        star_pos = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))

                    if lives <= 0:
                        game_over = True

    if title_screen:
        draw_title_screen()
    elif instruction_screen:
        draw_instruction_screen()
    else:
        if frog_x < frog_target_x:
            frog_x += frog_speed
            if frog_x > frog_target_x:
                frog_x = frog_target_x
        elif frog_x > frog_target_x:
            frog_x -= frog_speed
            if frog_x < frog_target_x:
                frog_x = frog_target_x
        if frog_y < frog_target_y:
            frog_y += frog_speed
            if frog_y > frog_target_y:
                frog_y = frog_target_y
        elif frog_y > frog_target_y:
            frog_y -= frog_speed
            if frog_y < frog_target_y:
                frog_y = frog_target_y

        if score > high_score:
            high_score = score

        draw_game()

pygame.quit()
