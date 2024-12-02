import pygame
import environment
class Graphics:
    
    
    
    def home_screen(screen):
        width , height = 540,710
        menu_background = pygame.Surface((width,height))
        menu_background.fill("cornflowerblue")
        image = pygame.image.load('textures/logo.png')
        header = pygame.transform.scale(image,(340,340*(image.get_height()/image.get_width())))
        image = pygame.image.load('textures/pacmanR.gif')
        pacman = pygame.transform.scale(image,(150,150))
        image = pygame.image.load('textures/Play-Button.png')
        play = pygame.transform.scale(image,(150,150*(image.get_height()/image.get_width())))
        screen.blit(menu_background,(0,0))
        screen.blit(header,(100,10))
        screen.blit(pacman,(195,header.get_height()+50))
        screen.blit(play,(195, pacman.get_offset()[0]+pacman.get_height()+250))
        return play
    def game_screen(screen,game):
        if game.direction==0:
            pac = 'textures/pacmanR.gif'
        if game.direction==1:
            pac = 'textures/pacmanD.gif'
        if game.direction==2:
            pac = 'textures/pacmanL.gif'
        if game.direction==3:
            pac = 'textures/pacmanU.gif'
        width , height = 540,710
        game_background = pygame.Surface((width,height))
        game_background.fill("gray9")
        wall =pygame.Surface((19,19))
        wall.fill("cornflowerblue")
        dot = pygame.Surface((5,5))
        dot.fill("white")
        superdot = pygame.Surface((15,15))
        superdot.fill("gray9")
        pygame.draw.circle(superdot,color="white",radius=7,center=(8,8))
        pacman = pygame.transform.scale(pygame.image.load(pac),(19,19))
        gate = pygame.Surface((19,19))
        gate.fill("pink")
        ghosts = [pygame.transform.scale(pygame.image.load('textures/red-ghost.png'),(19,19)),pygame.transform.scale(pygame.image.load('textures/pink-ghost.png'),(19,19)),pygame.transform.scale(pygame.image.load('textures/blue-ghost.png'),(19,19)),pygame.transform.scale(pygame.image.load('textures/orange-ghost.png'),(19,19))]
        frightened=pygame.transform.scale(pygame.image.load('textures/fright-ghost.png'),(19,19))
            
                
        screen.blit(game_background,(0,0))
        
        score=pygame.transform.scale(pygame.font.Font('textures/PIXELITE.FON').render("Score:"+str(game.points),True,"white"),(300,50))
        screen.blit(score,(10,10))
        for i in range(len(game.board)):
            for j in range(len(game.board[i])):
                match game.board[i][j]:
                    case -1:
                        screen.blit(wall,(4+j*19,100+i*19))
                    case 1:
                        screen.blit(dot,(11+j*19,107+i*19))
                    case 11:
                        screen.blit(pacman,(4+j*19,100+i*19))
                    case 10:
                        screen.blit(ghosts[0],(4+j*19,100+i*19))
                    case 7:
                        screen.blit(ghosts[3],(4+j*19,100+i*19))
                    case 9:
                        screen.blit(ghosts[1],(4+j*19,100+i*19))
                    case 8:
                        screen.blit(ghosts[2],(4+j*19,100+i*19))
                    case -10:
                        screen.blit(frightened,(4+j*19,100+i*19))
                    case -7:
                        screen.blit(frightened,(4+j*19,100+i*19))
                    case -9:
                        screen.blit(frightened,(4+j*19,100+i*19))
                    case -8:
                        screen.blit(frightened,(4+j*19,100+i*19))
                    case 5:
                        screen.blit(superdot,(6+j*19,102+i*19))
                    case -2:
                        screen.blit(gate,(4+j*19,100+i*19))
        if game.game_over=="win":
            screen.blit(pygame.transform.scale(pygame.font.Font('textures/PIXELITE.FON').render("YOU WIN",True,"LIME"),(19*6,17)),(209,17*19+100))
        if game.game_over=="lose":
            screen.blit(pygame.transform.scale(pygame.font.Font('textures/PIXELITE.FON').render("GAME OVER",True,"red"),(19*6,17)),(209,17*19+100))
                    
                
            
                