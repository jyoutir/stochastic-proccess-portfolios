import numpy as np
import matplotlib.pyplot as plt

# transition matrix with hypothetical probabilities
transition_matrix = np.array([
    [0.8, 0.1, 0.1],  # G to G, Y, R
    [0.2, 0.7, 0.1],  # Y to G, Y, R
    [0.1, 0.2, 0.7]   # R to G, Y, R
])

# function to simulate Markov chain
def simulate_markov_chain(trans, steps, initial_state=0):
    num_states = trans.shape[0]
    current_state = initial_state
    state_visits = np.zeros(num_states)

    for i in range(steps):
        state_visits[current_state] += 1
        current_state = markov_move(trans, current_state)

    return state_visits / steps

# markov move function
def markov_move(trans, start):
    myrand = np.random.uniform(0, 1)
    accum = 0
    for next_state, prob in enumerate(trans[start]):
        accum += prob
        if myrand <= accum:
            return next_state

# params to simulate
steps = 10000
block_size = 100
n_blocks = steps // block_size

# do block averaging
block_averages = np.array([
    simulate_markov_chain(transition_matrix, block_size)
    for i in range(n_blocks)
])

# calc mean and variance of block averages
mean_distribution = np.mean(block_averages, axis=0)
variance_distribution = np.var(block_averages, axis=0, ddof=1)

# ploptting
plt.figure(figsize=(6, 4))
plt.bar(['G', 'Y', 'R'], mean_distribution, yerr=np.sqrt(variance_distribution), color=['green', 'yellow', 'red'])
plt.title('Estimating Stationary Distribution of Traffic Light Transitions')
plt.xlabel('State')
plt.ylabel('Probability')
plt.tight_layout()
plt.savefig('./portfolio_VI/figure_1.png')
plt.show()


# cal;c standard error for table
standard_error = np.sqrt(variance_distribution / n_blocks)

# calc 95% confidence intervals
confidence_intervals = np.array([
    mean_distribution - 1.96 * standard_error,
    mean_distribution + 1.96 * standard_error
])

states = ['G', 'Y', 'R']
# save the table to a text file
with open('./portfolio_VI/table1.txt', 'w') as f:
    f.write(f"{'State':<5} {'Mean Probability':<20} {'Standard Error':<20} {'95% Confidence Interval':<30}\n")
    for i, state in enumerate(states):
        ci_low, ci_high = confidence_intervals[:, i]
        f.write(f"{state:<5} {mean_distribution[i]:<15.4f} {standard_error[i]:<15.4f} [{ci_low:.4f}, {ci_high:.4f}]\n")