import pygame
import torch
from environment import Game
from DQN_Agent import DQN_Agent
import graphics
import os
WIDTH , HEIGHT = 540,710
def main ():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Space')
        # clock = pygame.time.Clock()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption('PAC MAN')
    game = Game()
    graphics.Graphics.home_screen(screen)

    best_score = 0

    ####### params ############
    player = DQN_Agent()
    player_hat = DQN_Agent()
    player_hat.DQN = player.DQN.copy()
    batch_size = 50
    # buffer = ReplayBuffer(path=None)
    learning_rate = 0.00001
    ephocs = 200000
    start_epoch = 0
    C = 3
    loss = torch.tensor(-1)
    avg = 0
    scores, losses, avg_score = [], [], []
    optim = torch.optim.Adam(player.DQN.parameters(), lr=learning_rate)
    # scheduler = torch.optim.lr_scheduler.StepLR(optim,100000, gamma=0.50)
    scheduler = torch.optim.lr_scheduler.MultiStepLR(optim,[5000*1000, 10000*1000, 15000*1000], gamma=0.5)
    step = 0

    ######### checkpoint Load ############
    checkpoint_path = "Data/checkpoint20.pth"
    buffer_path = "Data/buffer20.pth"
    if os.path.exists(checkpoint_path):
        checkpoint = torch.load(checkpoint_path)
        start_epoch = checkpoint['epoch']+1
        player.DQN.load_state_dict(checkpoint['model_state_dict'])
        player_hat.DQN.load_state_dict(checkpoint['model_state_dict'])
        optim.load_state_dict(checkpoint['optimizer_state_dict'])
        scheduler.load_state_dict(checkpoint['scheduler_state_dict'])
        buffer = torch.load(buffer_path)
        losses = checkpoint['loss']
        scores = checkpoint['scores']
        avg_score = checkpoint['avg_score']
    player.DQN.train()
    player_hat.DQN.eval()

    #################################

    for epoch in range(start_epoch, ephocs):
        game = Game()
        end_of_game = False
        state = game.state()
        while not end_of_game:
            print (step, end='\r')
            step += 1
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return
            
            ############## Sample Environement #########################
            action = player.getAction(state=state, epoch=epoch)
            reward, done = game.move(action=action)
            next_state = game.state()
            buffer.push(state, torch.tensor(action, dtype=torch.int64), torch.tensor(reward, dtype=torch.float32), 
                        next_state, torch.tensor(done, dtype=torch.float32))
            if done:
                best_score = max(best_score, game.points)
                break

            state = next_state

            pygame.display.update()
            clock.tick(60)
            
            # if len(buffer) < MIN_BUFFER:
            #     continue
    
            ############## Train ################
            states, actions, rewards, next_states, dones = buffer.sample(batch_size)
            Q_values = player.Q(states, actions)
            Q_hat_Values = player_hat.getActionValues(next_states)

            loss = player.DQN.loss(Q_values, rewards, Q_hat_Values, dones)
            loss.backward()
            optim.step()
            optim.zero_grad()
            scheduler.step()

        if epoch % C == 0:
            player_hat.DQN.load_state_dict(player.DQN.state_dict())

        #########################################
        print (f'epoch: {epoch} loss: {loss:.7f} LR: {scheduler.get_last_lr()} step: {step} ' \
               f'score: {game.points} best_score: {best_score}')
        step = 0
        if epoch % 10 == 0:
            scores.append(game.points)
            losses.append(loss.item())

        avg = (avg * (epoch % 10) + game.points) / (epoch % 10 + 1)
        if (epoch + 1) % 10 == 0:
            avg_score.append(avg)
            print (f'average score last 10 games: {avg} ')
            avg = 0

        if epoch % 1000 == 0 and epoch > 0:
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