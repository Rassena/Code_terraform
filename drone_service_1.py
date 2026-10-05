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
    drone_refs = [drone_ref for drone_ref in get_component("fleet").drones()]
    for drone_ref in drone_refs:
        drone = get_component(drone_ref.id)
        if(
            drone_ref.engine
            and drone_ref.battery_capacity>0
        ):
            if(
                drone.battery.level() == 0
                and not drone_ref.id in self.get_docked()
                and drone.battery.capacity()>0
            ):
                rescue(drone_ref.id)
                pass
        elif(
            not drone_ref.is_docked
        ):
            rescue(drone_ref.id)
            
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


















        