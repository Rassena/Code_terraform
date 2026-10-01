self.steam_in.connect("gas_tank_1")
self.set_throttle(1)
clock = get_component("clock")


while True:
    battery_fill = get_component("battery_large_2").get_level()/get_component("battery_large_2").get_capacity()
    self.set_throttle(1-battery_fill)
    sleep(round(clock.real_seconds_per_hour()/4))