"""
This is code for Project 1. Here we simulate bus lateness as a function of exponential distribution.
"""

import numpy as np
import matplotlib.pyplot as plt

# assuming the average bus = 5 mins late
average_late = 5
rate = 1 / average_late  # i.e. lambda

# yvals
lateness = np.random.exponential(1/rate, 50)

# xvals
bus_numbers = np.linspace(1,50,50)

plt.plot(bus_numbers, lateness, "ro", label ="simulated lateness")
plt.axhline(y=average_late, color='b', linestyle='--', label="average lateness")
plt.xlabel("bus number")
plt.ylabel("lateness (mins)")
plt.title("lateness of busses simulated through exponential distrbution")
plt.legend()
plt.savefig('portfolio_1/figure_1.png')
plt.show()
