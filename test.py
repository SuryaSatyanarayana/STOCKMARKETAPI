import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Plotting the graph
plt.plot(x, y, marker='o', linestyle='-')

# Adding title and labels
plt.title('Sample Graph')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Save the plot to a file
plt.savefig('sample_graph.png')


# Close the plot to free up memory
plt.close()