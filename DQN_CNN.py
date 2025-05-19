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

output_size = 4 # V(state)
gamma = 0.95 

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0
epsilon_decay = 100

class DQN (nn.Module):
    def __init__(self, input_channels: int = 3, row: int = 31, col: int= 28, device = torch.device('cpu')) -> None:
        super().__init__()
        if device is None:
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.device = device
        
        self.conv1 = nn.Conv2d(in_channels=input_channels, out_channels=8, kernel_size=3, padding=1)  
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1) 
        # self.conv3 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1) 
        self.MSELoss = nn.MSELoss()

        # Dynamically calculate flattened size
        with torch.no_grad():
            dummy = torch.zeros(1, input_channels, row, col)
            dummy = self.conv1(dummy)
            dummy = F.relu(dummy)
            dummy = self.conv2(dummy)
            dummy = F.relu(dummy)
            self.flattened_size = dummy.view(1, -1).shape[1]

        self.fc1 = nn.Linear(self.flattened_size, 64)
        self.output = nn.Linear(64, 1)
        self.to(self.device)
    
    def forward(self, x):
        x = F.relu(self.conv1(x))         # [B, 32, H, W]
        x = F.relu(self.conv2(x))         # [B, 64, H, W]
        # x = F.relu(self.conv3(x))         # [B, 64, H, W]
        x = x.view(x.size(0), -1)         # Flatten to [B, *]
        x = F.relu(self.fc1(x))           # [B, 128]
        return self.output(x)             # [B, 1]

    def loss (self, Q_value, rewards, Q_next_Values, Dones ):
        Q_new = rewards.to(device=self.device) + gamma * Q_next_Values * (1- Dones.to(device=self.device))
        return self.MSELoss(Q_value, Q_new)

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
