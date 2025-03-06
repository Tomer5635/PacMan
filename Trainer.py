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
    path = "Data/parameters2"
    bufferPath = "Data/buffer2"
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('PAC MAN')
    game = Game()

    best_score = 0

    ####### params ############
    player = DQN_Agent(path)
    # player.load_params(path)
    player.save_param(path)
    player_hat = DQN_Agent()
    player_hat.DQN = player.DQN.copy()
    batch_size = 500
    buffer = ReplayBuffer()
    learning_rate = 0.001
    epochs = 1000
    start_epoch = 0
    gamma=0.1
    C = 3
    loss = torch.tensor(-1,dtype=torch.float32,requires_grad=True)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000], gamma=gamma)
    step = 0
    wandb.init(
    # set the wandb project where this run will be logged
    project="pacman-project",
    config={
    "learning_rate": learning_rate,
    "architecture": "DQN",
    "dataset": "PACMAN",
    "epochs": epochs,
    "batch_size":batch_size,
    "gamma":gamma

    }
    )

    ######### checkpoint Load ############
    checkpoint_path = "Data/checkpoint1.pth"
    buffer_path = "Data/buffer1.pth"
    # if os.path.exists(checkpoint_path):
    #     checkpoint = torch.load(checkpoint_path)
    #     start_epoch = checkpoint['epoch']+1
    #     player.DQN.load_state_dict(checkpoint['model_state_dict'])
    #     player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
    #     optim.load_state_dict(checkpoint['optimizer_state_dict'])
    #     scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
    #     buffer = torch.load(buffer_path)
    #     losses = checkpoint['loss']
    #     scores = checkpoint['scores']
    #     avg_score = checkpoint['avg_score']
    # player.DQN.train()
    # player_hat.DQN.eval()

    #################################

    for epoch in range(start_epoch, epochs):
        game = Game()
        state = game.state()
        gameTick=0
        run = True
        steps=0
        while run:
            events = pygame.event.get()
            for event in events:
                if event.type==pygame.QUIT:
                    run=False
            gameTick=gameTick%264
            ############## Sample Environement #########################
            if gameTick%6==0:
                step+=1
                action = player.getAction(state=state, epoch=epoch,train=False)
                graphics.Graphics.game_screen(screen,game)
                gameTick,nextState,reward=game.tick(gameTick,action)
                buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                            nextState, torch.tensor(game.game_over!=False, dtype=torch.float32))
            else:
                gameTick,midState,_=game.tick(gameTick,action)
                graphics.Graphics.game_screen(screen,game)

            if game.game_over:
                best_score = max(best_score, game.points)
                buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), midState, torch.tensor(game.game_over!=False, dtype=torch.float32))
                graphics.Graphics.game_screen(screen,game)
                pygame.display.update()
                break
            state = nextState

            pygame.display.update()
            clock.tick(1000)
            
            if len(buffer) < 100:
                continue
    
            ############## Train ################
            if gameTick%6==0:
                states, actions, rewards, next_states, dones = buffer.sample(batch_size)
                Q_values = player.getActionValues(states)
                Q_hat_Values = player_hat.getActionValues(next_states).detach()
                loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)

                loss.backward()
                optim.step()
                optim.zero_grad()
                scheduler.step()
                wandb.log({ "loss": loss})
                print (f"epoch: {epoch},step:{step}, score: {game.points}, best score: {best_score}, loss: {loss}, reward:{reward}", end="\r")
                
        if epoch % C == 0:
            player_hat.DQN.load_state_dict(player.DQN.state_dict())
            player.save_param(path)
        
        
       
        #########################################

        
        torch.save(buffer,bufferPath)
        

        print (f'epoch: {epoch} loss: {loss:.7f} LR: {scheduler.get_last_lr()} step: {step} ' \
               f'score: {game.points} best_score: {best_score}')
        step = 0
        scores.append(game.points)
        losses.append(loss.item())

        avg = (avg * (epoch % 10) + game.points) / (epoch % 10 + 1)
        if (epoch + 1) % 10 == 0:
            avg_score.append(avg)
            print (f'average score last 10 games: {avg} ')
            avg = 0

        wnblog = {
                        'epoch': epoch,
                        'loss': losses,
                        'score':game.points
            }
        wandb.log(wnblog)
        if epoch % 5 == 0 and epoch > 0:
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': player.DQN.state_dict(),
                'optimizer_state_dict': optim.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'loss': losses,
                'scores':scores,
                'avg_score': avg_score
            }
            
            torch.save(checkpoint, checkpoint_path)
            torch.save(buffer, buffer_path)
           
        

        


        
if __name__ == "__main__":
    main ()