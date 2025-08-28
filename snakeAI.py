import numpy as np
import pygame
import random
from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SnakeGameAI:
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height

        # Inicia posicao da cabeca da cobra no meio da tela 
        self.head = Point(self.width/2, self.height/2)

        # Inicia a posicao do corpo da cobra a 20 e 40 pixels da cabeca
        self.snake = [self.head,
                      Point(self.head.x-20, self.head.y-20),
                      Point(self.head.x-40, self.head.y-40)]        

        self.score = 0
        self.food = None
        self._place_food()

def _place_food(self):
    x = random.randint(0, (self.width-20 // 20) * 20)
    y = random.randint(0, (self.height-20 // 20) * 20)

    self.food = Point(x,y)

    # se a maca for colocada dentro da cobra -> chama a funcao e reposiciona a maca
    if self.food in self.snake:
        _place_food()

def _move(self, action):
        # 1. Atualizar a direção com base na ação
        # [0, 1, 0] -> esquerda
        # [1, 0, 0] -> em frente
        # [0, 0, 1] -> direita

        clockwise_map = (Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP)
        idx = clockwise_map.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_direction = clockwise_map[idx]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx + 1) % 4
            new_direction = clockwise_map[next_idx]
        elif np.array_equal(action, [0,0,1]):
            next_idx = (idx - 1) % 4
            new_direction = clockwise_map[next_idx]

        self.direction = new_direction


        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += 20
        elif self.direction == Direction.LEFT:
            x -= 20
        elif self.direction == Direction.UP:
            y += 20
        elif self.direction == Direction.DOWN:
            y -= 20

        self.head(x, y)

        
        