import pygame
import sys
import os
from pygame.locals import *
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dark Forest Battle: Hero vs Dark Elves")

# Diagnostics
print("Current directory:", os.getcwd())
print("Files in current directory:", os.listdir("."))
if "eth.gif" in os.listdir("."):
    print("Found eth.gif in current directory.")
else:
    print("Warning: eth.gif not found in current directory. Using placeholder.")

# Colors for the pixel-art-inspired dark forest
DARK_NIGHT = (15, 15, 25)  # Deep night sky
MUDDY_GROUND = (50, 30, 20)  # Muddy ground
TREE_TRUNK = (20, 10, 5)  # Dark, gnarled trunks
GLOW_BLUE = (0, 100, 150)  # Blue glowing lights
GLOW_RED = (150, 50, 50)  # Red glowing lights
MIST_GRAY = (60, 60, 70, 40)  # Misty overlay
DISTANT_SHADOW = (20, 20, 30)  # Distant hills
PLAYER_COLOR = (0, 100, 200)  # Blue placeholder for player
ENEMY_COLOR = (80, 0, 0)  # Dark red for dark elves (fallback)
# Colors for health bars
HEALTH_BAR_GREEN = (0, 255, 0)  # Green for current health
HEALTH_BAR_RED = (255, 0, 0)    # Red for missing health
HEALTH_BAR_BORDER = (0, 0, 0)   # Black border
# Colors for projectiles
SPEAR_COLOR = (200, 200, 200)  # Silver for elf1,1's spear
LASER_COLOR = (0, 255, 255)    # Cyan for elf2,2's laser
FIREBOMB_COLOR = (255, 100, 0) # Orange for elf3,3's firebomb
AIR_PROJECTILE_COLOR = (0, 255, 255)  # Cyan for $AIR projectile
NUKE_COLOR = (100, 100, 100)  # Dark gray for nuke
NUKE_AURA_COLOR = (200, 50, 50, 100)  # Red glowing aura
EXPLOSION_COLOR = (255, 100, 0, 200)  # Bright orange for nuke explosion
# Colors for particle effects
PARTICLE_SPEAR = (180, 180, 180, 120)  # Brighter gray for spear trail
PARTICLE_LASER = (0, 220, 220, 180)    # Brighter cyan for laser trail
PARTICLE_AIR = (255, 255, 255, 180)    # White for $AIR trail (changed)
PARTICLE_FIREBOMB = (255, 70, 0, 220)  # Vibrant orange for firebomb trail
PARTICLE_FIREBOMB_SECONDARY = (200, 0, 0, 180)  # Red for firebomb accent
ETHOS_COLOR = (255, 255, 255, 180)  # Semi-transparent white for ETHOS text
AIR_TEXT_COLOR = (255, 255, 255)  # White for $AIR text
NUKE_PARTICLE = (150, 150, 150, 120)  # Gray for nuke trail
EXPLOSION_PARTICLE = (255, 50, 0, 200)  # Orange for explosion particles
# Colors for screens
START_BG_COLOR = (50, 0, 100)  # Deep purple for start screen
START_TEXT_COLOR = (0, 255, 255)  # Glowing cyan for start button
VICTORY_BG_COLOR = (0, 50, 0)  # Dark green for victory
VICTORY_TEXT_COLOR = (0, 255, 0)  # Bright green for victory text
GAME_OVER_BG_COLOR = (50, 0, 0)  # Dark red for game over
GAME_OVER_TEXT_COLOR = (255, 0, 0)  # Bright red for game over text

# Player settings
player_width = 64
player_height = 64
player_x = 50  # Left side of the map
player_y = SCREEN_HEIGHT - 70 - player_height  # Feet touch ground
player_speed = 5
player_jump_power = -8  # Reduced jump height
player_gravity = 0.4
player_velocity_y = 0
player_jumping = False
player_health = 225  # Increased by 50% from 150
player_max_health = 225  # Increased by 50% from 150
# Flight settings
player_flying = False
space_press_count = 0
space_press_timer = 0
DOUBLE_PRESS_WINDOW = 0.3  # Time (seconds) to detect double press
FLIGHT_BOOST = -7  # Balanced upward boost
ethos_timer = 0  # Timer for ETHOS text display
ETHOS_DURATION = 0.5  # ETHOS text display time (seconds)
# Ranged projectile settings
AIR_PROJECTILE_SPEED = 6  # Slower speed for $AIR projectile
AIR_PROJECTILE_SIZE = (20, 10)  # Width, height
AIR_PROJECTILE_DAMAGE = 20  # Reduced damage
AIR_PROJECTILE_COOLDOWN = 3.0  # Increased cooldown
air_projectile_timer = 0  # Timer for projectile cooldown
# Nuke attack settings
NUKE_SPEED_UP = 4  # Slower upward speed
NUKE_SPEED_DOWN = 8  # 2x speed downward
NUKE_SIZE = (30, 60)  # Larger size for nuke
NUKE_DAMAGE = 55  # Damage to all in area
NUKE_RADIUS = 75  # Larger explosion radius
NUKE_COOLDOWN = 4.0  # Cooldown
nuke_timer = 0  # Timer for nuke cooldown

# Fonts with fallback
try:
    title_font = pygame.font.SysFont("arial", 48, bold=True)  # For screens
    font = pygame.font.SysFont("arial", 24, bold=True)  # For ETHOS
    air_font = pygame.font.SysFont("arial", 20, bold=True)  # For $AIR
    nuke_font = pygame.font.SysFont("arial", 24, bold=True)  # For nuke ETHOS
except Exception as e:
    print(f"Error loading fonts: {e}. Falling back to default font.")
    title_font = pygame.font.Font(None, 48)
    font = pygame.font.Font(None, 24)
    air_font = pygame.font.Font(None, 20)
    nuke_font = pygame.font.Font(None, 24)

# Load player sprite (eth.gif)
player_image = None
try:
    player_image = pygame.image.load("eth.gif").convert_alpha()
    player_image = pygame.transform.scale(player_image, (player_width, player_height))
    background_color = (255, 255, 0)
    player_image.set_colorkey(background_color)
    player_image.set_alpha(None)
    print("Player sprite (eth.gif) loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading player sprite (eth.gif): {e}. Using blue rectangle placeholder.")
except Exception as e:
    print(f"Unexpected error loading eth.gif: {e}. Using blue rectangle placeholder.")

# Enemy settings
enemy_width = 64
enemy_height = 64
enemies = [
    {"x": SCREEN_WIDTH // 3, "y": SCREEN_HEIGHT - 70 - enemy_height, "health": 100, "fire_timer": 0, "fire_interval": 1500, "base_x": SCREEN_WIDTH // 3, "fly_timer": 0, "type": "chase", "image": None},
    {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT - 400, "health": 100, "fire_timer": 0, "fire_interval": 3000, "base_x": SCREEN_WIDTH // 2, "fly_timer": 0, "type": "fly", "image": None},
    {"x": SCREEN_WIDTH - 150, "y": SCREEN_HEIGHT - 70 - enemy_height, "health": 100, "fire_timer": 0, "fire_interval": 5000, "base_x": SCREEN_WIDTH - 150, "sway_offset": 0, "fly_timer": 0, "type": "sway", "image": None}
]

# Load enemy sprites
try:
    enemy_images = [
        pygame.image.load("elf1,1.gif").convert_alpha(),
        pygame.image.load("elf2,2.gif").convert_alpha(),
        pygame.image.load("elf3,3.gif").convert_alpha()
    ]
    for i in range(len(enemy_images)):
        enemy_images[i] = pygame.transform.scale(enemy_images[i], (enemy_width, enemy_height))
        background_color = (0, 0, 0)
        enemy_images[i].set_colorkey(background_color)
        enemy_images[i].set_alpha(None)
        enemies[i]["image"] = enemy_images[i]
    print("Enemy sprites loaded successfully with transparency.")
except FileNotFoundError as e:
    print(f"Error loading enemy sprite: {e}. Using placeholders.")
    for enemy in enemies:
        enemy["image"] = None
except Exception as e:
    print(f"Unexpected error loading enemy sprites: {e}. Using placeholders.")
    for enemy in enemies:
        enemy["image"] = None

# Projectile settings
projectiles = []
PROJECTILE_SPEED = 7
SPEAR_SIZE = (10, 4)
LASER_SIZE = (20, 4)
FIREBOMB_RADIUS = 8
PROJECTILE_DAMAGE = 10

# Particle settings
particles = []

# Background tree movement (parallax)
bg_tree_offset = 0
bg_tree_speed = 0.5

# Fog surface
fog_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fog_surface.fill(MIST_GRAY)

# Clock for frame rate
clock = pygame.time.Clock()

# Start screen button
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 60)

# Function to reset game state
def reset_game():
    global player_x, player_y, player_velocity_y, player_health, player_jumping, player_flying
    global space_press_count, space_press_timer, ethos_timer, air_projectile_timer, nuke_timer
    global enemies, projectiles, particles, bg_tree_offset
    player_x = 50
    player_y = SCREEN_HEIGHT - 70 - player_height
    player_velocity_y = 0
    player_health = player_max_health
    player_jumping = False
    player_flying = False
    space_press_count = 0
    space_press_timer = 0
    ethos_timer = 0
    air_projectile_timer = 0
    nuke_timer = 0
    enemies = [
        {"x": SCREEN_WIDTH // 3, "y": SCREEN_HEIGHT - 70 - enemy_height, "health": 100, "fire_timer": 0, "fire_interval": 1500, "base_x": SCREEN_WIDTH // 3, "fly_timer": 0, "type": "chase", "image": enemy_images[0] if enemy_images[0] else None},
        {"x": SCREEN_WIDTH // 2, "y": SCREEN_HEIGHT - 400, "health": 100, "fire_timer": 0, "fire_interval": 3000, "base_x": SCREEN_WIDTH // 2, "fly_timer": 0, "type": "fly", "image": enemy_images[1] if enemy_images[1] else None},
        {"x": SCREEN_WIDTH - 150, "y": SCREEN_HEIGHT - 70 - enemy_height, "health": 100, "fire_timer": 0, "fire_interval": 5000, "base_x": SCREEN_WIDTH - 150, "sway_offset": 0, "fly_timer": 0, "type": "sway", "image": enemy_images[2] if enemy_images[2] else None}
    ]
    projectiles.clear()
    particles.clear()
    bg_tree_offset = 0

# Function to draw health bars
def draw_health_bar(screen, x, y, health, max_health=100, width=50, height=8):
    bar_x = x + (player_width - width) // 2 if y == player_y else x + (enemy_width - width) // 2
    bar_y = max(0, y - 20)
    pygame.draw.rect(screen, HEALTH_BAR_RED, (bar_x, bar_y, width, height))
    health_width = (health / max_health) * width if max_health > 0 else 0
    pygame.draw.rect(screen, HEALTH_BAR_GREEN, (bar_x, bar_y, health_width, height))
    pygame.draw.rect(screen, HEALTH_BAR_BORDER, (bar_x, bar_y, width, height), 1)

# Function to create a projectile
def create_projectile(start_x, start_y, target_x, target_y, type, target_enemy=None):
    dx = target_x + enemy_width // 2 - start_x if target_enemy else target_x + player_width // 2 - start_x
    dy = target_y + enemy_height // 2 - start_y if target_enemy else target_y + player_height // 2 - start_y
    distance = max(1, math.hypot(dx, dy))
    if type == "air":
        vx = (dx / distance) * AIR_PROJECTILE_SPEED
        vy = (dy / distance) * AIR_PROJECTILE_SPEED
    elif type == "nuke":
        vx, vy = 0, -NUKE_SPEED_UP
    else:
        vx = (dx / distance) * PROJECTILE_SPEED
        vy = (dy / distance) * PROJECTILE_SPEED
    proj = {"x": start_x, "y": start_y, "vx": vx, "vy": vy, "type": type, "phase": "up" if type == "nuke" else None}
    if type == "spear":
        proj["size"] = SPEAR_SIZE
    elif type == "laser":
        proj["size"] = LASER_SIZE
    elif type == "firebomb":
        proj["radius"] = FIREBOMB_RADIUS
    elif type == "air":
        proj["size"] = AIR_PROJECTILE_SIZE
        proj["target_enemy"] = target_enemy
    elif type == "nuke":
        proj["size"] = NUKE_SIZE
        proj["target_x"] = random.randint(0, SCREEN_WIDTH - NUKE_SIZE[0])
    return proj

# Function to create particles
def create_particles(x, y, type):
    if type == "spear":
        for _ in range(random.randint(3, 4)):
            particles.append({"x": x, "y": y, "vx": random.uniform(-1.5, 1.5), "vy": random.uniform(-1.5, 1.5),
                             "color": PARTICLE_SPEAR, "radius": random.randint(1, 2), "lifetime": random.uniform(0.3, 0.5)})
    elif type == "laser":
        for _ in range(random.randint(6, 8)):
            particles.append({"x": x, "y": y, "vx": random.uniform(-2, 2), "vy": random.uniform(-2, 2),
                             "color": PARTICLE_LASER, "radius": random.randint(1, 3), "lifetime": random.uniform(0.3, 0.5)})
    elif type == "air":
        for _ in range(random.randint(6, 8)):
            particles.append({"x": x, "y": y, "vx": random.uniform(-2, 2), "vy": random.uniform(-2, 2),
                             "color": PARTICLE_AIR, "radius": random.randint(1, 3), "lifetime": random.uniform(0.3, 0.5)})
    elif type == "firebomb":
        for _ in range(random.randint(6, 8)):
            color = random.choice([PARTICLE_FIREBOMB, PARTICLE_FIREBOMB_SECONDARY])
            particles.append({"x": x, "y": y, "vx": random.uniform(-2.5, 2.5), "vy": random.uniform(-3, 0),
                             "color": color, "radius": random.randint(2, 5), "lifetime": random.uniform(0.6, 1.0)})
    elif type == "nuke":
        for _ in range(random.randint(4, 6)):
            particles.append({"x": x, "y": y, "vx": random.uniform(-1, 1), "vy": random.uniform(-1, 1),
                             "color": NUKE_PARTICLE, "radius": random.randint(1, 2), "lifetime": random.uniform(0.3, 0.5)})
    elif type == "explosion":
        for _ in range(random.randint(15, 20)):
            color = random.choice([PARTICLE_FIREBOMB, PARTICLE_FIREBOMB_SECONDARY])
            particles.append({"x": x, "y": y, "vx": random.uniform(-4, 4), "vy": random.uniform(-4, 4),
                             "color": color, "radius": random.randint(3, 6), "lifetime": random.uniform(0.7, 1.2)})

# Game loop
game_state = "start"
running = True
while running:
    dt = clock.tick(60) / 1000.0

    if game_state == "start":
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    game_state = "playing"
                    reset_game()
            elif event.type == MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game_state = "playing"
                    reset_game()

        screen.fill(START_BG_COLOR)
        pygame.draw.rect(screen, START_TEXT_COLOR, start_button_rect, 2)
        start_text = title_font.render("START ETHOS ROYALE", True, START_TEXT_COLOR)
        start_rect = start_text.get_rect(center=start_button_rect.center)
        screen.blit(start_text, start_rect)

    elif game_state == "playing":
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    space_press_count += 1
                    space_press_timer = DOUBLE_PRESS_WINDOW
                    if space_press_count == 1 and not player_jumping and player_y >= SCREEN_HEIGHT - 70 - player_height:
                        player_velocity_y = player_jump_power
                        player_jumping = True
                        player_flying = False
                    elif space_press_count >= 2:
                        player_flying = True
                        player_velocity_y = FLIGHT_BOOST
                        player_jumping = True
                        ethos_timer = ETHOS_DURATION
                        space_press_count = 0
                elif event.key == K_r and air_projectile_timer <= 0 and enemies:
                    air_projectile_timer = AIR_PROJECTILE_COOLDOWN
                    target_enemy = random.choice(enemies)
                    proj = create_projectile(player_x + player_width // 2, player_y + player_height // 2,
                                            target_enemy["x"], target_enemy["y"], "air", target_enemy)
                    projectiles.append(proj)
                elif event.key == K_e and nuke_timer <= 0:
                    nuke_timer = NUKE_COOLDOWN
                    proj = create_projectile(player_x + player_width // 2, player_y + player_height // 2, 0, 0, "nuke")
                    projectiles.append(proj)

        if space_press_timer > 0:
            space_press_timer -= dt
            if space_press_timer <= 0:
                space_press_count = 0
                player_flying = False
        if ethos_timer > 0:
            ethos_timer -= dt
        if air_projectile_timer > 0:
            air_projectile_timer -= dt
        if nuke_timer > 0:
            nuke_timer -= dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            bg_tree_offset -= bg_tree_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
            bg_tree_offset += bg_tree_speed

        player_velocity_y += player_gravity
        player_y += player_velocity_y
        if player_y > SCREEN_HEIGHT - 70 - player_height:
            player_y = SCREEN_HEIGHT - 70 - player_height
            player_velocity_y = 0
            player_jumping = False
            player_flying = False
        if player_y < 0:
            player_y = 0
            player_velocity_y = max(0, player_velocity_y)

        # Update enemy movement
        for enemy in enemies[:]:
            if enemy["type"] == "chase":
                target_x = player_x + player_width // 2
                enemy_center_x = enemy["x"] + enemy_width // 2
                distance_to_player = abs(target_x - enemy_center_x)
                if distance_to_player > 50:
                    speed = 2
                    if target_x < enemy_center_x:
                        enemy["x"] -= speed * dt * 60
                    elif target_x > enemy_center_x:
                        enemy["x"] += speed * dt * 60
                    enemy["x"] = max(0, min(enemy["x"], SCREEN_WIDTH - enemy_width))
            elif enemy["type"] == "fly":
                enemy["fly_timer"] = enemy.get("fly_timer", 0) + dt
                amplitude = 100
                period = 6
                enemy["x"] = enemy["base_x"] + amplitude * math.sin(2 * math.pi * enemy["fly_timer"] / period)
                enemy["x"] = max(0, min(enemy["x"], SCREEN_WIDTH - enemy_width))
            elif enemy["type"] == "sway":
                if enemy["fire_timer"] >= enemy["fire_interval"]:
                    enemy["sway_offset"] = random.uniform(-10, 10)
                enemy["x"] = enemy["base_x"] + enemy.get("sway_offset", 0)
                enemy["x"] = max(0, min(enemy["x"], SCREEN_WIDTH - enemy_width))

        # Update enemy firing timers
        for enemy in enemies[:]:
            enemy["fire_timer"] += dt * 1000
            if enemy["fire_timer"] >= enemy["fire_interval"]:
                projectile = create_projectile(enemy["x"], enemy["y"], player_x, player_y,
                                              "spear" if enemy["type"] == "chase" else "laser" if enemy["type"] == "fly" else "firebomb")
                projectiles.append(projectile)
                enemy["fire_timer"] = 0

        # Update projectiles
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        projectiles_to_remove = []
        for proj in projectiles[:]:
            print(f"Projectile: type={proj['type']}, x={proj['x']}, y={proj['y']}, phase={proj.get('phase', 'None')}, vy={proj.get('vy', 'None')}")
            if proj["type"] == "nuke":
                if proj["phase"] == "up":
                    proj["y"] -= NUKE_SPEED_UP * dt * 60
                    if proj["y"] < -SCREEN_HEIGHT:
                        print(f"Nuke exiting map at y={proj['y']}, switching to down phase")
                        proj["phase"] = "down"
                        proj["y"] = -NUKE_SIZE[1]
                        proj["x"] = proj["target_x"]
                        proj["vy"] = NUKE_SPEED_DOWN
                        print(f"Nuke repositioned to x={proj['x']}, y={proj['y']}, vy={proj['vy']}")
                elif proj["phase"] == "down":
                    proj["y"] += proj["vy"] * dt * 60
                    print(f"Nuke descending: y={proj['y']}, vy={proj['vy']}")
                    if proj["y"] >= SCREEN_HEIGHT - 70 - NUKE_SIZE[1]:
                        explosion_rect = pygame.Rect(proj["x"] - NUKE_RADIUS, proj["y"] - NUKE_RADIUS,
                                                    NUKE_RADIUS * 2, NUKE_RADIUS * 2)
                        if explosion_rect.colliderect(player_rect):
                            player_health -= NUKE_DAMAGE
                        for enemy in enemies[:]:
                            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_width, enemy_height)
                            if explosion_rect.colliderect(enemy_rect):
                                enemy["health"] -= NUKE_DAMAGE
                                if enemy["health"] <= 0:
                                    enemies.remove(enemy)
                        create_particles(proj["x"], proj["y"], "explosion")
                        projectiles_to_remove.append(proj)
                        print(f"Nuke exploded at x={proj['x']}, y={proj['y']}")
                    elif proj["y"] > SCREEN_HEIGHT + NUKE_SIZE[1]:
                        projectiles_to_remove.append(proj)
                        print(f"Nuke removed: went off-screen at y={proj['y']}")
            else:
                proj["x"] += proj["vx"]
                proj["y"] += proj["vy"]
                create_particles(proj["x"], proj["y"], proj["type"])
                if proj["type"] in ["spear", "laser"]:
                    proj_rect = pygame.Rect(proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                           proj["size"][0], proj["size"][1])
                    if proj_rect.colliderect(player_rect):
                        player_health -= PROJECTILE_DAMAGE
                        projectiles_to_remove.append(proj)
                elif proj["type"] == "firebomb":
                    proj_rect = pygame.Rect(proj["x"] - proj["radius"], proj["y"] - proj["radius"],
                                           proj["radius"] * 2, proj["radius"] * 2)
                    if proj_rect.colliderect(player_rect):
                        player_health -= PROJECTILE_DAMAGE
                        projectiles_to_remove.append(proj)
                elif proj["type"] == "air" and proj.get("target_enemy") in enemies:
                    target_rect = pygame.Rect(proj["target_enemy"]["x"], proj["target_enemy"]["y"], enemy_width, enemy_height)
                    proj_rect = pygame.Rect(proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                           proj["size"][0], proj["size"][1])
                    if proj_rect.colliderect(target_rect):
                        proj["target_enemy"]["health"] -= AIR_PROJECTILE_DAMAGE
                        if proj["target_enemy"]["health"] <= 0:
                            enemies.remove(proj["target_enemy"])
                        projectiles_to_remove.append(proj)
                if proj["type"] != "nuke":
                    if (proj["x"] < -50 or proj["x"] > SCREEN_WIDTH + 50 or
                        proj["y"] < -50 or proj["y"] > SCREEN_HEIGHT + 50):
                        projectiles_to_remove.append(proj)

        for proj in projectiles_to_remove:
            if proj in projectiles:
                projectiles.remove(proj)

        # Update particles
        particles_to_remove = []
        for particle in particles:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["lifetime"] -= dt
            if particle["lifetime"] <= 0:
                particles_to_remove.append(particle)

        for particle in particles_to_remove:
            if particle in particles:
                particles.remove(particle)

        # Check win/lose conditions
        if player_health <= 0:
            game_state = "game_over"
        elif not enemies:
            game_state = "victory"

        # Draw the stage
        screen.fill(DARK_NIGHT)

        # Distant shadowy hills
        pygame.draw.rect(screen, DISTANT_SHADOW, (0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 80))
        pygame.draw.polygon(screen, DISTANT_SHADOW, [(100, SCREEN_HEIGHT - 170), (200, SCREEN_HEIGHT - 200), (300, SCREEN_HEIGHT - 170)])
        pygame.draw.polygon(screen, DISTANT_SHADOW, [(500, SCREEN_HEIGHT - 180), (600, SCREEN_HEIGHT - 220), (700, SCREEN_HEIGHT - 180)])

        # Background trees (parallax)
        for i in range(-1, 2):
            x_base = (i * SCREEN_WIDTH + bg_tree_offset) % SCREEN_WIDTH
            for j in range(0, SCREEN_WIDTH, 120):
                x = x_base + j
                pygame.draw.rect(screen, TREE_TRUNK, (x, SCREEN_HEIGHT - 130, 10, 60))
                pygame.draw.line(screen, TREE_TRUNK, (x + 5, SCREEN_HEIGHT - 130), (x + 15, SCREEN_HEIGHT - 160), 2)
                pygame.draw.line(screen, TREE_TRUNK, (x + 5, SCREEN_HEIGHT - 130), (x - 5, SCREEN_HEIGHT - 150), 2)
                pygame.draw.circle(screen, GLOW_BLUE, (x + 15, SCREEN_HEIGHT - 160), 2)
                pygame.draw.circle(screen, GLOW_RED, (x - 5, SCREEN_HEIGHT - 150), 2)

        # Ground
        pygame.draw.rect(screen, MUDDY_GROUND, (0, SCREEN_HEIGHT - 70, SCREEN_WIDTH, 70))
        for i in range(0, SCREEN_WIDTH, 50):
            pygame.draw.ellipse(screen, (40, 25, 15), (i, SCREEN_HEIGHT - 70, 40, 10))

        # Foreground trees
        for i in range(0, SCREEN_WIDTH, 100):
            pygame.draw.rect(screen, TREE_TRUNK, (i, SCREEN_HEIGHT - 220, 15, 150))
            pygame.draw.line(screen, TREE_TRUNK, (i + 7, SCREEN_HEIGHT - 220), (i + 20, SCREEN_HEIGHT - 260), 3)
            pygame.draw.line(screen, TREE_TRUNK, (i + 7, SCREEN_HEIGHT - 220), (i - 5, SCREEN_HEIGHT - 240), 3)
            pygame.draw.circle(screen, GLOW_BLUE, (i + 20, SCREEN_HEIGHT - 260), 3)
            pygame.draw.circle(screen, GLOW_BLUE, (i - 5, SCREEN_HEIGHT - 240), 3)
            pygame.draw.rect(screen, TREE_TRUNK, (i + 50, SCREEN_HEIGHT - 200, 12, 130))
            pygame.draw.line(screen, TREE_TRUNK, (i + 56, SCREEN_HEIGHT - 200), (i + 70, SCREEN_HEIGHT - 240), 3)
            pygame.draw.line(screen, TREE_TRUNK, (i + 56, SCREEN_HEIGHT - 200), (i + 40, SCREEN_HEIGHT - 220), 3)
            pygame.draw.circle(screen, GLOW_RED, (i + 70, SCREEN_HEIGHT - 240), 3)
            pygame.draw.circle(screen, GLOW_RED, (i + 40, SCREEN_HEIGHT - 220), 3)

        # Fog overlay
        screen.blit(fog_surface, (0, 0))

        # Draw particles
        for particle in particles:
            pygame.draw.circle(screen, particle["color"], (int(particle["x"]), int(particle["y"])), particle["radius"])

        # Draw projectiles
        for proj in projectiles:
            if proj["type"] == "spear":
                pygame.draw.rect(screen, SPEAR_COLOR,
                                 (proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                  proj["size"][0], proj["size"][1]))
            elif proj["type"] == "laser":
                pygame.draw.rect(screen, (0, 200, 200, 100),
                                 (proj["x"] - proj["size"][0] // 2 - 2, proj["y"] - proj["size"][1] // 2 - 2,
                                  proj["size"][0] + 4, proj["size"][1] + 4), border_radius=2)
                pygame.draw.rect(screen, LASER_COLOR,
                                 (proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                  proj["size"][0], proj["size"][1]))
            elif proj["type"] == "firebomb":
                pygame.draw.circle(screen, (255, 50, 0, 100), (int(proj["x"]), int(proj["y"])), proj["radius"] + 3)
                pygame.draw.circle(screen, FIREBOMB_COLOR, (int(proj["x"]), int(proj["y"])), proj["radius"])
            elif proj["type"] == "air":
                pygame.draw.rect(screen, (0, 200, 200, 100),
                                 (proj["x"] - proj["size"][0] // 2 - 2, proj["y"] - proj["size"][1] // 2 - 2,
                                  proj["size"][0] + 4, proj["size"][1] + 4), border_radius=2)
                pygame.draw.rect(screen, AIR_PROJECTILE_COLOR,
                                 (proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                  proj["size"][0], proj["size"][1]))
                try:
                    air_text = air_font.render("$AIR", True, AIR_TEXT_COLOR)
                    text_rect = air_text.get_rect(center=(proj["x"], proj["y"]))
                    outline = air_font.render("$AIR", True, (0, 0, 0))
                    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
                        screen.blit(outline, (text_rect.x + offset[0], text_rect.y + offset[1]))
                    screen.blit(air_text, text_rect)
                except Exception as e:
                    print(f"Error rendering $AIR text: {e}")
            elif proj["type"] == "nuke":
                pygame.draw.rect(screen, NUKE_AURA_COLOR,
                                 (proj["x"] - proj["size"][0] // 2 - 5, proj["y"] - proj["size"][1] // 2 - 5,
                                  proj["size"][0] + 10, proj["size"][1] + 10), border_radius=5)
                pygame.draw.rect(screen, NUKE_COLOR,
                                 (proj["x"] - proj["size"][0] // 2, proj["y"] - proj["size"][1] // 2,
                                  proj["size"][0], proj["size"][1]))
                try:
                    ethos_text = nuke_font.render("ETHOS", True, (255, 255, 255))
                    text_rect = ethos_text.get_rect(center=(proj["x"], proj["y"]))
                    outline = nuke_font.render("ETHOS", True, (0, 0, 0))
                    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (1, 0)]:
                        screen.blit(outline, (text_rect.x + offset[0], text_rect.y + offset[1]))
                    screen.blit(ethos_text, text_rect)
                except Exception as e:
                    print(f"Error rendering ETHOS text: {e}")

        # Draw ETHOS text if in flight mode
        if ethos_timer > 0:
            ethos_text = font.render("ETHOS", True, ETHOS_COLOR)
            ethos_rect = ethos_text.get_rect(center=(player_x + player_width // 2, player_y + player_height + 10))
            screen.blit(ethos_text, ethos_rect)

        # Draw player
        if player_image is not None:
            screen.blit(player_image, (player_x, player_y))
        else:
            pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, player_width, player_height))

        # Draw player health bar
        draw_health_bar(screen, player_x, player_y, player_health, player_max_health)

        # Draw enemies and their health bars
        for enemy in enemies:
            if enemy["image"] is not None:
                screen.blit(enemy["image"], (enemy["x"], enemy["y"]))
            else:
                pygame.draw.rect(screen, ENEMY_COLOR, (enemy["x"], enemy["y"], enemy_width, enemy_height))
            draw_health_bar(screen, enemy["x"], enemy["y"], enemy["health"], max_health=100)

    elif game_state == "victory":
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    game_state = "playing"
                    reset_game()
                elif event.key == K_q:
                    running = False

        screen.fill(VICTORY_BG_COLOR)
        victory_text = title_font.render("ETHOS VICTORY", True, VICTORY_TEXT_COLOR)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(victory_text, victory_rect)
        restart_text = title_font.render("RESTART ROYALE (R)", True, VICTORY_TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
        quit_text = title_font.render("QUIT (Q)", True, VICTORY_TEXT_COLOR)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(quit_text, quit_rect)

    elif game_state == "game_over":
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    game_state = "playing"
                    reset_game()
                elif event.key == K_q:
                    running = False

        screen.fill(GAME_OVER_BG_COLOR)
        game_over_text = title_font.render("ETHOS OVER", True, GAME_OVER_TEXT_COLOR)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)
        restart_text = title_font.render("RESTART ROYALE (R)", True, GAME_OVER_TEXT_COLOR)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text, restart_rect)
        quit_text = title_font.render("QUIT (Q)", True, GAME_OVER_TEXT_COLOR)
        quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        screen.blit(quit_text, quit_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()