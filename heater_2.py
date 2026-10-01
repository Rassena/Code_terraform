VALUES = {
    "clear":5,
    "dust_storm":3,
    "heat_bleed":9,
    "dust_veil":2
}


last_state:str= ""


if self.tier() == 3:
    self.steam_in.connect("gas_tank_1")

while True:
    current_state = self.thermal_state()
    if current_state != last_state:
        self.set_power(VALUES.get(current_state))
        print(current_state,VALUES.get(current_state),self.efficiency())
        last_state = current_state