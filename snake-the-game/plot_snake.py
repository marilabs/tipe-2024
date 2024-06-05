import pickle
import matplotlib.pyplot as plt
import config as c

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

(max_fitness, min_fitness, avg_fitness, max_apple_eaten, min_apple_eaten, avg_apple_eaten, max_snake_length) = restore_curves("curve.pickle")

fig, ax1 = plt.subplots()

color1 = 'tab:blue'
ax1.set_xlabel('Itération')
ax1.set_ylabel('Fitness maximum', color=color1)
ax1.set_yscale('log')
ax1.plot(range(len(max_fitness)), max_fitness, color=color1)
ax1.tick_params(axis='y', labelcolor=color1)

color3 = 'tab:green'
ax2 = ax1.twinx()
ax2.set_ylabel('Pommes mangées maximum', color=color3)
ax2.plot(range(len(max_apple_eaten)), max_apple_eaten, color=color3)
ax2.tick_params(axis='y', labelcolor=color3)

plt.title('Fitness vs Iteration')
# Add Vertical Gridlines (The Key Change)
ax1.grid(axis='x', linestyle='--')  # Gridlines on the x-axis (iterations)
ax2.grid(axis='y', linestyle='--')  # You need to add it for the second axis too
fig.tight_layout()
plt.savefig("curve.svg")
plt.savefig("curve.eps")
plt.savefig("curve.pdf")
plt.show()