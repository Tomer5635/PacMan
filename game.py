import pygame
import graphics
import environment
import torch
import numpy as np
from HumanAgent import agent as HumanAgent
from DQN_Agent_CNN import DQN_Agent
pygame.init()
checkpoint_path = "Data/checkpoint0.pth"

human_agent = False #change to True in order to play

width , height = 540,710
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('PAC MAN')
game = environment.Game()
graphics.Graphics.home_screen(screen)

if human_agent:
    player = HumanAgent()
else:
    player=DQN_Agent(env=game)
    checkpoint = torch.load(checkpoint_path)
    player.DQN.load_state_dict(checkpoint['model_state_dict'])

def main ():
    run = True
    isGame = not human_agent
    gameTickCounter=0
    action=0
    while(run):
        events = pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN and graphics.Graphics.home_screen(screen).get_rect(topleft=(195,400)).collidepoint(event.pos):
                isGame=True
        
        
        
        if not isGame:
            pygame.display.update()
            continue

        action,_ = player.getAction(events=events, state_cnn=game.state_cnn(), epoch=100000,train=False,action=action)
        graphics.Graphics.game_screen(screen,game)
        gameTickCounter,_,_ =game.tick(gameTickCounter,action)
            
       
        pygame.display.update()
        clock.tick(60)
    
        

if __name__ == '__main__':
    main()