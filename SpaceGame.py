import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodg3r")

# Load galaxy background image
background = pygame.image.load("galaxy.jpg")  # Replace with your galaxy image
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load smaller image
car_image = pygame.image.load("NewSpaceShip.png")  # Update the image filename
car_rect = car_image.get_rect()
car_rect.topleft = (WIDTH // 2 - car_rect.width // 2, HEIGHT - car_rect.height - 10)

# Create a clock object to control the frame rate
clock = pygame.time.Clock()

# Game variables
car_speed = 5
obstacle_speed = 5
obstacle_frequency = 50  # Adjust the obstacle frequency
obstacles = []
score = 0
high_score = 0  # New variable to store high score

# Fonts
font = pygame.font.Font(None, 36)

# Game state
game_active = True

# Function to draw text on the screen
def draw_text(text, x, y):
    surface = font.render(text, True, WHITE)
    screen.blit(surface, (x, y))

# Function to reset the game state
def reset_game():
    global obstacles, car_rect, obstacle_speed, score
    obstacles = []
    car_rect.topleft = (WIDTH // 2 - car_rect.width // 2, HEIGHT - car_rect.height - 10)
    obstacle_speed = 5
    score = 0

# High Score Code
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))


high_score = load_high_score()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not game_active:
                    game_active = True
                    reset_game()

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_rect.x > 0:
            car_rect.x -= car_speed
        if keys[pygame.K_RIGHT] and car_rect.x < WIDTH - car_rect.width:
            car_rect.x += car_speed

        # Create obstacles
        if random.randint(1, obstacle_frequency) == 1:
            obstacle = pygame.Rect(random.randint(0, WIDTH - 50), 0, 50, 50)
            obstacles.append(obstacle)

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1
                if score > high_score:
                    high_score = score  # Update high score

                if score % 10 == 0:  # Increase speed every 10 points
                    obstacle_speed += 1

        # Check for collisions with obstacles
        for obstacle in obstacles:
            if car_rect.colliderect(obstacle):
                game_active = False

        # Draw the background
        screen.blit(background, (0, 0))

        # Draw the car
        screen.blit(car_image, car_rect)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, obstacle)

        # Draw score
        draw_text("Score: {}".format(score), 10, 10)
        draw_text("High Score: {}".format(high_score), WIDTH - 200, 10)
    else:
        # Draw retry screen
        draw_text("Game Over! Press Enter to Retry", WIDTH // 2 - 200, HEIGHT // 2 - 20)

        # Save high score to file
        save_high_score(high_score)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(FPS)




