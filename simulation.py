from network import Network
from channel import Channel
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
"""
Important Notes:
the first step is to find center point and then the other point generated.
"""
class Simulation:
    def __init__(self, num_networks, min_users, max_users, variance, grid_range, radius_range, num_channels,base_freq, sinr_threshold,total_bandwidth):
        # Simulation Parameters
        self.num_networks = num_networks #
        self.min_users = min_users #add option to default= 2
        self.max_users = max_users #add option to default= 22
        self.variance = variance # imprortant to ganarete+ visuliza
        self.grid_range = grid_range #in the article its u1 in algo1 for the ganarate
        self.radius_range = radius_range #algo1: r
        self.num_channels = num_channels  # K will be a class in the future
        self.base_freq = base_freq
        self.bw = total_bandwidth / num_channels
        self.sinr_threshold = sinr_threshold  # SINR* was in table2, i didint do something with it
        self.networks = [] #dict of all the networks
        self.channels = [] #dict of all the channels
        self.users = [] #dict of all the users

    def generate_networks(self, transmit_power, antenna_gain, antenna_height):  #Algorim1
        for i in range(self.num_networks):
            if i == 0:
                center_x = random.uniform(-self.grid_range, self.grid_range)
                center_y = random.uniform(-self.grid_range, self.grid_range)
            else:
                # Relative positioning to an existing network
                ref_network = random.choice(self.networks)
                r = random.uniform(self.radius_range[0], self.radius_range[1])
                theta = random.uniform(0, 2 * np.pi)
                center_x = ref_network.center[0] + r * np.cos(theta)
                center_y = ref_network.center[1] + r * np.sin(theta)

            # Create a Network object
            network = Network(i, center_x, center_y, transmit_power, antenna_gain, antenna_height)
            self.networks.append(network)

    def generate_users(self): #after algo1: genarete all the other user thet not the central
        for network in self.networks:
            num_users = random.randint(self.min_users, self.max_users) #uniform [min_users,max_users]
            network.add_users(num_users, self.variance) #normal distrebution



    def generate_channel(self):
        for i in range(self.num_channels):
            frequency = self.base_freq + i * self.bw
            channel = Channel(i, frequency, self.bw)
            self.channels.append(channel)


    def visualize_topology(self):
        plt.figure(figsize=(10, 10))

        for network in self.networks:
            # Plot the users
            color = plt.cm.tab10(network.network_id % 10)
            for user in network.users:
                plt.scatter(user.position[0], user.position[1], color=color, alpha=0.7)

            # Draw the central point label "Ma"
            central_user = network.users[0]  # Assuming the first user is the central point
            plt.text(
                central_user.position[0],
                central_user.position[1],
                "Ma",
                fontsize=12,
                weight='bold',
                color='black', #mabe change to the color of the network later.
                ha='center',
                va='center'
            )

            # Draw the network ID near the center CPT did it
            plt.text(
                central_user.position[0] + 30,  # Offset for visibility
                central_user.position[1] - 20,
                f"{network.network_id + 1}",
                fontsize=12,
                color=color,
                weight='bold'
            )

            # Draw an ellipse around the users
            ellipse = patches.Ellipse(
                (network.center[0], network.center[1]),
                width=2 * self.variance,
                height=1.5 * self.variance,
                edgecolor=color,
                facecolor='none',
                linestyle='--',
                linewidth=2
            )
            plt.gca().add_patch(ellipse)

        # Adjust axis scaling and add labels
        plt.xlim(1100, 1600)
        plt.ylim(1200, 2300)
        plt.xlabel("X [m]", fontsize=14)
        plt.ylabel("Y [m]", fontsize=14)
        plt.title("Network Center Points and User Locations", fontsize=16)
        plt.grid(True)
        plt.axis('equal')  # Consistent aspect ratio

        plt.show()

    def print_channels(self):
        for channel in self.channels:
            print(channel)

    #Check the sinr computation without generating all the networks... simple so it could be debugged
    def test_sinr(self):
        #will implement after finishing the user class :sinr calculation
       pass
