import cStorage as cStor
import cNavigation as cNav

THROTTLE = 1
CHARGE_BATTERY_THRESHOLD = 1
DISCHARGE_BATTERY_THRESHOLD = 0.2
TRAVEL_SLEEP_TIME = 1
RECHARGE_SLEEP_TIME = 1

class cDrone():
    
    drone:DroneSmall|DroneMedium|DroneLarge

    nav_throttle:float = THROTTLE

    def __init__(self,drone:DroneSmall|DroneMedium|DroneLarge):
        self.drone = drone
        return

    def get_drone(self) -> DroneSmall|DroneMedium|DroneLarge:
        return self.drone

    def status(self) -> str:
        return self.drone.status()

    def _battery_installed(self) -> bool:
        return hasattr(self.drone,"battery")

    def _bio_extractor_installed(self) -> bool:
        return hasattr(self.drone,"bio_extractor")

    def _bio_scanner_installed(self) -> bool:
        return hasattr(self.drone,"bio_scanner")

    def _cargo_installed(self) -> bool:
        return hasattr(self.drone,"cargo")

    def _oil_tank_installed(self) -> bool:
        return hasattr(self.drone,"oil_tank")

    def battery_below_threshold(self) ->bool:
        if not self._battery_installed():
            return False
        return self.drone.battery.percent() < DISCHARGE_BATTERY_THRESHOLD

    def set_throttle(self,throttle:float=THROTTLE):
        self.nav_throttle = throttle
        return
        
    def get_throttle(self) -> float:
        return self.nav_throttle

    def travel_to(self,x:int,y:int,throttle:float|None = None,ignore_battery:bool=False):
        self.drone.set_throttle(throttle if throttle else THROTTLE)
        self.drone.go_to(x,y)
        while self.drone.status() == "traveling":
            if not ignore_battery and self.battery_below_threshold():
                self.recharge()
            sleep(TRAVEL_SLEEP_TIME)
        return
        
    def travel_to_station(self,station_id:str,throttle:float|None = None,ignore_battery:bool=False):
        self.drone.set_throttle(throttle if throttle else THROTTLE)
        self.drone.go_to_station(station_id)
        while self.drone.status() == "traveling":
            if not ignore_battery and self.battery_below_threshold():
                self.recharge()
            sleep(TRAVEL_SLEEP_TIME)
        return
        
    def travel_to_drill(self,drill_id:str,throttle:float|None = None,ignore_battery:bool=False):
        self.drone.set_throttle(throttle if throttle else THROTTLE)
        self.drone.go_to_drill(drill_id)
        while self.drone.status() == "traveling":
            if not ignore_battery and self.battery_below_threshold():
                self.recharge()
            sleep(TRAVEL_SLEEP_TIME)
        return

    def get_drone_service_station_refs(self) -> list[BuildingRef]:
        drone_service_station_refs = []
        for outpost_ref in get_component("outpost_network").outposts():
            drone_service_station_refs+=outpost_ref.buildings("drone_service_station")
        return drone_service_station_refs

    def get_nearest_drone_service_station_refs(self) -> BuildingRef:
        return cNav.get_nearest_building_ref(
            self.get_drone_service_station_refs(),
            self.drone.position().x,
            self.drone.position().y
        )

    def recharge(self):
        self.travel_to_station(self.get_nearest_drone_service_station_refs().id,throttle=THROTTLE/2,ignore_battery=True)
        while self.drone.battery.percent() < CHARGE_BATTERY_THRESHOLD:
            sleep(RECHARGE_SLEEP_TIME)
        return

    













