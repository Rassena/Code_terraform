from cVehicle import cVehicle


class cRover(cVehicle):
    vehicle:Rover
    
    base_modules = {
        0: "nav_module",
        1: "sonar_module",
        2: "drill_module"
    }

    def get_rover(self) -> Rover:
        return self.vehicle
    
    