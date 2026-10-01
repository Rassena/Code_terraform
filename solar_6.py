clock = get_component("clock")

while True:
    self.set_tilt(90 - clock.get_elevation())

