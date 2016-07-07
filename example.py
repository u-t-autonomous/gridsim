import pygame
from random import random
from bisect import bisect
from environment import Simulation


def main():

    sim = Simulation("config.txt", "matrix.txt")

    done = False
    while not done:

        sim.move_agent(0, "east")
        sim.move_agent(1, "south")
        
        agent1 = sim.get_state()["agents"][0]
        print "agent1: {}".format(agent1)

        obstacle1 = sim.get_state()["moving_obstacles"][0]
        print "obstacle1: {}".format(obstacle1)

        done = sim.update()

    for line in sim.get_log()["agents"][0]:
        print line
        

main()
    
