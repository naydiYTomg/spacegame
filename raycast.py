import pygame as pg
from map import world_map, world_height, world_width
from settings import *
from math import *
from numba import njit

@njit(fastmath=True)
def mapping(a, b):
    return (a // tile) * tile, (b // tile) * tile


@njit(fastmath=True)
def raycast(player_pos, player_angle, world_map):
    casted_walls = []
    ox, oy = player_pos
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - half_fov
    # сам рейкастинг
    for ray in range(rays):
        sin_a = sin(cur_angle)
        cos_a = cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # тут просчитываются вертикали и горизонтали
        x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, world_width, tile):
            
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * tile

        
        y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, world_height, tile):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * tile

        # просчитывание столкновений лучей и их запуск
        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % tile
        depth *= cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min(int(coef_proj / depth), penta_height)

        
        # sc.blit(wall_column, (ray * scale, half_height - proj_height // 2))
        casted_walls.append((depth, offset, proj_height, texture))
        cur_angle += delta_angle
    return casted_walls

def raycastingwalls(player, textures):
    casted_walls = raycast(player.pos, player.p_angle, world_map)
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        wall_column = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        wall_column = pg.transform.scale(wall_column, (scale, proj_height))
        wall_pos = (ray * scale, half_height - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    return walls











        # берём синусы и косинусы текущего угла
        # sin_a = sin(cur_angle)
        # cos_a = cos(cur_angle)
        # sin_a = sin_a if sin_a else 0.000001
        # cos_a = cos_a if cos_a else 0.000001
        

        # x, dx = (xm + tile, 1) if cos_a >= 0 else (xm, -1)
        
        # # тут высчитывабтся столкновения лучей с вертикалями и горизонталями, эта конструкция увеличивает фпс на порядки
        # for i in range(0, width, tile):
        #     depth_v = (x - ox) / cos_a
        #     yv = oy + depth_v * sin_a
        #     tile_v = mapping(x + dx, yv)
        #     if tile_v in world_map:
        #         texture_v = world_map[tile_v]
        #         break
        #     x += dx * tile
        # y, dy = (ym + tile, 1) if sin_a >= 0 else (ym, -1)
        # for i in range(0, height, tile):
        #     depth_h = (y - oy) / sin_a
        #     xh = ox + depth_h * cos_a
        #     tile_h = mapping(x, y + dy)
        #     if tile_h in world_map:
        #         texture_h = world_map[tile_h]
        #         break
        #     y += dy * tile

        # # здесь процесс отрисовки псевдо-3д
        # depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        # offset = int(offset) % tile
        # depth *= cos(player_angle - cur_angle)
        # depth = max(depth, 0.00001)
        # proj_height = min(int(coef_proj / depth), 2 * height)

        # wall_coll = textures[texture].subsurface(offset * texture_scale, 0, texture_scale, texture_height)
        # wall_coll = pg.transform.scale(wall_coll, (scale, proj_height))
        # sc.blit(wall_coll, (ray * scale, half_height - proj_height // 2))
        # # c = 255 / (1 + depth * depth * 0.00002)
        # # color = (c, c // 2, c // 3)
        # # pg.draw.rect(sc, color, (ray * scale, half_height - proj_height // 2, scale, proj_height))
        # # break
        # cur_angle += delta_angle