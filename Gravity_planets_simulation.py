# importing libraries
import pygame
import numpy as np
from Gravity_assets import *
import os

directory = "Images"
if not os.path.exists(directory):
    os.makedirs(directory)

# set up screen size
screen_size = width, height = (1024, 720)
# background colour
background_colour = (0, 0, 0) # black

# setup screen
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Gravity Simulation")

env = Environment(screen, width, height, background_colour)
env.addPlanets(50)

screen.fill(env.colour)
running = True
file_num = 0
while running:
    screen.fill(env.colour)
    env.showPlanets()
    env.resultant_forces()
    env.update()
    fname = directory + "/Gravitation_{0:04}.png".format(file_num)
    pygame.image.save(screen, fname)
    file_num += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # event.type will be QUIT when close button is pressed
            running = False
    pygame.display.update()

pygame.quit()