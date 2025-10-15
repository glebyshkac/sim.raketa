import pygame
import random
import time
from screen import Screen
from objects import RocketLauncher, Rocket, AirDefense, RTV
from utils import check_hit

def run_game():
    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

    screen = Screen(1550, 650)
    clock = pygame.time.Clock()

    try:
        pygame.mixer.music.load('assets/battle.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
    except:
        print("battle.wav не знайдено")

    try:
        hit_sound = pygame.mixer.Sound('assets/hit.wav')
    except:
        hit_sound = None

    try:
        boom_sound = pygame.mixer.Sound('assets/boom.wav')
    except:
        boom_sound = None

    launchers = []
    for _ in range(random.randint(3, 5)):
        pos = (random.randint(1450, 1530), random.randint(50, 600))
        launcher = RocketLauncher(pos)
        for _ in range(random.randint(3, 6)):
            rocket = Rocket(launcher, speed=180, weight=500, range_=80000)
            launcher.add_rocket(rocket)
        launchers.append(launcher)

    targets = [(random.randint(50, 500), random.randint(50, 600)) for _ in range(40)]

    air_defenses = []
    for _ in range(random.randint(3, 5)):
        house = random.choice(targets)
        pos = (house[0] + random.randint(40, 70), house[1] + random.randint(-30, 30))
        air_defenses.append(AirDefense(pos))

    rtv = RTV()
    active_rockets = []
    start_time = time.time()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        current_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for launcher in launchers:
            launcher.auto_launch(targets, interval=2, current_time=current_time, active_rockets=active_rockets)

        for rocket in active_rockets[:]:
            rocket.update(dt)

            if check_hit(rocket, air_defenses, rtv):
                if hit_sound: hit_sound.play()
                if boom_sound: boom_sound.play()

            if not rocket.is_active() and not rocket.destroyed:
                active_rockets.remove(rocket)
            elif rocket.destroyed and time.time() - rocket.explosion_time >= 0.5:
                active_rockets.remove(rocket)

        screen.draw_background()
        screen.draw_launchers(launchers)
        screen.draw_targets(targets)
        screen.draw_rockets(active_rockets)
        screen.draw_air_defenses(air_defenses)
        screen.flip()

    pygame.quit()
