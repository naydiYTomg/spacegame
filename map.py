import pygame
from settings import *
import numpy as np
import numba as nb
from numba import njit, int32, typed, types, typeof
from numba.core import types
from numba.typed import Dict
# тут карты


_ = False
matrix_map = [
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,_,_,_,1],
    [1,2,_,_,_,_,_,_,_,_,_,_,_,2,_,_,_,1],
    [1,2,_,_,_,_,_,_,_,_,_,_,_,2,_,_,_,1],
    [1,1,1,1,1,1,_,_,_,1,1,1,1,1,1,1,_,1],
    [1,_,_,_,_,1,_,_,_,1,_,_,_,_,_,1,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,_,1,_,1],
    [1,_,_,_,_,1,_,_,_,1,_,_,_,_,_,1,_,1],
    [1,1,1,1,1,1,_,_,_,1,1,1,1,1,1,1,_,1],
    [1,1,1,1,1,1,_,_,_,1,1,1,1,1,1,1,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,1,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,1,_,_,1],
    [1,_,_,_,_,_,_,_,_,_,_,_,_,_,1,_,_,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
world_width = len(matrix_map[0]) * tile
world_height = len(matrix_map) * tile
coll_walls = []
world_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type = int32)
# по символам определяем, что это такое
for j, row in enumerate(matrix_map):
    for i, char in enumerate(row):
        if char:
            coll_walls.append(pygame.Rect(i * tile, j * tile, tile, tile))
            if char == 1:
                world_map[(i * tile, j * tile)] = 1
            elif char == 2:
                world_map[(i * tile, j * tile)] = 2;