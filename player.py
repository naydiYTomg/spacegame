import pygame as pg
from math import *
from settings import *
from map import coll_walls

# тут сам игрок
class Player():
    def __init__(self, hp, damage, speed, sprites):
        self.x, self.y = player_pos
        self.hp = hp
        self.sprites = sprites
        self.damage = damage
        self.speed = speed
        self.p_angle = angle
        self.side = 50
        self.rect = pg.Rect(*player_pos, self.side, self.side)
        self.collision_sprites = [pg.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_objects if obj.blocked]
        self.collision_list = coll_walls + self.collision_sprites
        self.sensitivity = 0.004


    @property
    def pos(self):
        return (self.x, self.y)
    
    # здесь скрипт коллизии
    def detect_coll(self, dx, dy):

        # берём позицию игрока
        next_rect = self.rect.copy()

        # пробуем сместить её а заданные точки
        next_rect.move_ip(dx, dy)

        # получаем коллизии
        hit_indexes = next_rect.collidelistall(self.collision_list)

        # тут высчитываем все столкновения
        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0
        self.x += dx
        self.y += dy

    # движение
    def move(self):
        self.keys_c()
        self.rect.center = self.x, self.y
        self.mouse_control()
        self.p_angle %= pi * 2
        
       
    # управление кнопками
    def keys_c(self):
        sin_a = sin(self.p_angle)
        cos_a = cos(self.p_angle)
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx = self.speed * cos_a
            dy = self.speed * sin_a
            self.detect_coll(dx, dy)
        if keys[pg.K_s]:
            dx = -self.speed * cos_a
            dy = -self.speed * sin_a
            self.detect_coll(dx, dy)
        if keys[pg.K_a]:
            dx = self.speed * sin_a
            dy = -self.speed * cos_a
            self.detect_coll(dx, dy)
        if keys[pg.K_d]:
            dx = -self.speed * sin_a
            dy = self.speed * cos_a
            self.detect_coll(dx, dy)
        if keys[pg.K_LEFT]:
            self.p_angle -= 0.02
        if keys[pg.K_RIGHT]:
            self.p_angle += 0.02
    # управление мышкой
    def mouse_control(self):
        if pg.mouse.get_focused():
            difference = pg.mouse.get_pos()[0] - half_width
            pg.mouse.set_pos((half_width, half_height))
            self.p_angle += difference * self.sensitivity