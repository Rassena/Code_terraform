steam_tank = get_component("gas_tank_1")

clock = get_component("clock")
battery = get_component("battery_large_2")
power_control = get_component("power_control")

power_grid = next(
    [
        power_grid
        for power_grid in power_control.grids()
        for member in power_grid.members
        if self.id == member.id
    ],
    None
)

thermal_caps = [
    get_component(thermal_cap.id)
    for thermal_cap in power_grid.members
    if thermal_cap.type_id == "thermal_cap"
]


self.steam_in.connect(steam_tank.id)
self.set_throttle(1)

while True:
    battery_fill = battery.get_level()/battery.get_capacity()
    # if (
    #     any(
    #         [
    #             thermal_cap.relief() > 0.5
    #             for thermal_cap in thermal_caps
    #         ]
    #     )
    # ):
    #     self.set_throttle(1)
    # else:
    self.set_throttle(1-battery_fill)

    sleep(round(clock.real_seconds_per_hour()/4))