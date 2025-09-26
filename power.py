import time

class Power:
    def __init__(self, type, duration =5):
        self.type = type
        self.start_time = time.time()
        self.duration = duration  # in seconds

    def expired(self):
        return (time.time() - self.start_time) > self.duration
    
    def time_left(self):
        return self.duration - (time.time() - self.start_time)