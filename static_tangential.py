from re import A
from turtle import distance
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import random
import numpy as np



fig = plt.figure(figsize=(12,12))
ax = plt.axes()

#function to calculate euclidean distance
def dist(start,end):
    return np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)

#defining a drone object. it will have a goal which it will continuously seek
#each drone will also have its delta derived from its own goal
#each drone will also have a starting point : tuple
class Drone():
    def __init__(self, start, goal):
        self.goal = goal
        self.start = start
        self.currentx=[start[0]]
        self.currenty=[start[1]]
    
        
    
    def update_goal(self):
        current = (self.currentx[-1],self.currenty[-1])
        #print(current)

        theta = np.arctan2((self.goal.coords[1]-current[1]),(self.goal.coords[0]-current[0]))
        d = dist(current,self.goal.coords)
        #print(d)

        if d < self.goal.radius:
            return (0,0)

        elif self.goal.radius < d < self.goal.radius + self.goal.influence:

            return (self.goal.strength*(d-self.goal.radius)*np.cos(theta),self.goal.strength*(d-self.goal.radius)*np.sin(theta))

        else:
            return (self.goal.strength*self.goal.influence*np.cos(theta),self.goal.strength*self.goal.influence*np.sin(theta))
    
    def update_avoid(self, roundabout):
        current = (self.currentx[-1],self.currenty[-1])
        #print(current)

        theta = np.arctan2((roundabout.coords[1]-current[1]),(roundabout.coords[0]-current[0])) - np.pi/2
        #theta = np.arctan2((roundabout.coords[1]-current[1]),(roundabout.coords[0]-current[0]))
        d = dist(current,roundabout.coords)

        if d < roundabout.radius:
            return(-np.sign(np.cos(theta))*np.inf,-np.sign(np.sin(theta))*np.inf)
        elif roundabout.radius <= d <= roundabout.radius + roundabout.influence:
            return (-roundabout.strength*(roundabout.influence+roundabout.radius-d)*np.cos(theta),-roundabout.strength*(roundabout.influence+roundabout.radius-d)*np.sin(theta))

        else:
            return (0,0)


    
    def update_delta(self, roundabouts):
        delr = (0,0)
        for roundabout in roundabouts:
            delrr = self.update_avoid(roundabout)
            delr = (delr[0]+delrr[0] , delr[1]+delrr[1])

        delg = self.update_goal()

        current = (self.currentx[-1],self.currenty[-1])

        self.currentx.append(current[0] + delr[0] + delg[0])
        self.currenty.append(current[1] + delr[1] + delg[1])
        

    
    
        
class Goal(): #the goal class to define goals
    def __init__(self,coords,strength,radius,influence):
        self.coords = coords
        self.strength=strength
        self.radius=radius
        self.influence = influence

        


goals = [Goal((10,10),0.01,0.3,4),Goal((7,10),0.02,0.3,2)]

roundabouts = [Goal((5,5),0.5,0.3,1),Goal((5.5,5.5),0.5,0.3,1)]

drones = [Drone((1,2),goals[0]),Drone((3,1),goals[1])]



def anim_func(i):
    plt.xlim(-1,11)
    plt.ylim(-1,11)

    

    for goal in goals:
        ax.add_patch(plt.Circle(goal.coords,goal.radius, fc='blue'))
    
    for roundabout in roundabouts:
        ax.add_patch(plt.Circle(roundabout.coords, roundabout.radius, fc='red'))

    for drone in drones:
        drone.update_delta(roundabouts)

    clist = ['red','green','blue','yellow','pink']
    for i in range(len(drones)):
        drone = drones[i]
        plt.scatter(drone.currentx,drone.currenty,c=clist[i])
        ax.add_patch(plt.Circle((drone.currentx[-1],drone.currenty[-1]), 0.45, fill=False))
        #print(drone.currentx)

    



animation = FuncAnimation(fig, anim_func, interval=100)

plt.show()

    