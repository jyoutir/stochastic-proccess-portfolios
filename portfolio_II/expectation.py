"""
This is code for portfolio II. Here we ()
"""

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

def sample_mean(n):
    sum = 0
    for i in range(n):
        sum += np.random.exponential(1) 
    return sum / n


def variance(n):
    total_squared = 0
    total = 0
    for i in range(n):
        x = np.random.exponential(1)
        total += x
        total_squared += x**2
    mean = total / n
    var = (n/(n-1))*(total_squared/n-(mean*mean))
    return var


def mean_with_errors(n):
    mean = sample_mean(n)
    var = variance(n) / n
    lower = mean + scipy.stats.norm.ppf(0.05) * (var ** 0.5)
    upper = mean + scipy.stats.norm.ppf(0.95) * (var ** 0.5)
    return lower, mean, upper


def plot_convergence(sample_sizes, num_trials):
    plt.figure(figsize=(10, 6))
    
    for size in sample_sizes:
        cumulative_means = np.zeros(num_trials)
        running_sum = 0
        
        for i in range(num_trials):
            running_sum += sample_mean(size)
            cumulative_means[i] = running_sum / (i + 1)
        
        plt.plot(range(1, num_trials + 1), cumulative_means, label=f'n={size}')

    plt.axhline(y=1.0, color='r', linestyle='--', label='true mean')
    plt.xscale('log')
    plt.xlabel('no. of trials')
    plt.ylabel('cumulative average of sample means')
    plt.title('convergence of sample means for exponential distribution')
    plt.legend()
    plt.show()

# usage
sample_sizes = [10, 100, 1000]
num_trials = 10000

plot_convergence(sample_sizes, num_trials)

