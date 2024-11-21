import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class TimeVaryingPollingQueue:
    def __init__(self, base_rate=10, service_rate=15, capacity=None):
        """
        Time-Varying Polling Station Queue Simulator

        Parameters:
        - base_rate: background arrival rate (per hour)
        - service_rate: service rate (per hour)
        - capacity: maximum queue capacity (optional)
        """
        self.base_rate = base_rate
        self.service_rate = service_rate
        self.capacity = capacity

        # Define peak periods (times in hours)
        self.peaks = [
            {"amplitude": 30, "time": 9, "width": 1.5},    # Morning peak at 9 AM
            {"amplitude": 20, "time": 12, "width": 2},     # Lunch peak at 12 PM
            {"amplitude": 25, "time": 16.5, "width": 1.5}, # Afternoon peak at 4:30 PM
        ]

        # Current state
        self.queue_length = 0
        self.time = 0

        # Keep track of these for plotting
        self.queue_history = []
        self.time_history = []
        self.arrival_rate_history = []

        # Statistics
        self.total_voters = 0
        self.rejected_voters = 0

        # Compute M, the maximum of lambda(t)
        self.M = self.compute_max_arrival_rate()

    def compute_max_arrival_rate(self):
        """Compute maximum of arrival_rate(t) over the duration"""
        # Compute over fine-grained time points to find maximum
        t_values = np.linspace(0, 24, 1000)
        rates = [self.arrival_rate(t) for t in t_values]
        M = max(rates)
        return M * 1.1  # Add small buffer to ensure M ≥ lambda(t) for all t

    def arrival_rate(self, t):
        """
        Calculate arrival rate at time t
        t: time in hours
        """
        rate = self.base_rate
        for peak in self.peaks:
            A = peak["amplitude"]
            t_peak = peak["time"]
            sigma = peak["width"]
            rate += A * np.exp(-((t - t_peak)**2) / (2 * sigma**2))
        return rate

    def generate_next_arrival_time(self, current_time):
        """
        Generate the next arrival time using thinning algorithm
        """
        t = current_time
        while True:
            # Generate S ~ Exponential(M)
            S = np.random.exponential(scale=1 / self.M)
            t_candidate = t + S
            if t_candidate >= self.simulation_end_time:
                return None  # No more arrivals within the simulation time
            # Acceptance probability
            U = np.random.uniform(0, 1)
            lambda_t_candidate = self.arrival_rate(t_candidate)
            if U <= lambda_t_candidate / self.M:
                return t_candidate
            else:
                t = t_candidate  # Continue to next candidate time

    def generate_service_time(self):
        """Generate a service time"""
        return np.random.exponential(scale=1 / self.service_rate)

    def run_simulation(self, duration_hours=12):
        """Run the simulation for specified hours"""
        self.simulation_end_time = duration_hours  # in hours
        t = 0  # current time in hours
        queue_length = 0
        self.queue_history = []
        self.time_history = []
        self.arrival_rate_history = []
        self.total_voters = 0
        self.rejected_voters = 0

        # Initialize event times
        # Generate first arrival time
        t_arrival = self.generate_next_arrival_time(t)
        # No departure scheduled initially
        t_departure = np.inf

        while True:
            # If no more arrivals and queue is empty, simulation ends
            if t_arrival is None and (queue_length == 0 or t_departure == np.inf):
                break
            # Next event occurs at min of next arrival or next departure
            if t_arrival is not None and t_arrival <= t_departure:
                t = t_arrival
                current_arrival_rate = self.arrival_rate(t)
                self.queue_history.append(queue_length)
                self.time_history.append(t)
                self.arrival_rate_history.append(current_arrival_rate)

                # Handle arrival event
                if self.capacity is None or queue_length < self.capacity:
                    queue_length += 1
                    self.total_voters += 1
                    if queue_length == 1:
                        # Queue was empty, schedule next departure
                        service_time = self.generate_service_time()
                        t_departure = t + service_time
                else:
                    self.rejected_voters += 1

                # Generate next arrival time
                t_arrival = self.generate_next_arrival_time(t)
            else:
                # Next event is a departure
                t = t_departure
                current_arrival_rate = self.arrival_rate(t)
                self.queue_history.append(queue_length)
                self.time_history.append(t)
                self.arrival_rate_history.append(current_arrival_rate)

                # Handle departure event
                queue_length -= 1
                if queue_length > 0:
                    # Generate next departure
                    service_time = self.generate_service_time()
                    t_departure = t + service_time
                else:
                    # Queue empty
                    t_departure = np.inf

    def run_multiple_simulations(self, n_simulations=30, duration_hours=24):
        avg_queue_lengths = []
        
        for i in range(n_simulations):
            print(f"Running simulation {i+1}/{n_simulations}")
            self.run_simulation(duration_hours)
            avg_queue_lengths.append(np.mean(self.queue_history))
        
        # Calculate mean and 95% confidence interval
        mean = np.mean(avg_queue_lengths)
        std_err = stats.sem(avg_queue_lengths)
        ci = stats.t.interval(confidence=0.95,  # Changed from alpha to confidence
                            df=len(avg_queue_lengths)-1,
                            loc=mean,
                            scale=std_err)
        return mean, ci[0], ci[1]



    def plot_results(self):
        """Visualize the queue length and arrival rate over time"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

        # Plot queue length
        ax1.step(self.time_history, self.queue_history, where='post', label='Queue Length')
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Number of Voters in Queue')
        ax1.set_title('Polling Station Queue Analysis')
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Plot arrival rate
        time_continuous = np.linspace(0, self.simulation_end_time, 1000)
        arrival_rates = [self.arrival_rate(t) for t in time_continuous]
        ax2.plot(time_continuous, arrival_rates, 'r-', label='Arrival Rate')
        ax2.set_xlabel('Time (hours)')
        ax2.set_ylabel('Arrival Rate (voters/hour)')
        ax2.set_title('Time-Varying Arrival Rate')
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        plt.tight_layout()
        plt.savefig('portfolio_IX/figure_1.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("\nSimulation Results:")
        print(f"Total Voters Served: {self.total_voters}")
        print(f"Rejected Voters: {self.rejected_voters}")
        print(f"Average Queue Length: {np.mean(self.queue_history):.1f}")
        print(f"Maximum Queue Length: {max(self.queue_history)}")
        print(f"Average Arrival Rate: {np.mean(self.arrival_rate_history):.1f} voters/hour")

# Modify the main block to use multiple simulations
if __name__ == "__main__":
    sim = TimeVaryingPollingQueue(base_rate=5, service_rate=25, capacity=20)
    
    # Run multiple simulations and get confidence interval
    mean_ql, ci_lower, ci_upper = sim.run_multiple_simulations(n_simulations=30, 
                                                             duration_hours=24)
    
    # Run one final simulation for plotting
    sim.run_simulation(duration_hours=24)
    sim.plot_results()
    
    # Add confidence interval information to the output
    print("\nConfidence Interval Analysis:")
    print(f"Average Queue Length: {mean_ql:.1f} ± {(ci_upper-ci_lower)/2:.1f}")
    print(f"95% CI: [{ci_lower:.1f}, {ci_upper:.1f}]")
