from simulation import Simulation


# Define simulation parameters




num_networks = 5
min_users = 2
max_users = 15
variance = 50
grid_range = 400
radius_range = (50, 500)
num_channels = 10
sinr_threshold = 4  # in dBm for later
transmit_power = 2  # in dBW for later
antenna_gain = 1  # G_R, G_T
antenna_height = 1  # H_R, H_T
base_freq = 208 # f0
total_bandwidth = 20  # B
# Create and run the simulation
simulation = Simulation(num_networks, min_users, max_users, variance, grid_range, radius_range, num_channels,base_freq, sinr_threshold,total_bandwidth)
simulation.generate_networks(transmit_power, antenna_gain, antenna_height)
simulation.generate_users()
simulation.visualize_topology()
simulation.generate_channel()
simulation.print_channels()
simulation.test_sinr()