import numpy as np
from user import User
class Network:
    def __init__(self, network_id, center_x, center_y, transmit_power, antenna_gain, antenna_height):
        self.network_id = network_id
        self.center = (center_x, center_y)
        self.transmit_power = transmit_power
        self.antenna_gain = antenna_gain
        self.antenna_height = antenna_height
        self.users = []  # List of User objects

    def add_users(self, num_users, variance):
        # Create the central point (Ma)
        central_user = User(
            user_id=0,
            position=self.center,
            network_id=self.network_id,
            is_central_point=True
        )
        self.users.append(central_user)

        # Create regular users and assign the central point
        for user_id in range(1, num_users + 1): # page 4:'The spatial distribution. of users within each network is determined by a multi-variate Gaussian distribution'
            x = np.random.normal(self.center[0], variance)
            y = np.random.normal(self.center[1], variance)
            position = (x, y)
            user = User(
                user_id=user_id,
                position=position,
                network_id=self.network_id,
                central_point=central_user  # Reference to the central point
            )
            self.users.append(user)
