import queue

class Wave:
    def __init__(self):
        self.wave_number
        self.enemies
        self.time_period
        self.reward
        self.elapsed_time = 0
        self.is_active = False

    def start(self):
        self.is_active = True

    def update(self, delta_time):
        if not self.is_active or not self.enemies:
            return
        
        self.elapsed_time += delta_time


        pass

    def spawn_enemy(self):
        if self.enemies:
            pass


    def render():
        pass

