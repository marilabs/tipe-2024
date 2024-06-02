import pygame
import os
import signal
import sys
import pickle
from game import Game
import math
import matplotlib.pyplot as plt
import numpy as np
import config as c
from neural_network import NeuralNetwork

max_fitness = []
min_fitness = []
avg_fitness = []
max_apple_eaten = []
min_apple_eaten = []
avg_apple_eaten = []
max_snake_length = 0

def restore_curves(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

(max_fitness, min_fitness, avg_fitness, max_apple_eaten, min_apple_eaten, avg_apple_eaten, max_snake_length) = restore_curves(c.CURVES_FILES)

"""
# Set the y-axis limits from 0 to max_fitness_value
plt.plot(range(len(max_fitness)), max_fitness, color='blue', label='Max Fitness')
plt.plot(range(len(max_fitness)), avg_fitness, color='green', label='Average Fitness')
plt.plot(range(len(max_fitness)), max_apple_eaten, color='red', label='Max Apples Eaten')

plt.xlabel('Iteration')
plt.ylabel('Fitness')
plt.ylim(0, max(np.max(max_fitness), np.max(avg_fitness), np.max(max_apple_eaten)))
plt.title('Fitness vs Iteration')
plt.grid(True)
plt.legend()
plt.show()
"""

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('Itération')
ax1.set_ylabel('Fitness max', color=color)
#x_new = np.linspace(0, len(max_fitness), 300)
#spl = make_interp_spline(range(len(max_fitness)), max_fitness, k=3)
#max_fitness_smooth = spl(x_new)
#ax1.plot(x_new, max_fitness_smooth, color=color)
ax1.set_yscale('log')
ax1.plot(range(len(max_fitness)), max_fitness, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Fitness moyenne', color=color)
ax2.set_yscale('log')
ax2.plot(range(len(avg_fitness)), avg_fitness, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Fitness moyenne/maximum fct itération')
plt.grid(True)
plt.show()


fig, ax1 = plt.subplots()

color1 = 'tab:blue'
ax1.set_xlabel('Itération')
ax1.set_ylabel('Fitness maximum', color=color1)
ax1.plot(range(len(max_fitness)), max_fitness, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

color2 = 'tab:red'
ax2 = ax1.twinx()
ax2.set_ylabel('Fitness moyenne', color=color2)
ax2.plot(range(len(avg_fitness)), avg_fitness, color=color2)
ax2.tick_params(axis='y', labelcolor=color2)

color3 = 'tab:green'
ax1.plot(range(len(max_apple_eaten)), max_apple_eaten, color=color3, linestyle='dashed', label='Pommes manées maximum')

fig.tight_layout()
plt.title('Fitness vs Iteration')
plt.grid(True)
plt.show()
