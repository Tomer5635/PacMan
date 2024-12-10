import environment
from DQN import DQN
import random
import torch
path = "Data/parameters1"
class DQN_Agent:
    def __init__(self,parameters_path =None,train =False,env =None):
        self.parameters_path=parameters_path
        self.train=train
        self.env=env
        self.DQN : DQN = DQN()

    def setTrainMode (self):
          if self.train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def getAction(self, state, epoch = 0, events= None, train =False): 
        actions = [0,1,2,3]
        if train:
            epsilon = self.DQN.epsilon_greedy(epoch)
            rnd = random.random()
            if rnd < epsilon:
                return random.choice(actions)
        with torch.no_grad():
            Q_values = self.DQN(state)
        max_index = torch.argmax(Q_values)
        return actions[max_index]
        # return random.choice(actions)
    
    def getActionValues(self,state):
        with torch.no_grad():
            Q_values = self.DQN(state)
        return Q_values

    
    def loadModel (self, file):
        self.model = torch.load(file)
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)
