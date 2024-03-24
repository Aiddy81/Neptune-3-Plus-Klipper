import numpy as np
import matplotlib.pyplot as plt

# Define the mesh values
points = np.array([
    [0.120465, 0.072781, 0.084075, 0.037645, 0.03639, 0.04141, 0.066507, 0.060232, 0.069016, 0.1167, 0.156855],
    [0.072781, 0.060232, 0.058978, 0.037645, 0.045174, 0.072781, 0.067762, 0.056468, 0.091604, 0.114191, 0.145562],
    [0.067762, 0.076545, 0.070271, 0.090349, 0.08282, 0.094113, 0.102897, 0.127994, 0.12423, 0.149326, 0.164385],
    [0.071526, 0.097878, 0.085329, 0.115446, 0.107917, 0.150581, 0.144307, 0.136778, 0.141797, 0.148072, 0.136778],
    [0.069016, 0.087839, 0.099133, 0.0778, 0.096623, 0.100387, 0.101642, 0.097878, 0.104152, 0.111681, 0.115446],
    [0.089094, 0.095368, 0.0778, 0.109171, 0.101642, 0.126739, 0.125484, 0.109171, 0.105407, 0.12172, 0.127994],
    [0.104152, 0.097878, 0.057723, 0.056468, 0.061487, 0.055213, 0.065252, 0.092858, 0.084075, 0.084075, 0.095368],
    [0.153091, 0.11921, 0.091604, 0.084075, 0.084075, 0.066507, 0.099133, 0.069016, 0.102897, 0.110426, 0.135523],
    [0.174423, 0.141797, 0.092858, 0.048939, 0.026352, 0.017568, 0.025097, 0.058978, 0.0778, 0.110426, 0.171914],
    [0.193246, 0.127994, 0.069016, 0.053958, -0.016313, 0.005019, -0.023842, 0.010039, 0.065252, 0.117955, 0.179443],
    [0.195756, 0.143052, 0.056468, 0.011294, -0.052703, -0.0389, -0.008784, 0.013803, 0.066507, 0.16313, 0.233401],
])

# Display the mesh in a matrix
#plt.imshow(points, cmap='hot', interpolation='nearest')
#plt.colorbar(label='Z-offset')
#plt.title('Mesh Z-offsets')
#plt.show()

# Calculate the best z-offset (the one that minimizes the standard deviation)
#best_z_offset = np.mean(points)
#print(f"The best Z-offset is {best_z_offset}")

# Calculate the best z-offset (the one that minimizes the standard deviation)
best_z_offset = np.mean(points)

# Create a figure and axis
fig, ax = plt.subplots()

# Display the mesh in a matrix
#List of colour Map options
#https://matplotlib.org/stable/users/explain/colors/colormaps.html
cax = ax.imshow(points, cmap='bwr', interpolation='nearest')

# Add the colorbar
cbar = fig.colorbar(cax, label='Probed Values')

# Add the mesh values to the heatmap
for i in range(points.shape[0]):
    for j in range(points.shape[1]):
        ax.text(j, i, round(points[i, j], 2), ha='center', va='center', color='black')

# Set the title including the best Z-offset
plt.title('Mesh Z-offsets\nRecommended Z-offset: {:.4f}'.format(best_z_offset))

# Show the plot
plt.show()

