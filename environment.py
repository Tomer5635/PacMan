import numpy as np
import math
import random
import torch

class Game:
    ghostHomeTiles = [(1,26),(1,1),(29,26),(29,1)]
    board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
             [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1],
             [-1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 5,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 5,-1],
            [-1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1],
            [-1, 1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1,-1],
            [-1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 0,-1,-1, 0,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1,-1],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1,-1,-1,-1, 0,-1,-1, 0,-1,-1,-1,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1, 0, 0, 0, 0, 0,10, 0, 0, 0, 0,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1, 0,-1,-1,-1,-2,-2,-1,-1,-1, 0,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [-1,-1,-1,-1,-1,-1, 1,-1,-1, 0,-1, 0, 0, 0, 0, 0, 0,-1, 0,-1,-1, 1,-1,-1,-1,-1,-1,-1],
            [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,-1, 0, 7, 0, 8, 0, 9,-1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [-1,-1,-1,-1,-1,-1, 1,-1,-1, 0,-1, 0, 0, 0, 0, 0, 0,-1, 0,-1,-1, 1,-1,-1,-1,-1,-1,-1],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1, 0,-1,-1,-1,-1,-1,-1,-1,-1, 0,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [ 0, 0, 0, 0, 0,-1, 1,-1,-1, 0,-1,-1,-1,-1,-1,-1,-1,-1, 0,-1,-1, 1,-1, 0, 0, 0, 0, 0],
            [-1,-1,-1,-1,-1,-1, 1,-1,-1, 0,-1,-1,-1,-1,-1,-1,-1,-1, 0,-1,-1, 1,-1,-1,-1,-1,-1,-1],
            [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1],
            [-1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 1,-1,-1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1, 1,-1,-1,-1,-1, 1,-1],
            [-1, 5, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1, 1, 1,11, 1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 5,-1],
            [-1,-1,-1, 1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1, 1,-1,-1,-1],
            [-1,-1,-1, 1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1, 1,-1,-1,-1],
            [-1, 1, 1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1,-1,-1, 1, 1, 1, 1, 1, 1,-1],
            [-1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1],
            [-1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1,-1, 1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, 1,-1],
            [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,-1],
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]]
    board = np.array(board,dtype=int)
    direction = 0
    nextDirection = 0
    points = 0
    ghostModes = [1,1,1,1] #0=chase 1=scatter 2=frightened
    ghostDirections = [0,3,3,3]
    ghostUnder = np.array([0,0,-3,0],dtype=int)
    ghostTargetTiles = [(1,26),(1,1),(29,26),(29,1)]
    waveCounter=0
    waveTime=0
    frightenedTime=0
    game_over = False
    
    def move(self):
        prevPoints = self.points
        if 11 in self.board:
            i,j=np.argwhere(self.board == 11)[0]
        if self.board[i][j] ==11:
            if self.nextDirection==0:
                if self.board[i][(j+1)%28]>=0:
                    self.direction=0
            elif self.nextDirection==1:
                if self.board[i+1][j]>=0:
                    self.direction=1
            elif self.nextDirection==2:
                if self.board[i][j-1]>=0:
                    self.direction=2
            elif self.nextDirection==3:
                if self.board[i-1][j]>=0:
                    self.direction=3
            if self.direction==0:
                nextPos = (i,(j+1)%28)
            elif self.direction==1:
                nextPos = (i+1,j)
            elif self.direction==2:
                nextPos = (i,j-1)
            elif self.direction==3:
                nextPos = (i-1,j)
            if self.board[nextPos[0]][nextPos[1]]!=-1 and self.board[nextPos[0]][nextPos[1]]!=-2:
                if self.board[nextPos[0]][nextPos[1]]>6:
                    self.gameOver()
                    return self.state,0
                if self.board[nextPos[0]][nextPos[1]]<-6:
                    self.respawnGhost(self.board[nextPos[0]][nextPos[1]]+10,nextPos)
                        
                self.board[i][j] = 0
                if self.board[nextPos[0]][nextPos[1]]==1:
                    self.points+=10
                if self.board[nextPos[0]][nextPos[1]]==5:
                    self.points+=50
                    self.ghostModes=[2,2,2,2]
                    self.frightenedTime=0
                self.board[nextPos[0]][nextPos[1]]=11
                reward=self.points - prevPoints
                
                return self.state,reward
            
                
    def ghostModeUpdate(self):
        if self.waveCounter%2==0:
            mode=1
        else:
            mode=0
        if 2 not in self.ghostModes:
            self.waveTime+=1
            self.frightenedTime=0
            if self.waveCounter>6:
                self.waveTime=-999999
            elif self.waveCounter%2==1:
                if self.waveTime==20:
                    self.waveCounter+=1
                    self.waveTime=0
                    self.ghostModes=[1,1,1,1]
            else:
                if self.waveCounter>3:
                    if self.waveTime==5:
                        self.waveCounter+=1
                        self.waveTime=0
                        self.ghostModes=[0,0,0,0]
                else:
                    if self.waveTime==7:
                        self.waveCounter+=1
                        self.waveTime=0
                        self.ghostModes=[0,0,0,0]
        else:
            self.frightenedTime+=1
            if self.frightenedTime==7:
                self.frightenedTime=0
                for i in range(len(self.ghostModes)):
                    if self.ghostModes[i] ==2:
                        self.ghostModes[i]=mode
                        x,y=np.argwhere(self.board==i-10)[0]
                        self.board[x][y]=self.board[x][y]*-1
    
    def ghostMove(self,ghost):
        if ghost <4-int(self.points<300)-int(self.points<600):
            if 10-ghost not in self.board:
                self.ghostMove(ghost+1)
                return
            i,j=np.argwhere(self.board==10-ghost)[0]
            self.determineTargetTile(ghost)
            options = []
            if (self.board[i-1][j]>=0   or (self.board[i-1][j]==-2 and i==13) or self.board[i-1][j]==-10+ghost) and self.ghostDirections[ghost]!=1:
                options.insert(0,(i-1,j))
            if (self.board[i+1][j]>=0  or self.board[i+1][j]==ghost-10) and self.ghostDirections[ghost]!=3:
                options.insert(0,(i+1,j))
            if (self.board[i][(j-1)%28]>=0 or self.board[i][(j-1)%28]==ghost-10) and self.ghostDirections[ghost]!=0:
                options.insert(1,(i,(j-1)%28))
            if (self.board[i][(j+1)%28]>=0 or self.board[i][(j+1)%28]==ghost-10) and self.ghostDirections[ghost]!=2:
                options.insert(0,(i,(j+1)%28))
            if(len(options)==0):
                self.ghostMove(ghost+1)
                return False
            
            least = options[0]
            if len(options)>1:
                for index in range(len(options)):
                    if math.hypot(options[index][0]-self.ghostTargetTiles[ghost][0],options[index][1]-self.ghostTargetTiles[ghost][1])<=math.hypot(least[0]-self.ghostTargetTiles[ghost][0],least[1]-self.ghostTargetTiles[ghost][1]):
                        least=options[index]
            nextPos=least
            if j+1==nextPos[1]:
                dir=0
            elif j-1==nextPos[1]:
                    dir=2
            elif i-1==nextPos[0]:
                dir=3
            else:
                dir=1
            if self.board[nextPos[0]][nextPos[1]]==11:
                self.gameOver()
                return False
            self.ghostDirections[ghost]=dir
            self.board[i][j]=self.ghostUnder[ghost]
            self.ghostUnder[ghost]=self.board[nextPos[0]][nextPos[1]]
            if self.ghostModes[ghost]==2:
                self.board[nextPos[0]][nextPos[1]] = ghost-10
            else:
                self.board[nextPos[0]][nextPos[1]] = 10-ghost
            self.ghostMove(ghost+1)
            return True
    def blueGhostMove(self,ghost):
        if ghost <4-int(self.points<300)-int(self.points<600):
            if ghost-10 not in self.board:
                self.blueGhostMove(ghost+1)
                return True
            i,j=np.argwhere(self.board==ghost-10)[0]
            options = []
            if (self.board[i-1][j]>=0 or (self.board[i-1][j]==-2 and i==13) or self.board[i-1][j]==-10+ghost) and self.ghostDirections[ghost]!=1:
                options.insert(0,(i-1,j))
            if (self.board[i+1][j]>=0 or self.board[i+1][j]==ghost-10) and self.ghostDirections[ghost]!=3:
                options.insert(0,(i+1,j))
            if (self.board[i][j-1]>=0 or self.board[i][j-1]==ghost-10) and self.ghostDirections[ghost]!=0:
                options.insert(1,(i,(j-1)%28))
            if (self.board[i][(j+1)%28]>=0 or self.board[i][(j+1)%28]==ghost-10) and self.ghostDirections[ghost]!=2:
                options.insert(0,(i,(j+1)%28))
            if(len(options)==0):
                self.ghostDirections[ghost]=(self.ghostDirections[ghost]+2)%4
                self.blueGhostMove(ghost+1)
                return
            nextPos=options[random.randint(0,len(options)-1)]
                
            if j+1==nextPos[1]:
                dir=0
            elif j-1==nextPos[1]:
                    dir=2
            elif i-1==nextPos[0]:
                dir=3
            else:
                dir=1
            if self.board[nextPos[0]][nextPos[1]]==11:
                self.respawnGhost(ghost,(i,j))
                self.blueGhostMove(ghost+1)
                return
            self.ghostDirections[ghost]=dir
            self.board[i][j]=self.ghostUnder[ghost]
            self.ghostUnder[ghost]=self.board[nextPos[0]][nextPos[1]]
            self.board[nextPos[0]][nextPos[1]] = ghost-10
            self.blueGhostMove(ghost+1)
            return True
    def determineTargetTile(self,ghost):
        coords = np.argwhere(abs(self.board)==10-ghost)[0]
        if (coords[0] >=13 and coords[0]<=15) and coords[1]>10 and coords[1]<16:
            self.ghostTargetTiles[ghost]=(11,14)
            return
        if self.ghostModes[ghost] == 1:
            self.ghostTargetTiles[ghost]=self.ghostHomeTiles[ghost]
        elif self.ghostModes[ghost]==0:
            pacman=np.argwhere(self.board==11)[0]
            if ghost==0:
                self.ghostTargetTiles[0]= pacman
            if ghost==1:
                self.ghostTargetTiles[1]=pacman
                if self.direction == 0:
                    self.ghostTargetTiles[1]=(self.ghostTargetTiles[1][0],self.ghostTargetTiles[1][1]+4)
                if self.direction == 1:
                    self.ghostTargetTiles[1]=(self.ghostTargetTiles[1][0]+4,self.ghostTargetTiles[1][1])
                if self.direction == 2:
                    self.ghostTargetTiles[1]=(self.ghostTargetTiles[1][0],self.ghostTargetTiles[1][1]-4)
                if self.direction == 3:
                    self.ghostTargetTiles[1]=(self.ghostTargetTiles[1][0]-4,self.ghostTargetTiles[1][1])
            if ghost==2:
                if 10 in self.board or -10 in self.board:
                    blinky=np.argwhere(abs(self.board)==10)[0]
                else:
                    blinky=np.argwhere(abs(self.board)==10-np.argwhere(abs(self.ghostUnder)==10)[0])[0]
                halfway=pacman
                if self.direction == 0:
                    halfway=(halfway[0],halfway[1]+2)
                if self.direction == 1:
                    halfway=(halfway[0]+2,halfway[1])
                if self.direction == 2:
                    halfway=(halfway[0],halfway[1]-2)
                if self.direction == 3:
                    halfway=(halfway[0]-2,halfway[1])
                self.ghostTargetTiles[2]=(2*halfway[0]-blinky[0],2*halfway[1]-blinky[1])
            if ghost==3:
                clyde=np.argwhere(self.board==7)[0]
                if math.hypot(pacman[0]-clyde[0],pacman[1]-clyde[1])>8:
                    self.ghostTargetTiles[3]= pacman
                else:
                    self.ghostTargetTiles[3]=self.ghostHomeTiles[3]
    def respawnGhost(self,ghost,pos):
        self.board[13,14] = 10-ghost
        self.points+=200
        self.ghostDirections[ghost]=3
        if self.waveCounter%2==0:
            self.ghostModes[ghost]=1
        else:
            self.ghostModes[ghost]=0
        self.board[pos]=self.ghostUnder[ghost]
        self.ghostUnder[ghost]=0
    def gameOver(self):
        print("GAME OVER")
        self.game_over="lose"
    def win(self):
        self.game_over="win"
    def getLegalActions(self):
        return [0,1,2,3]
    def tick(self,GameTick,action):
        if not self.game_over:
            if 11 not in self.board:
                self.gameOver()
            if (1 not in self.board and 5 not in self.board) and (1 not in self.ghostUnder and 5 not in self.ghostUnder):
                self.win()
            if action is not None:
                self.nextDirection = action
            if GameTick%6==0:
                self.move()
            if GameTick%8==0:
                self.ghostMove(0)
            if GameTick%11==0:
                self.blueGhostMove(0)
            if GameTick%60==0:
                self.ghostModeUpdate()
            return GameTick+1
        return GameTick
    def state(self):
        board_np = self.board.reshape(868)
        p_dir = self.direction
        g_dir = self.ghostDirections.copy()
        g_dir.append(p_dir)
        directions = np.array(g_dir,dtype=np.float32)
        print(directions.shape)
        state=np.concatenate([board_np,directions])
        return torch.tensor(state,dtype=torch.float32)
        

    
                
                            
        
                       
    
                
                
                        
        
                
        
            
                    
        


