
if self.tier() >= 3:
    self.water_in.connect("liquid_tank_1")

while True:
    atm = get_component("atmosphere")
    self.set_intake(atm.get_co2()/10)
    if self.waste() > 55:
        self.dump_waste()
