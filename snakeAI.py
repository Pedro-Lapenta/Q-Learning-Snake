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

class SnakeGame:
    def __init__(self, width = 640, height = 480):
        self.width = width
        self.height = height

        self.frame_interations = 0
        self.direction = Direction.RIGHT  # Inicializa direção

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
            self._place_food()

    def is_reward(self):
        if self.head.x == self.food.x and self.head.y == self.food.y:
            return True
        else:
            return False
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Bateu na parede
        if pt.x > self.width - 20 or pt.x < 0 or pt.y > self.height - 20 or pt.y < 0:
            return True
        # Bateu no corpo
        if pt in self.snake[1:]:
            return True
        
        return False

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

            self.head = Point(x, y)

            # Adiciona a nova posicao da cabeca ao inicio da lista do corpo
            self.snake.insert(0, self.head)

            # Verifica se comeu uma maca
            if self.is_reward():
                self.score += 1
                self._place_food()
            
            else:
                self.snake.pop()

    def get_state(self):
        head = self.snake[0]

        # Pontos de perigo
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        # Direção atual
        dir_l = self.direction == Direction.LEFT
        dir_r = self.direction == Direction.RIGHT
        dir_u = self.direction == Direction.UP
        dir_d = self.direction == Direction.DOWN

        state = [
            # Perigo reto
            (dir_r and self.is_collision(point_r)) or 
            (dir_l and self.is_collision(point_l)) or 
            (dir_u and self.is_collision(point_u)) or 
            (dir_d and self.is_collision(point_d)),

            # Perigo na direita
            (dir_u and self.is_collision(point_r)) or 
            (dir_d and self.is_collision(point_l)) or 
            (dir_l and self.is_collision(point_u)) or 
            (dir_r and self.is_collision(point_d)),

            # Perigo na esquerda
            (dir_d and self.is_collision(point_r)) or 
            (dir_u and self.is_collision(point_l)) or 
            (dir_r and self.is_collision(point_u)) or 
            (dir_l and self.is_collision(point_d)),
            
            # Direção de movimento
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Localização da comida
            self.food.x < self.head.x,  # comida à esquerda
            self.food.x > self.head.x,  # comida à direita
            self.food.y < self.head.y,  # comida acima
            self.food.y > self.head.y   # comida abaixo
            ]

        return np.array(state, dtype=int)
    
    def play_step(self, action):
        self.frame_interations += 1

        self._move(action)

        reward = 0
        game_over = False

        if self.is_collision() == False or self.frame_interations > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        elif self.is_reward() == True:
            self.score += 1
            reward = 10
            self._place_food

        else:
            reward = -0.1

        return reward, game_over, self.score