self.steam_out.connect("gas_tank_1")
self.set_throttle(1)

VENTING_MAX = 2000

while True:

    self.steam_out.flow_rate()
    
    if self.pressure()> 0.98 and self.relief()<1:
        self.set_relief(1)
    if self.pressure()> 0.95 and self.relief()<1:
        self.set_relief(
            max(
                0,
                (self.capture_rate()-self.steam_out.flow_rate())/VENTING_MAX)
        )
    elif self.pressure() < 0.9 and self.relief()>0:
        self.set_relief(0)
    
    sleep(0.1)