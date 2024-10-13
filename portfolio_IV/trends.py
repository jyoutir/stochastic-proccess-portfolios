"""
This is code for portfolio IV. Here we simulate median stock returns with error bars for different probabilities. 
"""

import numpy as np
import matplotlib.pyplot as plt

def stock_simulation(start_price, days, p, mean_change, std_dev_change):
    price = start_price
    for _ in range(days):
        daily_change = np.random.normal(mean_change, std_dev_change)
        adjustment = 1 + daily_change if np.random.rand() < p else 1 - daily_change
        price *= adjustment
    return price

def average_stock_price(start_price, days, p_values, simulations, mean_change, std_dev_change):
    averages, errors = [], []
    for p in p_values:
        results = [stock_simulation(start_price, days, p, mean_change, std_dev_change) for _ in range(simulations)]
        avg_price = np.mean(results)
        error = 1.96 * np.std(results, ddof=1) / np.sqrt(simulations)  # 95% confidence interval
        averages.append(avg_price)
        errors.append(error)
    return averages, errors

# Parameters
start_price = 100
days = 30
simulations = 200
p_values = [0.4, 0.45, 0.5, 0.55, 0.6]
mean_change = 0.1
std_dev_change = 0.05

# Calculate average stock prices and errors
averages, errors = average_stock_price(start_price, days, p_values, simulations, mean_change, std_dev_change)

# Plot the graph
plt.errorbar(p_values, averages, yerr=errors, fmt='ko')
plt.xlabel('Probability of Stock Price Increase')
plt.ylabel('Average Stock Price After 30 Days')
plt.title('Stock Price Simulation with Variable Percentage Changes')
plt.grid(True)
plt.savefig('portfolio_IV/figure_2.png')
plt.show()