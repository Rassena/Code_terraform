oil_tank  = get_component("liquid_tank_2")
clock = get_component("clock")

self.oil_in.connect(oil_tank.id)
self.set_throttle(1)


while True:
    battery_fill = get_component("battery_large_2").get_level()/get_component("battery_large_2").get_capacity()
    self.set_throttle(1-battery_fill)
    sleep(round(clock.real_seconds_per_hour()/4))