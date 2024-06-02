import pickle
import matplotlib.pyplot as plt

def restore_curves(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

max_iterations = 256

(max_fitness5, min_fitness5, avg_fitness5, max_apple_eaten5, min_apple_eaten5, avg_apple_eaten5, max_snake_length5) = restore_curves("curve_53.pickle")
(max_fitness1, min_fitness1, avg_fitness1, max_apple_eaten1, min_apple_eaten1, avg_apple_eaten1, max_snake_length1) = restore_curves("curve_13.pickle")

fig, ax1 = plt.subplots()

color1 = 'tab:blue'
color2 = 'tab:red'
color3 = 'tab:green'
color4 = 'tab:orange'

ax1.set_xlabel('Itération')
ax1.set_ylabel('Fitness maximum', color=color1)
ax1.set_yscale('log')
# Key change: Use iterations as the x-axis data
ax1.plot(range(1, max_iterations + 1), max_fitness1[1:max_iterations + 1], color=color2, label='Fitness strat 1')
ax1.plot(range(1, max_iterations + 1), max_fitness5[1:max_iterations + 1], color=color1, label='Fitness strat 5')
ax1.tick_params(axis='y', labelcolor=color1)

ax1.legend(loc='upper left')  # Add a legend for clarity

color3 = 'tab:green'
ax2 = ax1.twinx()
ax2.set_ylabel('Pommes mangées maximum', color=color3)
# Key change: Use iterations as the x-axis data
ax2.plot(range(1, max_iterations + 1), max_apple_eaten1[1:max_iterations + 1], color=color4, label='Pommes strat 1')
ax2.plot(range(1, max_iterations + 1), max_apple_eaten5[1:max_iterations + 1], color=color3, label='Pommes strat 5')
ax2.tick_params(axis='y', labelcolor=color3)

ax2.legend(loc='lower right')

# Add Vertical Gridlines (The Key Change)
ax1.grid(axis='x', linestyle='--')  # Gridlines on the x-axis (iterations)
ax2.grid(axis='y', linestyle='--')  # You need to add it for the second axis too

# Additional styling improvement
plt.title('Fitness et pommes mangées fct. itération')
fig.tight_layout()
plt.savefig("curve_compare_cv.svg")
plt.savefig("curve_compare_cv.eps")
plt.savefig("curve_compare_cv.pdf")
plt.show()
