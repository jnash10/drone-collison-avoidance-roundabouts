import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from objects import *
from functions import *



fig = plt.figure(figsize=(12,12))
ax = plt.axes()



goals = [Goal((10,10)),Goal((0,10)), Goal((0,5))]


drones = [Drone((0,0),goals[0]),Drone((10,0),goals[1]),Drone((10,1),goals[2]),Drone((5,0),goals[2])]


 

plt.xlim(-1,11)
plt.ylim(-1,11)
def anim_func(i):
    for drone in drones:


        plt.scatter(drone.currentx,drone.currenty, c = colours[drones.index(drone)],s=5)
        #check for exiting roundabout
        drone.check_exit()
        #chek for new roundabout
        drone.check_roundabout(drones)
        #now update to position
        drone.update_pos()
        #printing the roundabouts formed
        if drone.roundabout:
            print("yes")
            ax.add_patch(plt.Circle((drone.roundabout.coords),radius=drone.roundabout.radius,fill=False))
            plt.scatter(drone.roundabout.coords[0],drone.roundabout.coords[1],s=5,c='black')
        else:
            print("no")

animation = FuncAnimation(fig, anim_func, interval = 100)

plt.show()