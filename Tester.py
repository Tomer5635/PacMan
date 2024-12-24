import pygame
import torch
from environment import Game
from DQN_Agent import DQN_Agent
import graphics
import os
from ReplayBuffer import ReplayBuffer
import wandb
WIDTH , HEIGHT = 540,710
def main ():

    pygame.init()
    path = "Data/parameters1"
    bufferPath = "Data/buffer1"
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('PAC MAN')
    game = Game()

    best_score = 0

    ####### params ############
    player = DQN_Agent(path)
    player.load_params(path)
    player.save_param(path)
    player_hat = DQN_Agent()
    player_hat.DQN = player.DQN.copy()
    batch_size = 50
    buffer = ReplayBuffer()
    learning_rate = 0.00001
    epochs = 100
    start_epoch = 0
    C = 3
    loss = torch.tensor(-1,dtype=torch.float32,requires_grad=True)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000], gamma=0.5)
    step = 0
    wandb.init(
    # set the wandb project where this run will be logged
    project="pacman-project",

    # track hyperparameters and run metadata
    config={
    "learning_rate": learning_rate,
    "architecture": "DQN",
    "dataset": "PACMAN",
    "epochs": epochs,
    }
        )
    for epoch in range(start_epoch, epochs):
            game = Game()
            state = game.state()
            gameTick=0
            run = True
            while run:
                events = pygame.event.get()
                for event in events:
                    if event.type==pygame.QUIT:
                        run=False
                        epoch=epochs
                gameTick=gameTick%264
                ############## Sample Environement #########################
                if gameTick%6==0:
                    action = player.getAction(state=state, epoch=epoch,train=True)
                    # graphics.Graphics.game_screen(screen,game)
                    gameTick,nextState,reward=game.tick(gameTick,action)
                    buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                                nextState, torch.tensor(game.game_over!=False, dtype=torch.float32))
                else:
                    gameTick,midState,_=game.tick(gameTick,action)
                    # graphics.Graphics.game_screen(screen,game)
main()