import pygame as pg
from settings import *
from raycast import raycast


# файл для уменьшения писанины, тут отрисовка и всё что с ней связано
class Draw:
    def __init__(self, sc):
        self.sc = sc
        self.font = pg.font.SysFont("Arial", 36, bold=True)    
        self.textures = {
            1: pg.image.load("images/wspsh1.jpg").convert(),
            2: pg.image.load("images/wspsh2.jpg").convert()
        }
    def bg(self, angle, color_floor, texture, image, color_sky):
        
        if image == True:
            sky_offset = -5 * degrees(angle) % width
            s = pg.image.load(texture).convert()
            self.sc.blit(s, (sky_offset, 0))
            self.sc.blit(s, (sky_offset - width, 0))
            self.sc.blit(s, (sky_offset + width, 0))
        else:
            pg.draw.rect(self.sc, color_sky, (0, 0, width, half_height))
        pg.draw.rect(self.sc, color_floor, (0,  half_height, width, half_height))
    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.sc.blit(object, object_pos)
    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, pg.Color("red"))
        self.sc.blit(render, fps_pos)