VENTING_MAX = 2000

gas_tanks = [
    get_component("gas_tank_1"),
    get_component("gas_tank_2"),
    get_component("gas_tank_3"),
    get_component("gas_tank_4")
]

gas_tank = gas_tanks[3]
self.steam_out.connect(gas_tank.id)
self.set_throttle(1)

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
    if gas_tanks[0].fill_pct()<0.2:
        self.steam_out.connect("gas_tank_1")
    elif gas_tanks[0].fill_pct()>0.9:
        self.steam_out.connect(gas_tank.id)
    sleep(0.1)