class Effect:
    def __init__(self, name, duration=0):
        self.name = name
        self.duration = duration
        self.elapsed_time = 0
        self.is_active = True
    def reapply(self):
        #REAPPLY HAPPENS WHEN THE EFFECT IS ADDED, WHILE STILL ACTIVE
        self.elapsed_time = 0
    def update(self, delta_time: float, target):
        if self.elapsed_time >= self.duration:
            self.remove(target)
            self.is_active = False
        else:
            self.elapsed_time += delta_time
    def __eq__(self, other):
        return self.name == other.name

class EffectManager:
    def __init__(self):
        self.effects = []

    def add_effect(self, effect: Effect) -> None:
        existing_instance: Effect = next((e for e in self.effects if e == effect), None)
        if existing_instance:
            existing_instance.reapply()
        else:
            self.effects.append(effect)
    
    def update(self, delta_time: float, target):
        for effect in self.effects[:]:
            effect.update(delta_time, target)
            if not effect.is_active:
                self.effects.remove(effect)

class BurnEffect(Effect):
    #BURN EFFECT DEALS DAMAGE OVERTIME
    def __init__(self, damage, duration=0):
        super().__init__("Burn", duration)
        self.dps = damage
        self.tick_interval = 1
        self.tick_accumulator = 0
    def update(self, delta_time: float, target):
        if not self.is_active:
            return
        self.elapsed_time += delta_time
        self.tick_accumulator += delta_time
        if self.tick_accumulator >= self.tick_interval:
            ticks = self.tick_accumulator // self.tick_interval
            dmg = ticks * self.dps
            target.take_damage(dmg)
            self.tick_accumulator %= self.tick_interval

        if self.elapsed_time >= self.duration:
            self.is_active = False
            
class SlowEffect(Effect):
    #SLOW EFFECT SLOWS THE TARGET FOR ANY AMOUNT OF TIME
    def __init__(self, duration=5, percentage=0, amount=0):
        super().__init__("Slow", duration)
        self.percentage = percentage
        self.amount = amount
        self.is_applied = False
        self.target_original_move_speed = 0
    def apply(self, target):
        self.is_applied = True
        self.target_original_move_speed = target.move_speed
        if self.percentage > 0:
            target.move_speed *= (1 - self.percentage)
        if self.amount > 0:
            target.move_speed = max(0, target.move_speed - self.amount)
    def remove(self, target):
        if self.is_applied:
            target.move_speed = self.target_original_move_speed
            
    def update(self, delta_time: float, target):
        if not self.is_active:
            return
        if not self.is_applied:
            self.apply(target)

        self.elapsed_time += delta_time

        if self.elapsed_time >= self.duration:
            self.is_active = False
            self.remove(target)

class Regeneration(Effect):
    #REGENERATION HEALS THE TARGET OVERTIME
    def __init__(self, hps, duration=0):
        super().__init__("Regeneration", duration)
        self.hps = hps
        self.tick_interval = 1
        self.tick_accumulator = 0
    def update(self, delta_time: float, target):
        if not self.is_active:
            return
        self.elapsed_time += delta_time
        self.tick_accumulator += delta_time
        if self.tick_accumulator >= self.tick_interval:
            ticks = self.tick_accumulator // self.tick_interval
            hp = ticks * self.hps
            target.heal(hp)
            self.tick_accumulator %= self.tick_interval

        if self.elapsed_time >= self.duration:
            self.is_active = False

class Strength(Effect):
    #STRENGTH GIVES BONUS DAMAGE TO THE TARGET
    def __init__(self, dmg_amount=0, dmg_percent=0, duration=0):
        super().__init__("Strength", duration)
        self.dmg_amount = dmg_amount
        self.dmg_percent = dmg_percent
    def update(self, delta_time: float, target):
        if not self.is_active:
            return
        self.elapsed_time += delta_time

        if self.elapsed_time >= self.duration:
            self.is_active = False