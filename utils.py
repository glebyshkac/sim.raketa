import random

def check_hit(rocket, air_defenses, rtv):
    if not rocket.is_active():
        return False
    detected_pos = rtv.get_rocket_position_with_error(rocket)
    for ad in air_defenses:
        dist = ((detected_pos[0] - ad.position[0]) ** 2 + (detected_pos[1] - ad.position[1]) ** 2) ** 0.5
        if dist < ad.radius and random.random() < ad.hit_probability:
            rocket.destroy()
            return True
    return False
