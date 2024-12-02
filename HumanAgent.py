import pygame
import environment
import graphics
class agent:

    def getAction(self,events):
        for event in events:
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    return 0
                if event.key==pygame.K_DOWN:
                    return 1
                if event.key==pygame.K_LEFT:
                    return 2
                if event.key==pygame.K_UP:
                    return 3
        return None
