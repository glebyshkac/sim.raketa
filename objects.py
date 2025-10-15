import time
import math
import random

class Rocket:
    def __init__(self, launcher, speed, weight, range_):
        self.launcher = launcher
        self.speed = speed
        self.weight = weight
        self.range = range_
        self.g = 9.8
        self.target = None
        self.x, self.y = launcher.position
        self.z = 0
        self.vx = self.vy = self.vz = 0
        self.t = 0
        self.z_max = 0
        self.active = True
        self.destroyed = False

    def destroy(self):
        self.active = False
        self.destroyed = True
        self.explosion_time = time.time()
        self.explosion_pos = (int(self.x), int(self.y))

    def set_target(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        angle = math.atan2(dy, dx)
        self.vx = self.speed * math.cos(angle)
        self.vy = self.speed * math.sin(angle)
        self.vz = self.speed * 0.3
        self.z_max = (self.vz ** 2) / (2 * self.g)
        self.target = target

    def update(self, dt):
        if not self.active or not self.target:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z = self.vz * self.t - 0.5 * self.g * (self.t ** 2)
        self.t += dt
        if self.z < 0:
            self.active = False

    def get_position(self):
        z_norm = min(1, self.z / self.z_max) if self.z_max > 0 else 0
        return (int(self.x), int(self.y), z_norm)

    def is_active(self):
        return self.active

class RocketLauncher:
    def __init__(self, position):
        self.position = position
        self.rockets = []
        self.last_shot_time = 0

    def add_rocket(self, rocket):
        self.rockets.append(rocket)

    def auto_launch(self, targets, interval, current_time, active_rockets):
        if self.rockets and targets and (current_time - self.last_shot_time > interval):
            target = random.choice(targets)
            rocket = self.rockets.pop(0)
            rocket.set_target(target)
            active_rockets.append(rocket)
            self.last_shot_time = current_time

class AirDefense:
    def __init__(self, position):
        self.position = position
        self.radius = 120
        self.hit_probability = 0.6

class RTV:
    def __init__(self):
        self.error_sigma = 10

    def get_rocket_position_with_error(self, rocket):
        x, y, z = rocket.get_position()
        error_x = random.gauss(0, self.error_sigma / 50)
        error_y = random.gauss(0, self.error_sigma / 50)
        error_z = random.gauss(0, self.error_sigma / 50)
        return (x + error_x, y + error_y, z + error_z)
