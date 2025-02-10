import math
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import copy
import environment


# Parameters

input_size = 873 # state: board = 28 * 31 = 868 + direction = 1 = 869 + 4 GhostDirections
layer1 = 1200
layer2 = 800
layer3 = 400
layer4 = 100
output_size = 4 # V(state)
gamma = 0.99 

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsilon_decay = 100000

MSELoss = nn.MSELoss()

class DQN (nn.Module):
    def __init__(self) -> None:
        super().__init__()
        if torch.cuda.is_available:
            self.device = torch.device('cpu') # 'cuda'
        else:
            self.device = torch.device('cpu')
        
        self.linear1 = nn.Linear(input_size, layer1, device=self.device)
        self.linear2 = nn.Linear(layer1, layer2, device=self.device)
        self.linear3 = nn.Linear(layer2, layer3, device=self.device)
        self.linear4 = nn.Linear(layer3, layer4, device=self.device)
        self.output = nn.Linear(layer4, output_size, device=self.device)
        
    def forward (self, x):
        x = self.linear1(x)
        x = F.leaky_relu(x)
        x = self.linear2(x)
        x = F.leaky_relu(x)
        x = self.linear3(x)
        x = F.leaky_relu(x)
        x = self.linear4(x)
        x = F.relu(x)
        x = self.output(x)
        return x
    

    def loss (self, Q_value, rewards, Q_next_Values, Dones ):
        Q_new = rewards + gamma * Q_next_Values.detach() * (1- Dones)
        return MSELoss(Q_value, Q_new)

    def epsilon_greedy(self, epoch, start = epsilon_start, final=epsilon_final, decay=epsilon_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    def save_params(self, path):
        torch.save(self.state_dict(), path)

    def copy (self):
        return copy.deepcopy(self)
    
    def __call__ (self,state):
        return self.forward(state)
