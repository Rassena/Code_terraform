drones = [drone.id for drone in get_component("fleet").drones()]


def rescue(drone):
    if(
        not get_component(drone).is_being_rescued() 
        and not self.get_rescue_target()
    ):
        print("Rescue:",drone)
        self.dispatch_rescue(drone,0.18)
        

print(drones)


while True:
    drones = [drone.id for drone in get_component("fleet").drones()]
    for drone in drones:
        if hasattr(get_component(drone),"battery"):
            if(
                get_component(drone).battery.level() == 0
                and not drone in self.get_docked()
                and get_component(drone).battery.capacity()>0
            ):
                rescue(drone)
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


















        