﻿# Pong-AI
Beginner Project to start using pytorch together with pygame

How to run:
in main.py 138/139 line

  use this to train the ai
    run_neat(config) # train ai
  
  use this to test the ai against urself (arrow key up,down)
    run_best_ai(config) # test ai against human player
    
    
How to save the checkpoint:
in main.py 110 line

  uncomment this line and the checkpoint number should be the one you have saved after running the code for an while
    #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-44")
