"""
This is code for portfolio II. Here we ()
"""

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

# finds sample mean (for expo dist)
def sample_mean(n):
    sum = 0
    for i in range(n):
        sum += np.random.exponential(1) 
    return sum / n

# sample variance
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
    var = variance(n)/n
    lower = mean + scipy.stats.norm.ppf(0.05) * (var ** 0.5)
    upper = mean + scipy.stats.norm.ppf(0.95) * (var ** 0.5)
    return lower, mean, upper

def plot_clt(sample_sizes, num_samples):
    for i, size in enumerate(sample_sizes, 1):
        plt.figure(figsize=(8, 6))
        results = [mean_with_errors(size) for _ in range(num_samples)]
        means = [r[1] for r in results]
        
        plt.hist(means, bins=30, density=True, alpha=0.7)
        plt.title(f'Distribution of Sample Means (n={size})')
        plt.xlabel('Sample Mean')
        plt.ylabel('Density')
        plt.axvline(x=1.0, color='r', linestyle='--', label='true mean')
        plt.legend()

        plt.savefig(f'portfolio_II/figure_{i}.png')
        plt.close()

    print("\nMean with 90% confidence interval:")
    for size in sample_sizes:
        lower, mean, upper = mean_with_errors(size)
        print(f"n={size}: {mean:.4f} ({lower:.4f}, {upper:.4f})")

sample_sizes = [5, 20, 1000]
num_samples = 10000

plot_clt(sample_sizes, num_samples)
