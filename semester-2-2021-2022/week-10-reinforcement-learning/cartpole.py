import gym
import os
import torch
from torch import nn,optim
from torch.functional import F
import random
import copy
import gym
import numpy as np
#from google.colab import drive
#from google.colab import files
from torch.utils.data import Dataset, DataLoader
from torch.optim.lr_scheduler import ExponentialLR
from torch.autograd import Variable
import pickle
#drive.mount('/content/gdrive')
env = gym.make('CartPole-v1')

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


FloatTensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

class Network(nn.Module):
    def __init__(self,action_size,state_size):
        super(Network, self).__init__()
        self.hidden=nn.Linear(state_size,64)
        self.hidden2=nn.Linear(64,128)
        self.out=nn.Linear(128,action_size)

    def forward(self, x):
        x=x.to(device)
        x=F.relu(self.hidden(x))
        x=F.relu(self.hidden2(x))
        x=self.out(x)
        return x



class DQN():
    def __init__(self,gamma,action_shape,state_shape):
        self.memory=[]
        self.model=Network(action_shape,state_shape).to(device)
        self.target_model=copy.deepcopy(self.model)
        self.gamma=gamma
        self.done_mem=[]
        self.change=0
        self.num_action=action_shape
        self.optimizer=optim.Adam(self.model.parameters(),lr=0.00025)
        self.scheduler = ExponentialLR(self.optimizer, gamma=0.99)
    def reload(self,location):
      state_dict = torch.load(location)
      self.model.load_state_dict(state_dict)
      input=open("memory.dat",'rb')
      self.memory=pickle.load(input)
      self.target_model=copy.deepcopy(self.model)
    def save(self):
      torch.save(self.target_model.state_dict(), 'checkpoint_.pth')
      out= open("memory.dat",'wb')
      pickle.dump(self.memory,out)
      out.close()
    def exploit(self,state):
        with torch.no_grad():
            return torch.argmax(self.predict(self.target_model,state))
    def add_done(self,episode):
      self.done_mem.append(episode)
    def add_episode(self,episode):
        if len(self.memory)>50000:
            self.memory.pop(random.randrange(len(self.memory)))
        self.memory.append(episode)
    def predict(self,model,state):
        return model(torch.from_numpy(state).float())
    def act(self,state,epsilon,env):
        p=random.uniform(0,1)
        if p<epsilon:
            return env.action_space.sample()
        else:
            with torch.no_grad():
                return torch.argmax(self.predict(self.model,state))
    def train(self,batch_size):
        
        self.optimizer.zero_grad()
        transitions = random.sample(self.memory,batch_size)
        batch_state,batch_action,batch_reward,batch_next_state = zip(*transitions)
        batch_state,batch_action,batch_reward,batch_next_state=Variable(torch.cat(batch_state)), Variable(torch.cat(batch_action)), Variable(torch.cat(batch_reward)),Variable(torch.cat(batch_next_state))
        prediction=self.model(batch_state).gather(1, batch_action.type(torch.int64).unsqueeze(1)).squeeze(1)
        with torch.no_grad():
            max_q=self.target_model(batch_next_state).detach().max(1)[0]
            label=batch_reward+self.gamma*max_q
        loss=nn.SmoothL1Loss()(prediction,label)
        loss.backward()
        self.optimizer.step()
        self.target_model=copy.deepcopy(self.model)
        self.train_done(batch_size)
    def train_done(self,batch_size):
        self.optimizer.zero_grad()
        transitions = random.sample(self.done_mem,batch_size)
        batch_state, batch_action,batch_reward= zip(*transitions)
        batch_state, batch_action,batch_reward=Variable(torch.cat(batch_state)), Variable(torch.cat(batch_action)), Variable(torch.cat(batch_reward))
        prediction=self.model(batch_state).gather(1, batch_action.type(torch.int64).unsqueeze(1)).squeeze(1)
        loss=nn.SmoothL1Loss()(prediction,batch_reward)
        loss.backward()
        self.optimizer.step()
    def change_target(self):
        self.target_model=copy.deepcopy(self.model)
        self.change+=1
        #if self.change%100==0:
            #self.scheduler.step()



    


agent=DQN(0.8,env.action_space.n,env.observation_space.shape[0])
agent.reload('final_model.pth')

    
for i in range(100):
    total_training_rewards = 0
    observation = env.reset()
    done = False
    while not done:
        env.render()
        action=agent.exploit(observation)
        new_observation, reward, done, info = env.step(int(action))
        observation = new_observation
        total_training_rewards+=reward
    print(total_training_rewards)