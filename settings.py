from math import *

# тут все настройки

height = 800
width = 1200
half_height = height/2
half_width = width/2
penta_height = 5 * height
double_height = 2 * height
angle = 0
player_pos = (half_width, half_height)
tile = 100

# raycasting
fov = pi/3
half_fov = fov/2
rays = 300
delta_angle = fov / rays
max_depth = 1200

d = rays / (2 * tan(half_fov))
coef_proj = 3 * d * tile

fps_pos = (width - 65, 5)

scale = width // rays

texture_width = 1200
texture_height = 1200
texture_scale = texture_width // tile

map_scale = 5
map_tile = tile // map_scale
map_pos = (0, height - height // map_scale)

center_ray = rays // 2 - 1
fake_rays = 100
fake_rays_range = rays - 1 + 2 * fake_rays