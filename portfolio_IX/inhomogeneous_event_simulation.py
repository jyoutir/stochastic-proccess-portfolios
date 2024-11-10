import numpy as np
import matplotlib.pyplot as plt

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
    
    def run_simulation(self, duration_hours=12):
        """Run the simulation for specified hours"""
        duration = duration_hours * 60  # Convert to minutes
        
        while self.time < duration:
            current_hour = self.time / 60  # Convert current time to hours
            current_arrival_rate = self.arrival_rate(current_hour)
            
            # Record current state
            self.queue_history.append(self.queue_length)
            self.time_history.append(current_hour)
            self.arrival_rate_history.append(current_arrival_rate)
            
            # Generate random arrival and service events
            if np.random.random() < current_arrival_rate/60:  # Convert to per minute probability
                if self.capacity is None or self.queue_length < self.capacity:
                    self.queue_length += 1
                    self.total_voters += 1
                else:
                    self.rejected_voters += 1
            
            if np.random.random() < self.service_rate/60 and self.queue_length > 0:
                self.queue_length -= 1
            
            self.time += 1
    
    def plot_results(self):
        """Visualize the queue length and arrival rate over time"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot queue length
        ax1.plot(self.time_history, self.queue_history, 'b-', label='Queue Length')
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Number of Voters in Queue')
        ax1.set_title('Polling Station Queue Analysis')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot arrival rate
        ax2.plot(self.time_history, self.arrival_rate_history, 'r-', label='Arrival Rate')
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

# Run simulation
if __name__ == "__main__":
    sim = TimeVaryingPollingQueue(base_rate=5, service_rate=25, capacity=20)
    sim.run_simulation(duration_hours=24)  # Run for 24 hours
    sim.plot_results()