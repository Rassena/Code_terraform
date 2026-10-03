vehicles = [vehicle.id for vehicle in get_component("fleet").vehicles()]


def rescue(vehicle):
    if(
        not get_component(vehicle).is_being_rescued() 
        and not self.get_rescue_target()
    ):
        print("Rescue:",vehicle)
        self.dispatch_rescue(vehicle,0.18)
        

print(vehicles)


while True:
    vehicles = [vehicle.id for vehicle in get_component("fleet").vehicles()]
    for vehicle in vehicles:
        if(
            get_component(vehicle).battery.level() == 0
            and not vehicle in self.get_docked()
            and get_component(vehicle).battery.capacity()>0
        ):
            rescue(vehicle)
    for docked in self.get_docked():
        if (
            self.get_active().length < self.get_bay_count() 
            and self.status(docked)["state"] in [
                # "charging",
                "queued",
                "docked",
                # "target_reached",
                # "not_docked",
                # "station_offline",
                # "missing"
            ]
            
                
        ):
                self.charge(docked,1)


















        