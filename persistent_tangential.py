from re import A
from turtle import distance
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.animation import FuncAnimation
import random
import numpy as np
from random import randint



fig = plt.figure(figsize=(12,12))
ax = plt.axes()

#function to calculate euclidean distance
def dist(start,end):
    return np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2)

#defining a drone object. it will have a goal which it will continuously seek
#each drone will also have its delta derived from its own goal
#each drone will also have a starting point : tuple
class Drone():
    def __init__(self, start, goal, roundabouts = []):
        self.goal = goal
        self.start = start
        self.currentx=[start[0]]
        self.currenty=[start[1]]
        self.roundabouts = []
        self.current = start
        
    
    def update_goal(self):
        current = (self.currentx[-1],self.currenty[-1])
        #print(current)

        theta = np.arctan2((self.goal.coords[1]-current[1]),(self.goal.coords[0]-current[0]))
        d = np.round(dist(current,self.goal.coords),3)
        #print(d)

        if d < self.goal.radius:
            return (0,0)

        #elif self.goal.radius < d < self.goal.radius + self.goal.influence:

            #return (self.goal.strength*(d-self.goal.radius)*np.cos(theta),self.goal.strength*(d-self.goal.radius)*np.sin(theta))

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
    
    def coords(self):
        return (self.currentx[-1],self.currenty[-1])

def update_roundabout(drones):
    for i in range(len(drones)):
        drone = drones[i]
        drone.roundabouts=[]
        for j in range(len(drones)):
            if j!=i:
                compare = drones[j]
                if dist(drone.coords(),compare.coords()) < 1:

                    roundabout = Goal(((drone.coords()[0]+compare.coords()[0])/2,(drone.coords()[1]+compare.coords()[1])/2),0.1,0.3,1)
                    drone.roundabouts.append(roundabout)

                if dist(drone.coords(),compare.coords())<0.4:
                    print("collision at",drone.coords())

                

class Goal(): #the goal class to define goals
    def __init__(self,coords,strength,radius,influence):
        self.coords = coords
        self.strength=strength
        self.radius=radius
        self.influence = influence
        self.name = "doesn't matter"

        


goals = [Goal((0,10),0.01,0.3,4),Goal((10,0),0.02,0.3,2), Goal((10,10),0.01,0.3,4),Goal((10,5),0.02,0.3,4),Goal((0,5),0.01,0.3,4)]
#goals = [Goal((0,10),0.01,0.3,4),Goal((10,0),0.02,0.3,2)]



drones = [Drone((9,0),goals[0]),Drone((0,9),goals[1]),Drone((0,0),goals[2]),Drone((-1,5),goals[3]),Drone((11,5),goals[4])]
#drones = [Drone((9,0),goals[0]),Drone((0,9),goals[1])]



def drone_generator(n):#generates n drones(starting inrandom positions and n goals(in random positions))
    drones = []
    goals = []

    for i in range(n):
        goals.append(Goal((randint(-10,10),randint(-10,10)),0.1,0.3,1))
        drones.append(Drone((randint(-10,10),randint(-10,10)),goals[i]))
        
    return goals, drones


#goals, drones = drone_generator(55)



def anim_func(i):
    plt.xlim(-1,11)
    plt.ylim(-1,11)

    

    for goal in goals:
        ax.add_patch(plt.Circle(goal.coords,goal.radius, fc='blue'))
    
    



    update_roundabout(drones)

    clist = ['red','green','blue','yellow','pink']
    for i in range(len(drones)):
        drone = drones[i]
        drone.update_delta(drone.roundabouts)
    
        plt.scatter(drone.currentx,drone.currenty, c=clist[i])
        #ax.add_patch(plt.Circle((drone.currentx[-1],drone.currenty[-1]), 0.5, fill=False))
        #print(drone.currentx)

    



animation = FuncAnimation(fig, anim_func, interval=85)

plt.show()

print("finished")