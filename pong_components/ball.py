from settings import *
import pygame
import random
import math
class Ball:
    MAX_VEL = 5
    RADIUS = 7
    COLOR = WHITE
    def __init__(self, x, y):
        self.x = self.original_x = x
        self.y = self.original_y = y
        
        angle = self._get_random_angle(-30, 30,[0])
        pos = 1 if random.random() < 0.5 else -1
        
        self.radius = BALL_RADIUS
        self.x_vel = pos * abs(math.cos(angle) * self.MAX_VEL)
        self.y_vel = math.sin(angle) * self.MAX_VEL
        
    def _get_random_angle(self, min_angle, max_angle, excluded):
        angle = 0
        while angle in excluded:
            angle = math.radians(random.randrange(min_angle, max_angle))
        return angle
    
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y),self.radius)
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1