import os
import pickle
from game import Game
import config as c
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation

def restore_brain(brain_number: int) -> Game:
    # restore brain from file and inject it into the snake
    with open("brains_53.pickle", 'rb') as f:
        game_brains = pickle.load(f)
        brain = game_brains[brain_number]
        if c.DEBUG:
            print(game.brain, end=' ')
            print()
    return brain

def visualize_neural_network(brain):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
    fig.suptitle("Visualisation réseau de neurones", fontsize=16)
    for i in range(3):
        visualize_matrix(brain.weights[i], f"Poids synaptiques - Couche {i+1}", axes[0, i])
        visualize_matrix(brain.biases[i], f"Biais - Couche {i+1}", axes[1, i])
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig("brain_matrix.svg")
    plt.savefig("brain_matrix.eps")
    plt.savefig("brain_matrix.pdf")
    plt.savefig("brain_matrix.png")
    plt.show()

def visualize_matrix(matrix, title, ax=None):
    if ax is None:
        ax = plt.gca() # Get the current axes if not provided
    im = ax.imshow(matrix, cmap='viridis', interpolation='nearest')
    plt.colorbar(im, ax=ax, label='Valeur du poids synaptique')
    ax.set_xlabel('Index du neurone en entrée')
    ax.set_ylabel('Index du neurone en sortie')
    ax.set_title(title)
    # Setting tick parameters
    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_yticks(range(matrix.shape[0]))

def visualize_neural_network2(brain, fig, axes):
    fig.suptitle("Visualisation réseau de neurones", fontsize=16)
    for i in range(3):
        visualize_matrix(brain.weights[i], f"Poids synaptiques - Couche {i+1}", axes[0, i])
        visualize_matrix(brain.biases[i], f"Biais - Couche {i+1}", axes[1, i])

def update_visualization(i):
    brain = restore_brain(i)
    visualize_neural_network2(brain, fig, axes)

brain = restore_brain(c.SINGLE_SNAKE_BRAIN)
# brain has layers_sizes = [] weights = [] biases = []

for i, (w, b) in enumerate(zip(brain.weights, brain.biases)):
    print(f"Layer {i+1}:")
    print(f"  Weights: {w.shape}")
    print(f"  Biases: {b.shape}")

visualize_neural_network(brain)

# do an animation of the brain matrices

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
fig.suptitle("Visualisation réseau de neurones", fontsize=16)

ims = []  # List to store the animation frames (heatmaps)
for i in range(256):
    brain = restore_brain(i)
    frames = []  
    for j in range(3):
        frame1 = axes[0, j].imshow(brain.weights[j], cmap='viridis', interpolation='nearest', animated=True)
        frame2 = axes[1, j].imshow(brain.biases[j], cmap='viridis', interpolation='nearest', animated=True)
        frames.extend([frame1, frame2])
    ims.append(frames)  # Add frames for the current brain to the list

ani = animation.ArtistAnimation(fig, ims, interval=500, blit=True, repeat_delay=1000)
plt.show()