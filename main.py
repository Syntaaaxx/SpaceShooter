import math
import os
import pygame
import random
import time
import sys
import buttons
from createsoundfiles.dashsound import volume


# --- PYINSTALLER PATH FIX ---
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ----------------------------

pygame.init()
pygame.mixer.init()
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)


# background music
# Using resource_path for everything in the assets folder
bgmusic = pygame.mixer.Sound(resource_path(os.path.join("assets", "bgmusic.mp3")))
forest = pygame.mixer.Sound(resource_path(os.path.join("assets", "forest.mp3")))
shop = pygame.mixer.Sound(resource_path(os.path.join("assets", "shop.mp3")))
lostwoods = pygame.mixer.Sound(resource_path(os.path.join("assets", "lostwoods.mp3")))
fairy = pygame.mixer.Sound(resource_path(os.path.join("assets", "fairy.mp3")))
windmillhut = pygame.mixer.Sound(resource_path(os.path.join("assets", "windmillhut.mp3")))
gerudovalley = pygame.mixer.Sound(resource_path(os.path.join("assets", "gerudovalley.mp3")))

playlist = [
    resource_path(os.path.join("assets", "bgmusic.mp3")),
    resource_path(os.path.join("assets", "forest.mp3")),
    resource_path(os.path.join("assets", "shop.mp3")),
    resource_path(os.path.join("assets", "lostwoods.mp3")),
    resource_path(os.path.join("assets", "fairy.mp3")),
    resource_path(os.path.join("assets", "windmillhut.mp3")),
    resource_path(os.path.join("assets", "gerudovalley.mp3"))
]

random.shuffle(playlist)
pygame.mixer.music.load(playlist.pop())
if len(playlist) > 0:
    pygame.mixer.music.queue(playlist.pop())
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# sounds
lasersound1 = pygame.mixer.Sound(resource_path(os.path.join("assets", "laser.mp3")))
xplos = pygame.mixer.Sound(resource_path(os.path.join("assets", "balanced_comet_explosion.wav")))
loser = pygame.mixer.Sound(resource_path(os.path.join("assets", "game_over_8bit.wav")))
fail = pygame.mixer.Sound(resource_path(os.path.join("assets", "fail.wav")))
dashsound = pygame.mixer.Sound(resource_path(os.path.join("assets", "dash_swoosh.wav")))
dashsound.set_volume(1.0)

timer = time.time()
pause = False
white = [255, 255, 255]
black = [0, 0, 0]

pygame.display.set_caption("Space shooter")
pygame.display.set_icon(pygame.image.load(resource_path(os.path.join("assets", "ship.png"))))

window = pygame.display.set_mode([736, 932])
window.fill(black)

# Ship logic
ship = pygame.image.load(resource_path(os.path.join("assets", "ship.png"))).convert_alpha()
ship.set_colorkey(black)
defaultsizeship = (120, 70)
ship = pygame.transform.scale(ship, defaultsizeship)
coords = ship.get_rect()
coords.center = 368, 820

# wallpaper logic
scroll = 0
wallpaper = pygame.image.load(resource_path(os.path.join("assets", "bg.jpg"))).convert()
bg_height = wallpaper.get_height()
tiles = math.ceil(932 / bg_height) + 1

# projectile logic
laser_img = pygame.image.load(resource_path(os.path.join("assets", "laser.png"))).convert_alpha()
defaultsizelaser = (30, 30)
laser_img = pygame.transform.scale(laser_img, defaultsizelaser)
laser_img.set_colorkey(white)

# comets
comet1small = pygame.image.load(resource_path(os.path.join("assets", "comet1small.svg"))).convert_alpha()
comet2small = pygame.image.load(resource_path(os.path.join("assets", "comet2small.svg"))).convert_alpha()
comet1medium = pygame.image.load(resource_path(os.path.join("assets", "comet1medium.svg"))).convert_alpha()
comet2medium = pygame.image.load(resource_path(os.path.join("assets", "comet2medium.svg"))).convert_alpha()
comet1large = pygame.image.load(resource_path(os.path.join("assets", "comet1large.svg"))).convert_alpha()
comet2large = pygame.image.load(resource_path(os.path.join("assets", "comet2large.svg"))).convert_alpha()
comethuge = pygame.image.load(resource_path(os.path.join("assets", "comethuge.svg"))).convert_alpha()
comets = [comet2small, comet1medium, comet2medium, comet2large, comet1large, comethuge]
falling_comets = []
MAX_COMETS = 5
next_comet_spawn = pygame.time.get_ticks() + random.randint(900, 1600)

# explosions
explosion_frames = [
    pygame.image.load(resource_path(os.path.join("assets", "explos1.svg"))).convert_alpha(),
    pygame.image.load(resource_path(os.path.join("assets", "explos2.svg"))).convert_alpha(),
    pygame.image.load(resource_path(os.path.join("assets", "explos3.svg"))).convert_alpha()
]
blue_explosion_frames = [
    pygame.image.load(resource_path(os.path.join("assets", "explos1blue.svg"))).convert_alpha(),
    pygame.image.load(resource_path(os.path.join("assets", "explos2blue.svg"))).convert_alpha(),
    pygame.image.load(resource_path(os.path.join("assets", "explos3blue.svg"))).convert_alpha()
]
active_blue_explosions = []
active_explosions = []
EXPLOSION_FRAME_TIME = 100

lasers = []
LASER_SPEED = 10
shoot_delay = 600
last_shot_time = 0

# Boosts
boostsize = (40, 40)
boost1 = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "boost1.svg"))).convert_alpha(),
                                boostsize)
boost2 = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "boost2.svg"))).convert_alpha(),
                                boostsize)
boost3 = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "boost3.svg"))).convert_alpha(),
                                boostsize)
boost4 = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "boost4.svg"))).convert_alpha(),
                                boostsize)
boostlist = [boost1, boost2, boost3, boost4]

# hearts
heart = pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "heart.svg"))).convert_alpha(),
                               (42, 42))
emptyheart = pygame.transform.scale(
    pygame.image.load(resource_path(os.path.join("assets", "emptyheart.svg"))).convert_alpha(), (42, 42))

lives = 3
MAX_LIVES = 3
hit_cooldown = 2000
last_hit_time = 0
clock = pygame.time.Clock()

boosts = 0
boost_frame_index = 0
boost_timer = 0
boost_animation_speed = 150

is_dashing = False
dash_direction = 0
dash_timer = 0
dash_duration = 200
dash_cooldown_timer = 0
dash_cooldown_max = 3000
dash_speed = 20

dash_frames = [
    pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "swoosh1.svg"))).convert_alpha(),
                           (150, 70)),
    pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "swoosh2.svg"))).convert_alpha(),
                           (150, 70)),
    pygame.transform.scale(pygame.image.load(resource_path(os.path.join("assets", "swoosh3.svg"))).convert_alpha(),
                           (150, 70)),
]
dash_frame_index = 0
dash_anim_timer = 0
DASH_ANIM_SPEED = 50

test = True


def moveship():
    global coords, is_dashing, dash_direction, dash_timer, dash_cooldown_timer
    keys = pygame.key.get_pressed()
    if pause: return
    if is_dashing:
        coords.centerx += dash_direction * dash_speed
        if coords.left < 0:
            coords.left = 0
            is_dashing = False
        if coords.right > 736:
            coords.right = 736
            is_dashing = False
    else:
        if keys[pygame.K_LEFT] and coords.centerx > 50:
            coords.centerx -= 8
        if keys[pygame.K_RIGHT] and coords.centerx < 686:
            coords.centerx += 8


def shoot():
    global last_shot_time
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and current_time - last_shot_time > shoot_delay and not pause:
        new_laser = laser_img.get_rect()
        new_laser.centerx = coords.centerx
        new_laser.bottom = coords.top
        lasers.append(new_laser)
        last_shot_time = current_time
        lasersound1.play().set_volume(0.2)


def cometdrop():
    if not pause:
        comet_img = random.choice(comets)
        comet_rect = comet_img.get_rect()
        comet_rect.x = random.randint(0, 720 - comet_rect.width)
        comet_rect.y = random.randint(-200, -50)
        comet_speed = random.choice([1, 2, 4, 5, 8])
        falling_comets.append({"image": comet_img, "rect": comet_rect, "speed": comet_speed})


def draw_hearts():
    empty_hearts = MAX_LIVES - lives
    for i in range(MAX_LIVES):
        x, y = 10, 300 + i * 50
        window.blit(emptyheart if i < empty_hearts else heart, (x, y))


def get_highscore():
    try:
        with open(resource_path("highscore.txt"), "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_highscore(score):
    highscore = get_highscore()
    if score > highscore:
        with open(resource_path("highscore.txt"), "w") as f:
            f.write(str(score))


font = pygame.font.SysFont("gillsansultra", 20)
font2 = pygame.font.SysFont("gillsansultra", 35)
TEXT_COL = (255, 255, 255)

resume_image = pygame.image.load(resource_path(os.path.join("assets", "playbutton.png"))).convert_alpha()
resume_button = buttons.Button(215, 350, resume_image, 1)

timerevent = pygame.event.custom_type()
pygame.time.set_timer(timerevent, 1000)
ticker = 0
ticker2 = 0
tickerdestroyed = 0


def drawtext(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


run = True
endofgame = False
while run:
    dt = clock.tick(60)

    if boosts >= len(boostlist):
        boosts = 0

    window.fill(black)
    for i in range(0, tiles):
        window.blit(wallpaper, (0, (i * bg_height) + scroll - bg_height))

    scroll += 3
    if scroll >= bg_height:
        scroll = 0

    if not pause:
        if dash_cooldown_timer < dash_cooldown_max:
            dash_cooldown_timer += dt
        if is_dashing:
            dash_timer += dt
            dash_anim_timer += dt
            if dash_anim_timer >= DASH_ANIM_SPEED:
                dash_anim_timer = 0
                dash_frame_index = (dash_frame_index + 1) % len(dash_frames)
            if dash_timer >= dash_duration:
                is_dashing = False
                dash_timer = 0
                dash_frame_index = 0

    moveship()
    shoot()

    if is_dashing:
        current_dash_img = dash_frames[dash_frame_index]
        dash_rect = current_dash_img.get_rect()
        dash_rect.center = coords.center
        dash_rect.x -= dash_direction * 60
        if dash_direction == -1:
            current_dash_img = pygame.transform.flip(current_dash_img, True, False)
        window.blit(current_dash_img, dash_rect)

    boost_timer += dt
    if boost_timer >= boost_animation_speed:
        boost_timer = 0
        boost_frame_index = (boost_frame_index + 1) % len(boostlist)

    for laser in lasers[:]:
        laser.y -= LASER_SPEED
        if laser.bottom < 0:
            lasers.remove(laser)
        else:
            window.blit(laser_img, laser)

    current_boost = boostlist[boost_frame_index]
    boost_rect = current_boost.get_rect()
    boost_rect.midtop = (coords.centerx, coords.bottom - 10)
    window.blit(current_boost, boost_rect)
    window.blit(ship, coords)
    current_time = pygame.time.get_ticks()

    for explosion in active_explosions[:]:
        if not pause:
            explosion["timer"] += dt
            if explosion["timer"] >= EXPLOSION_FRAME_TIME:
                explosion["timer"] = 0
                explosion["frame"] += 1
        if explosion["frame"] >= len(explosion_frames):
            active_explosions.remove(explosion)
        else:
            window.blit(explosion_frames[explosion["frame"]], explosion["rect"])

    for explosionb in active_blue_explosions[:]:
        if not pause:
            explosionb["timer"] += dt
            if explosionb["timer"] >= EXPLOSION_FRAME_TIME:
                explosionb["timer"] = 0
                explosionb["frame"] += 1
        if explosionb["frame"] >= len(blue_explosion_frames):
            active_blue_explosions.remove(explosionb)
        else:
            window.blit(blue_explosion_frames[explosionb["frame"]], explosionb["rect"])

    for laser in lasers[:]:
        for comet in falling_comets[:]:
            if comet["rect"].colliderect(laser) and not pause:
                explosion_rect = explosion_frames[0].get_rect()
                explosion_rect.center = comet["rect"].center
                active_explosions.append({"rect": explosion_rect, "frame": 0, "timer": 0})
                xplos.play()
                falling_comets.remove(comet)
                if laser in lasers: lasers.remove(laser)
                tickerdestroyed += 1
                break

    for comet in falling_comets[:]:
        if comet["rect"].colliderect(coords) and not pause:
            if current_time - last_hit_time > hit_cooldown:
                fail.play()
                explosion_blue_rect = blue_explosion_frames[0].get_rect()
                explosion_blue_rect.center = comet["rect"].center
                active_blue_explosions.append({"rect": explosion_blue_rect, "frame": 0, "timer": 0})
                lives -= 1
                last_hit_time = current_time
                falling_comets.remove(comet)
                if lives <= 0:
                    lives = 0
                    save_highscore(tickerdestroyed)
                    pause = True
                    endofgame = True

    if current_time >= next_comet_spawn:
        if len(falling_comets) < MAX_COMETS:
            cometdrop()
        next_comet_spawn = current_time + random.randint(400, 1200)

    for comet in falling_comets[:]:
        comet["rect"].y += comet["speed"]
        if comet["rect"].top > 932 and not pause:
            falling_comets.remove(comet)
            if tickerdestroyed > 0:
                tickerdestroyed -= 1
        else:
            window.blit(comet["image"], comet["rect"])

    if pause:
        if endofgame:
            drawtext("GAME OVER", font2, TEXT_COL, 235, 260)
            drawtext(f"Score: {tickerdestroyed}", font, TEXT_COL, 280, 500)
            drawtext(f"Highscore: {get_highscore()}", font, TEXT_COL, 280, 530)
            drawtext("Click continue to restart", font, TEXT_COL, 210, 320)
            pygame.mixer.music.pause()
            if test:
                loser.play().set_volume(0.2)
                test = False

        if resume_button.draw(window):
            if endofgame:
                lives = MAX_LIVES
                endofgame = False
                tickerdestroyed = ticker = ticker2 = 0
                falling_comets.clear()
                lasers.clear()
                coords.center = 368, 820
                last_hit_time = pygame.time.get_ticks()
                test = True
            pause = False
            pygame.mixer.music.unpause()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not endofgame:
                pause = not pause
                pygame.mixer.music.pause() if pause else pygame.mixer.music.unpause()
            if event.key == pygame.K_d and not pause and not is_dashing:
                if dash_cooldown_timer >= dash_cooldown_max:
                    keys = pygame.key.get_pressed()
                    dash_direction = -1 if keys[pygame.K_LEFT] else 1
                    is_dashing = True
                    dash_timer = dash_cooldown_timer = 0
                    dashsound.play()
            if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and pause:
                if endofgame:
                    lives = MAX_LIVES
                    endofgame = False
                    tickerdestroyed = ticker = ticker2 = 0
                    falling_comets.clear()
                    lasers.clear()
                    coords.center = 368, 820
                    last_hit_time = pygame.time.get_ticks()
                    test = True
                pause = False
                pygame.mixer.music.unpause()
            if event.key == pygame.K_m:
                LASER_SPEED = 100
                shoot_delay = 10
            if event.key == pygame.K_r:
                LASER_SPEED = 10
                shoot_delay = 600
        if event.type == timerevent:
            ticker += 1
            if ticker == 60:
                ticker = 0
                ticker2 += 1

    draw_hearts()
    # DASH BAR
    bar_width, bar_height, bar_x, bar_y = 100, 10, 20, 900
    pygame.draw.rect(window, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    progress = (dash_cooldown_timer / dash_cooldown_max) * bar_width
    pygame.draw.rect(window, (0, 200, 255), (bar_x, bar_y, progress, bar_height))

    drawtext("DASH", font, TEXT_COL, bar_x, bar_y - 30)
    drawtext("Press ESC to pause", font, TEXT_COL, 10, 20)
    drawtext(f"{ticker2}:{ticker if ticker < 10 else ticker}", font2, TEXT_COL, 630, 5)
    drawtext(str(tickerdestroyed), font2, TEXT_COL, 354, 885)
    pygame.display.update()
    pygame.time.delay(3)
    boosts += 1

pygame.quit()
