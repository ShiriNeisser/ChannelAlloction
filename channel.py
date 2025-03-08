

class Channel:
    def __init__(self, channel_id, frequency, bandwidth):
        self.channel_id = channel_id          # Unique ID for the channel
        self.frequency = frequency            # Frequency in MHz
        self.bandwidth = bandwidth            # Bandwidth in MHz
        self.assigned_users = []              # Users assigned to this channel
        self.interference_power = 0.0         # Interference power on the channel

    def __repr__(self):
        return f"Channel {self.channel_id} ({self.frequency} MHz)"

