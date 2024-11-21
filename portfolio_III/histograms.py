"""
This is code for portfolio III. Here we 
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nbinom

def negative_binomial(r, p):
    return nbinom.rvs(r, p)

def histo_estimate(nsamples):
    r, p = 5, 0.5
    max_trials = 15
    histo = np.zeros(max_trials)
    for _ in range(nsamples):
        rand = negative_binomial(r, p)
        if rand < max_trials:
            histo[rand] += 1
    return histo / nsamples

nsamples, nresamples = 50, 500
max_trials = 15
histo_samples = np.zeros([nresamples, max_trials])
for i in range(nresamples):
    histo_samples[i] = histo_estimate(nsamples)

lower, upper, median = np.zeros(max_trials), np.zeros(max_trials), np.zeros(max_trials)
for i in range(max_trials):
    median[i] = np.median(histo_samples[:, i])
    lower[i] = np.percentile(histo_samples[:, i], 17)
    upper[i] = np.percentile(histo_samples[:, i], 83)

error = (upper - lower) / 2

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(range(max_trials), median, width=0.6, alpha=0.7)
ax.errorbar(range(max_trials), median, yerr=error, fmt='ko', capsize=5)
ax.set_xlabel('Number of Trials')
ax.set_ylabel('fraction of occurrences')
ax.set_title('Negative Binomial distribution estimate with error bars')
ax.set_xlim(-0.5, max_trials-0.5)
ax.set_ylim(bottom=0)
ax.bar([], [], color='C0', alpha=0.7, label='Median Estimate')
ax.errorbar([], [], yerr=1, fmt='ko', capsize=5, label='66% Confidence Interval')
ax.legend()

plt.tight_layout()
plt.savefig(f'portfolio_III/figure_1.png')
plt.show()
