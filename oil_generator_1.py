oil_tank  = get_component("liquid_tank_2")
clock = get_component("clock")

self.oil_in.connect(oil_tank.id)
self.set_throttle(1)


while True:
    sleep(clock.real_seconds_per_hour())