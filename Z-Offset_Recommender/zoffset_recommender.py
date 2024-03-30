import numpy as np
import matplotlib.pyplot as plt

# Define the mesh values
points = np.array([
    [0.062742, 0.060232, 0.032626, 0.022587, 0.005019, -0.012548, -0.025097, -0.027607, -0.005019, 0.007529, 0.017568],
    [0.035136, 0.032626, 0.007529, -0.005019, -0.005019, 0.005019, 0.007529, -0.010039, -0.0, 0.00251, 0.012548],
    [0.012548, 0.017568, 0.025097, 0.010039, 0.007529, 0.017568, 0.030116, 0.040155, 0.042665, 0.037645, 0.057723],
    [0.007529, -0.00251, 0.005019, 0.012548, 0.017568, 0.050194, 0.027607, 0.035136, 0.040155, 0.025097, 0.022587],
    [-0.0, 0.010039, 0.007529, 0.007529, 0.007529, 0.035136, 0.017568, 0.022587, 0.037645, 0.027607, 0.025097],
    [-0.00251, 0.005019, -0.00251, -0.00251, 0.012548, 0.027607, 0.022587, 0.030116, 0.030116, 0.030116, 0.025097],
    [0.022587, 0.007529, -0.010039, -0.00251, -0.015058, -0.005019, 0.005019, 0.022587, 0.027607, 0.010039, 0.017568],
    [0.055213, 0.032626, 0.012548, -0.0, -0.017568, -0.015058, -0.020078, -0.015058, 0.007529, 0.010039, 0.037645],
    [0.095368, 0.062742, 0.012548, -0.030116, -0.067762, -0.070271, -0.070271, -0.062742, -0.027607, -0.017568, 0.010039],        
    [0.090349, 0.037645, -0.030116, -0.0778, -0.105407, -0.095368, -0.092858, -0.105407, -0.065252, -0.020078, 0.007529],
    [0.075291, 0.015058, -0.025097, -0.092858, -0.143052, -0.168149, -0.173168, -0.115446, -0.060233, -0.015058, 0.027607],  
])

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

