# -------
# MODULES
# -------
import pygame
import os # operating system = find path to the images in our Assets folder
pygame.font.init() # initialize pygame font library
pygame.mixer.init()

# ------
# WINDOW
# ------
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Ship")
BORDER = pygame.Rect((WIDTH//2-5), 0, 10, HEIGHT)

# -----
# SOUND
# -----
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))


# -----------
# COLOUR/FONT
# -----------
BORDER_COL = (0, 0, 0)
YELLOW = (226, 224, 59)
RED = (240, 39, 54)
HEALTH_COL = (242, 84, 103)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)


# ---------
# VARAIBLES
# ---------
FPS = 60
VEL = 5 # space_ship velocity
BULLET_VEL = 7
MAX_BULLET = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40


# --------------
# USER UNIQUE ID
# --------------
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


# ------
# IMAGES
# ------
# YELLOW_SPACESHIP_IMAGE & RED_SPACESHIP_IMAGE are 'surfaces'
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


# ------------
# GAME ELEMENT
# ------------
def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    # 0,0 coordinate is top left
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BORDER_COL, BORDER)

    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, HEALTH_COL)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, HEALTH_COL)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # .blit() when u wanna draw 'surface' on the screen
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update() # need to manually update to see difference

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255,255,255))
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, 
                         HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) # pause the game for 5 sec

# -------------------------
# SPACESHIP/BULLET MOVEMENT
# -------------------------
def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and (yellow.x-VEL > 0): #LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and (yellow.x+VEL+yellow.height < BORDER.x): #RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and (yellow.y-VEL > 0): #UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and (yellow.y+VEL+yellow.width < HEIGHT): #DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and (red.x-VEL > BORDER.x+10): #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and (red.x+VEL+red.height < WIDTH): #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and (red.y-VEL > 0): #UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and (red.y+VEL+red.width < HEIGHT): #DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): # only works if both objects are .Rect()
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH: # prevent bullets to go off-screen
            yellow_bullets.remove(bullet)
    
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL        
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


# ----
# MAIN
# ----
def main():
    # a rectangle to see where these spaceship are going
    # .Rect(x, y, width, height)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    yellow_bullets = []
    red_bullets = []

    yellow_health = 10
    red_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # everyone has const frame rate (refresh) or <=60
        for event in pygame.event.get(): # get list of all the events
            if event.type == pygame.QUIT: # when u press the 'x' on the window
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET: # LEFT SHIFT for shooting
                    bullet = pygame.Rect(yellow.x + yellow.height, yellow.y + yellow.width//2 - 2, 10, 4)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET: # RIGHT SHIFT for shooting
                    bullet = pygame.Rect(red.x, red.y + red.width//2 - 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        # this method allows to have many keys be pressed at once
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()


# ensure that game only starts when this file is run
if __name__ == "__main__":
    main()