import pygame as pg
from settings import *
from raycast import raycastingwalls
from player import *
from map import *
from math import *
from draw import *
from sprites import *

# инициация всех классов и модулей\
sprites = Sprites()
player = Player(10, 2, 2, sprites)
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((width, height))
pg.mouse.set_visible(False)
pg.display.set_caption("Abordajer")
draw = Draw(screen)
clock = pg.time.Clock()

# основной цикл
while True:
    keys = pg.key.get_pressed()
    player.move()
    screen.fill((0, 0, 0))

    draw.bg(player.p_angle, pg.Color("darkgray"), "images/cosmos.jpg", False, pg.Color("black"))
    walls = raycastingwalls(player, draw.textures)
    draw.world(walls + [obj.object_locate(player) for obj in sprites.list_of_objects])
    draw.fps(clock)
    
    pygame.display.flip();
    clock.tick(120)

# обработка нажатий и т.д
    for event in pg.event.get():
        if keys[pg.K_ESCAPE]:
            exit()
        if event.type == pg.QUIT:
            exit()
    
    