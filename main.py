import pygame
from pong_components import Game
from settings import *

window = pygame.display.set_mode((WIDTH, HEIGHT))

game = Game(window, WIDTH, HEIGHT)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUITE:
            run = False
            break
    game.loop()
    game.draw()
    pygame.display.update()
    
pygame.quite()