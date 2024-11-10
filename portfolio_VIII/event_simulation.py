import numpy as np
import matplotlib.pyplot as plt

class SimplePollingQueue:
    def __init__(self, arrival_rate=100, service_rate=100, capacity=None):
        """
        Simple Polling Station Queue Simulator
        
        Parameters:
        - arrival_rate: voters per hour
        - service_rate: voters per hour
        - capacity: maximum queue capacity (optional)
        """
        self.arrival_rate = arrival_rate    # Keep as per hour
        self.service_rate = service_rate    # Keep as per hour
        self.capacity = capacity
        
        # Current state
        self.queue_length = 0
        self.time = 0
        
        # Keep track of these for plotting
        self.queue_history = []
        self.time_history = []
        
        # Statistics
        self.total_voters = 0
    
    def run_simulation(self, duration_hours=12):
        """Run the simulation for specified hours"""
        duration = duration_hours * 60  # Convert to minutes
        
        while self.time < duration:
            # Record current state
            self.queue_history.append(self.queue_length)
            self.time_history.append(self.time)
            
            # Generate random arrival and service events
            if np.random.random() < self.arrival_rate/60:  # Convert to per minute probability
                if self.capacity is None or self.queue_length < self.capacity:
                    self.queue_length += 1
                    self.total_voters += 1
            
            if np.random.random() < self.service_rate/60 and self.queue_length > 0:  # Convert to per minute probability
                self.queue_length -= 1
            
            self.time += 1
    
    def plot_results(self):
        """Visualize the queue length over time"""
        plt.figure(figsize=(10, 6))
        plt.plot(np.array(self.time_history)/60, self.queue_history, 'b-', 
                label='Queue Length')
        plt.xlabel('Time (hours)')
        plt.ylabel('Number of Voters in Queue')
        plt.title('Polling Station Queue Analysis')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.savefig('portfolio_VIII/figure_1.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("\nSimulation Results:")
        print(f"Total Voters: {self.total_voters}")
        print(f"Average Queue Length: {np.mean(self.queue_history):.1f}")
        print(f"Maximum Queue Length: {max(self.queue_history)}")

# Run simulation
if __name__ == "__main__":
    # Example: 20 arrivals per hour, 15 services per hour
    sim = SimplePollingQueue(arrival_rate=20, service_rate=30, capacity=10)
    sim.run_simulation(duration_hours=8)  # Run for 8 hours
    sim.plot_results()