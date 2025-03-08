import numpy as np


class User:
    def __init__(self, user_id, position, network_id, is_central_point=False, central_point=None):
        self.user_id = user_id                # Unique user ID
        self.position = position              # (x, y) coordinates
        self.network_id = network_id          # ID of the network the user belongs to
        self.is_central_point = is_central_point  # Is this the network manager?
        self.central_point = central_point    # Reference to the network's central point (another User object)
        self.assigned_channel = None          # Initially no channel is assigned
        self.signal_power = None              # Signal power (to be calculated later)
        self.interference = None              # Interference power (to be calculated later)
        self.sinr_j = None                      # SINR value of the communication with user j using the assigned channel (k)

    def assign_channel(self, channel):
        """
        Assign a channel to the user.
        for now, we will assign a channel randomly in the simulation the channel will be chosen.
        """
        self.assigned_channel = channel

    def calculate_path_loss(self, distance, freq, ht, hr, gt, gr):
        """Calculate path loss using the Egli model."""
        pl = (
            40 * np.log10(distance)
            - 20 * np.log10(40 / freq)
            - 20 * np.log10(ht * hr)
            - 10 * np.log10(gt * gr)
        )
        return pl #Denoated as PL^{n,n}_{i,j,k} in the paper

    def calculate_received_power(pt, path_loss):
        """Calculate received power."""
        return pt - path_loss #Denoated as PR^{n,n}_{i,j,k} in the paper

    def t_attenuation(self, k, k_tag):
        distance = np.abs(k - k_tag)
        if distance == 0:
            return 0
        elif distance == 1:
            return 20
        elif distance == 2:
            return 40
        elif distance == 3:
            return 50
        elif distance == 4:
            return 60
        elif distance > 5 and np.abs(k - k_tag) / k <= 0.05:
            return 95
        else:
            return 110

    def linear_to_db(self, linear_val):
        """Convert linear scale to dB."""
        return 10 * np.log10(linear_val)

    def db_to_linear(self,db_val):
        """Convert dB to linear scale."""
        return 10 ** (db_val / 10)

    def calculate_interference_power(self, other_users,assign_channel):
        #other_users is a list of all the other users in the network
        #assign_channel is the channel assigned to the user (k) in the paper
        """
        Calculate interference power.
        I^{n}_{j,k} at user j in network N^{n} on channel k is the sum over all other networks l, excluding N^{n}
        of the interference contributions
        \Phi^{n,l}_{j,k} from every user m in each network N^{l}
        """
        interference = 0
        for user in other_users:
            if user.assigned_channel is not None:
                interference += user.signal_power - self.t_attenuation(user.assigned_channel, assign_channel)
        return interference

    def thermal_noise_dBm(self, temp_k, bw_hz, noise_figure):
        """
        Calculate the thermal noise in dBm.
        temp_k: Temperature in Kelvin
        bw_hz: Channel bandwidth in Hz
        noise_figure: Receiver noise figure
        """
        k_b = 1.38e-23
        noise_watts = k_b * temp_k * bw_hz * noise_figure
        return self.linear_to_db(noise_watts) + 30 # convert to dBm

    def calculate_SINR(self,other_users, assign_channel, temp_k, bw_hz, noise_figure):
        """
        Calculate SINR value.
        SINR^{n,n}_{i,j,k} = PR^{n,n}_{i,j,k} / (I_T + I^{n}_{j,k})
        """
        # Step 1: Compute the distance from the central point
        distance = np.linalg.norm(np.array(self.position) - np.array(self.central_point.position))
        # Calculate signal power
        path_loss = self.calculate_path_loss(distance, assign_channel.frequency, 1, 1,1, 1)
        transmit_power = self.central_point.transmit_power
        self.signal_power = self.calculate_received_power(transmit_power, path_loss)

        # Calculate interference power
        self.interference = self.calculate_interference_power(other_users, assign_channel)

        # Calculate thermal noise
        thermal_noise = self.thermal_noise_dBm(temp_k, bw_hz, noise_figure)

        # Calculate SINR
        self.sinr = self.signal_power / (thermal_noise + self.interference)
        return self.sinr


"""

    def path_loss_egli(self,distance_m,freq_mhz,hr_m,ht_m,gt,gr):
        """
"""
        Egli Model path loss in dB
        :param distance_m: distance in meters
        :param freq_mhz: frequency in MHz
        :param hr_m: height of the receiver in meters
        :param ht_m: height of the transmitter in meters
        :param gt, gr: antenna gains (linear) or dBi?
            - If in dBi, we typically add them as dB in the final equation.
            - If linear, we convert to dB with 10*log10(g)
           PL (dB) = 40*log10(d) - 20*log10(40/f) - 20*log10(Ht * Hr) - 10*log10(Gt * Gr)
        """
""""
        if distance_m<0:
            raise ValueError("Distance must be non-negative")
        #Convert linear gains to dB if needed
        pl = (40*np.log10(distance_m)
              - 20*np.log10(freq_mhz)
              - 20*np.log10(hr_m * ht_m)
              - 10*np.log10(gt * gr))
        return pl

    


    

    def thermal_noise_dBm(self, temp_k,bw_hz,noise_figure): #I_{T}
        """
""""
        Calculate the thermal noise in dBm.
        temp_k: Temperature in Kelvin
        bw_hz: Channel bandwidth in Hz
        noise_figure: Receiver noise figure
        """
""""
        k_b = 1.38e-23 # Boltzmann constant
        #noise to watts = k_b * T * BW * NF
        noise_watts = k_b * temp_k * bw_hz * noise_figure
        noise_dbm = self.linear_to_db(noise_watts) + 30 #W -> mW=> +30
        return noise_dbm


    def __repr__(self):
        return f"User {self.user_id} ({self.position} {self.network_id} )"







"""