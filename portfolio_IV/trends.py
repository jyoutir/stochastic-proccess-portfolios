import numpy as np
import matplotlib.pyplot as plt

def stock_simulation(start_price, days, p, percentage_change):
    price = start_price
    for _ in range(days):
        if np.random.uniform(0, 1) < p:
            price *= (1 + percentage_change)  # Stock price goes up by a percentage
        else:
            price *= (1 - percentage_change)  # Stock price goes down by a percentage
    return price

def average_stock_price(start_price, days, p_values, simulations, percentage_change):
    averages = []
    errors = []
    for p in p_values:
        results = [stock_simulation(start_price, days, p, percentage_change) for _ in range(simulations)]
        avg_price = np.mean(results)
        sample_variance = np.var(results, ddof=1)
        standard_error = np.sqrt(sample_variance / simulations)
        z_score = 1.96  # for a 95% confidence interval
        error = z_score * standard_error
        averages.append(avg_price)
        errors.append(error)
    return averages, errors

# Parameters
start_price = 100
days = 30
simulations = 200
p_values = [0.4, 0.45, 0.5, 0.55, 0.6]  # Probability of stock price increase
percentage_change = 0.01  # 1% change in price

# Calculate average stock prices and errors
averages, errors = average_stock_price(start_price, days, p_values, simulations, percentage_change)

# Plot the graph
plt.errorbar(p_values, averages, yerr=errors, fmt='ko')
plt.xlabel('Probability of Stock Price Increase')
plt.ylabel('Average Stock Price After 30 Days')
plt.title('Stock Price Simulation with Percentage Changes')
plt.grid(True)
plt.savefig(f'portfolio_IV/figure_1.png')
plt.show()