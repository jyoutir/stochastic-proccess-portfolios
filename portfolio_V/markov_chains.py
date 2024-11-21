"""
This is code for portfolio V. Here we simulate a chronic gambler who has a dream to make it big and his probabilities using markov chains and hitting probabiliy
"""


import numpy as np
import matplotlib.pyplot as plt

# transition matrix P
P = np.array([
    [1,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0  ],  # State 0 (ruin)
    [0.5, 0,   0.5, 0,   0,   0,   0,   0,   0,   0,   0,   0  ],  # State 1
    [0,   0.5, 0,   0.5, 0,   0,   0,   0,   0,   0,   0,   0  ],  # State 2
    [0,   0,   0.5, 0,   0.5, 0,   0,   0,   0,   0,   0,   0  ],  # State 3
    [0,   0,   0,   0.5, 0,   0.5, 0,   0,   0,   0,   0,   0  ],  # State 4
    [0,   0,   0,   0,   0.5, 0,   0.5, 0,   0,   0,   0,   0  ],  # State 5
    [0,   0,   0,   0,   0,   0.5, 0,   0.5, 0,   0,   0,   0  ],  # State 6
    [0,   0,   0,   0,   0,   0,   0.5, 0,   0.5, 0,   0,   0  ],  # State 7
    [0,   0,   0,   0,   0,   0,   0,   0.5, 0,   0.5, 0,   0  ],  # State 8
    [0,   0,   0,   0,   0,   0,   0,   0,   0.5, 0,   0.5, 0  ],  # State 9
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0.5, 0,   0.5],  # State 10
    [0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   1  ]   # State 11 (winning state)
])

# extract Q (transitions between non-absorbing states)
Q = P[1:11, 1:11]  # Exclude states 0 and 11 (absorbing states)

# extract R (transitions to the winning state)
R = P[1:11, 11]

# calculate the fundamental matrix
I = np.eye(Q.shape[0])
N = np.linalg.inv(I - Q)

# Calculate hitting probabilities to the winning state (state 11)
hitting_probs = N @ R

# Add probabilities for absorbing states
hitting_probs = np.concatenate(([0], hitting_probs, [1]))

# Define all states (0 to 11) with corresponding dollar amounts
states = range(12)
dollar_amounts = ['$0', '$1K', '$2K', '$4K', '$8K', '$16K', '$32K', '$64K', '$128K', '$256K', '$512K', '$1024K']

# Plotting
plt.figure(figsize=(12, 6))
bars = plt.bar(states, hitting_probs)
plt.title('Hitting Probabilities for Winning State ($1,024,000)', fontsize=16)
plt.xlabel('Starting Amount', fontsize=14)
plt.ylabel('Probability of Reaching $1,024,000', fontsize=14)
plt.ylim(0, 1.1)  # Set y-axis limit from 0 to 1.1 to accommodate labels
plt.xticks(states, dollar_amounts, rotation=45, ha='right')

# Add probability values on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.4f}',
             ha='center', va='bottom')

# Highlight absorbing states
bars[0].set_color('red')  # Ruin state ($0)
bars[-1].set_color('green')  # Win state ($1,024,000)

plt.tight_layout()  # Adjust layout to prevent cutting off labels
plt.savefig('portfolio_V/figure_1.png', dpi=300, bbox_inches='tight')
plt.show()
