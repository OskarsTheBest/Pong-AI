import pygame
import neat
import os
import random
import pickle
from pong_components import Game
from settings import *


class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball


    def ai_game(self, genome, config):
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                        
            output = net.activate((self.right_paddle.y, self.ball.y , abs(self.right_paddle.x - self.ball.x)))
            decis = output.index(max(output))
            if decis == 0:
                pass
            elif decis == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)
            keys = pygame.key.get_pressed()    
            if keys[pygame.K_w]:
                self.game.move_paddle(left=False, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()
        
    def train_ai(self, genome1, genome2, config):
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
        
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    
            output1 = net1.activate((self.left_paddle.y, self.ball.y , abs(self.left_paddle.x - self.ball.x)))
            decis1 = output1.index(max(output1))
            if decis1 == 0:
                pass
            elif decis1 == 1:
                self.game.move_paddle(left=True, up=True)
            else:
                self.game.move_paddle(left=True, up=False)
                
            output2 = net2.activate((self.right_paddle.y, self.ball.y , abs(self.right_paddle.x - self.ball.x)))
            decis2 = output2.index(max(output2))
            if decis2 == 0:
                pass
            elif decis2 == 1:
                self.game.move_paddle(left=False, up=True)
            else:
                self.game.move_paddle(left=False, up=False)
            game_info = self.game.loop()
            self.game.loop()
            self.game.draw(False, True)
            pygame.display.update()
        
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.right_hits > 50:
                self.fitness_calc(genome1, genome2, game_info)
                break
                
        
    def fitness_calc(self, genome1, genome2, game_info):
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits
        
    
def eval_genomes(genomes, config):
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    
    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) -1:
            break
        genome1.fitness = 0
        
        
        for genome_id2, genome2 in genomes[i+1:]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)

    
    
def run_neat(config):
    #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-44")
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    
    #gets the best ai who after 50 generations
    winner = p.run(eval_genomes, 50)
    with open("best_ai.pickle", "wb") as f:
        pickle.dump(winner, f)
        
def run_best_ai(config):
    with open("best_ai.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    width, height = 700, 500
    window = pygame.display.set_mode((width, height))
    pong_components = PongGame(window, width, height)
    pong_components.ai_game(winner, config)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path )
    
    #run_neat(config) # train ai
    run_best_ai(config) # test ai against human player