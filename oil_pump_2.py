oil_tank = get_component("liquid_tank_2")


self.oil_out.connect(oil_tank.id)

while True:
    self.set_throttle(1)