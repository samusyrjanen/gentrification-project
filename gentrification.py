import numpy as np
import matplotlib.pyplot as plt

# Sample data for yearly income of a district (replace this with your actual data)
income = [5, 8, 2, 3, 1, 6, 4, 9, 7, 2]

# Calculate the income change of the district
change = [income[i] - income[i - 1] for i in range(1, len(income))]
print(f'Change from the previous value:\n{change}')

# Calculate the mean change (in the future this would calculate the mean change of all districts that year)
mean_change = sum(change) / len(change)
print(f'\nMean change per year: {mean_change}')

# Difference to the mean change
difference_to_mean = [income_change - mean_change for income_change in change]
print(f'\nDifference to the mean change:\n{difference_to_mean}')

# Normalize the difference to the mean to a scale from -1 to 1
max_difference = max(difference_to_mean, key=abs)
normalized_difference = [difference / abs(max_difference) for difference in difference_to_mean]
print(f'\nNormalized Difference to Mean (-1 to 1):\n{normalized_difference}')

# Plot the results
plt.plot(difference_to_mean)
plt.xlabel('Year')
plt.ylabel('Gentrification Score')
plt.title('Gentrification Score Over Time')
plt.show()
