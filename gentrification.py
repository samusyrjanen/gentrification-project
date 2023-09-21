import numpy as np
import matplotlib.pyplot as plt

# Sample data for yearly income changes (replace this with your actual data)
income_changes = [5, 8, 2, -3, -1, 6, 4, 9, 7, -2]

# Calculate the gentrification index
gentrification_index = [(income_changes[i] - income_changes[i - 1]) / income_changes[i - 1] * 100 for i in range(1, len(income_changes))]

# Normalize the index
min_index = min(gentrification_index)
max_index = max(gentrification_index)
normalized_index = [2 * ((x - min_index) / (max_index - min_index)) - 1 for x in gentrification_index]

# Apply the sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

final_distribution = [sigmoid(x) for x in normalized_index]

# Plot the results
plt.plot(final_distribution)
plt.xlabel('Year')
plt.ylabel('Gentrification Score')
plt.title('Gentrification Score Over Time')
plt.show()
