import pygame
import graphics
import environment
from HumanAgent import agent as HumanAgent
from DQN_Agent import DQN_Agent
pygame.init()
path = "Data/parameters1"
# player = HumanAgent()
player=DQN_Agent(path)
player.load_params(path)
player.save_param(path)
width , height = 540,710
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption('PAC MAN')
game = environment.Game()
graphics.Graphics.home_screen(screen)

def main ():
    run = True
    isGame = type(player) is not HumanAgent
    gameTickCounter=0
    
    while(run):
        events = pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.MOUSEBUTTONDOWN and graphics.Graphics.home_screen(screen).get_rect(topleft=(195,400)).collidepoint(event.pos):
                isGame=True
        
        if not isGame:
            continue

        action = player.getAction(events=events, state=game.state(), epoch=100000)
        graphics.Graphics.game_screen(screen,game)
        gameTickCounter,_,_ =game.tick(gameTickCounter,action)
        if gameTickCounter%60==0:
            print (gameTickCounter/60,game.ghostModes)
            
       
        pygame.display.update()
        clock.tick(60)
    print(game.state())
    
        

if __name__ == '__main__':
    main()