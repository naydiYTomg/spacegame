import pygame
from settings import *
from collections import deque

# чёто со спрайтами
class Sprites:
    def __init__(self):

        self.list_of_objects = []


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.viewing_angles = parameters['viewing_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.blocked = parameters['blocked']
        self.side = 30
        self.animation_count = 0
        self.x, self.y = pos[0] * tile, pos[1] * tile
        self.pos = self.x - self.side // 2, self.y - self.side // 2
        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.object)}

    def object_locate(self, player):

        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = sqrt(dx ** 2 + dy ** 2) 

        theta = atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += pi * 2

        delta_rays = int(gamma / delta_angle)
        current_ray = center_ray + delta_rays
        distance_to_sprite *= cos(half_fov - current_ray * delta_angle)

        fake_ray = current_ray + fake_rays
        if 0 <= fake_ray <= fake_rays_range and distance_to_sprite > 30:
            proj_height = min(int(coef_proj / distance_to_sprite * self.scale), double_height)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            # choosing sprite for angle
            if self.viewing_angles:
                if theta < 0:
                    theta += pi * 2
                theta = 360 - int(degrees(theta))

                for angles in self.sprite_angles:
                    if theta in angles:
                        self.object = self.sprite_positions[angles]
                        break

            # sprite animation
            sprite_object = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0

            # sprite scale and pos
            sprite_pos = (current_ray * scale - half_proj_height, half_height - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False,)