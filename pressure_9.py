
if self.tier() == 3:
    self.water_in.connect("liquid_tank_1")

while True:
    if self.gauge() > self.next_window_low() and self.gauge() < self.next_window_high():
        self.sync()