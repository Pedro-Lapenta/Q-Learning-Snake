import numpy as np
import pygame
import random
from enum import Enum

# Cores
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

BLOCK_SIZE = 20
SPEED = 40  # Velocidade do jogo para visualização

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

class SnakeGame:
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        
        # Inicializar pygame
        pygame.init()
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake AI Training')
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.Font(None, 25)  # None usa a fonte padrão do pygame

        self.reset()

    def reset(self):
        self.frame_interations = 0
        self.direction = Direction.RIGHT

        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        self.food = Point(x, y)

        if self.food in self.snake:
            self._place_food()

    def is_reward(self):
        return self.head.x == self.food.x and self.head.y == self.food.y
    
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        
        # Bateu na parede
        if pt.x >= self.width or pt.x < 0 or pt.y >= self.height or pt.y < 0:
            return True
        # Bateu no corpo
        if pt in self.snake[1:]:
            return True
        
        return False

    def _move(self, action):
        clockwise_map = (Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP)
        idx = clockwise_map.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clockwise_map[idx]
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clockwise_map[next_idx]
        elif np.array_equal(action, [0, 0, 1]):
            next_idx = (idx - 1) % 4
            new_direction = clockwise_map[next_idx]

        self.direction = new_direction

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE

        self.head = Point(x, y)
        self.snake.insert(0, self.head)

        reward = False
        if self.is_reward():
            self.score += 1
            reward = True
            self._place_food()
        else:
            self.snake.pop()
            
        return reward

    def get_state(self):
        head = self.snake[0]

        point_l = Point(head.x - BLOCK_SIZE, head.y)
        point_r = Point(head.x + BLOCK_SIZE, head.y)
        point_u = Point(head.x, head.y - BLOCK_SIZE)
        point_d = Point(head.x, head.y + BLOCK_SIZE)
        
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
            
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            self.food.x < self.head.x,
            self.food.x > self.head.x,
            self.food.y < self.head.y,
            self.food.y > self.head.y
        ]

        return np.array(state, dtype=int)
    
    def play_step(self, action, show_ui=True):
        self.frame_interations += 1

        # Lidar com eventos do pygame apenas quando mostrando UI
        if show_ui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        # Move e verifica se comeu
        reward_eaten = self._move(action)

        reward = 0
        game_over = False

        if self.is_collision() or self.frame_interations > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if reward_eaten:
            reward = 10
        else:
            reward = 0

        # Atualizar display apenas quando necessário
        if show_ui:
            self._update_ui()
            self.clock.tick(SPEED)

        return reward, game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)
        
        # Desenhar cobra
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        
        # Desenhar cabeça da cobra
        head = self.snake[0]
        pygame.draw.rect(self.display, GREEN, pygame.Rect(head.x, head.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(head.x+4, head.y+4, 12, 12))
        
        # Desenhar comida
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Mostrar score
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        
        pygame.display.flip()

    def close(self):
        pygame.quit()
