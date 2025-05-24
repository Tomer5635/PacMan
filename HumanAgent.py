import pygame
import environment
import graphics
class agent:

    def getAction(self,events, state_cnn=None, epoch=None,action=None,train=None):
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    return 0,None
                if event.key==pygame.K_DOWN:
                    return 1,None
                if event.key==pygame.K_LEFT:
                    return 2,None
                if event.key==pygame.K_UP:
                    return 3,None
        return action,None
