import cStorage as cStor
import cNavigation as cNav

journal = get_component("journal")

THROTTLE = 1
CHARGE_BATTERY_THRESHOLD = 1
DISCHARGE_BATTERY_THRESHOLD = 0.2
TRAVEL_SLEEP_TIME = 1
RECHARGE_SLEEP_TIME = 1


FAILED_ROUTE_STATES = [
  "stalled_no_battery",
  "stalled_no_oil",
  "stalled_no_route",
  "scrambled",
]

REAGENTS_ID = [
    "alkaline_buffer",
    "cryo_solvent",
    "protein_marker",
    "chelating_agent",
    "enzyme_solution",
]

coasta_life_forms_id = [
    "brine_plankton",
    "coral_fungus",
    "salt_crust",
    "sea_algae",
    "shore_lichen",
    "tide_moss"
]

frozen_life_forms_id = [
    "cold_spores",
    "frost_fungus",
    "frost_lichen",
    "ice_algae",
    "ice_crust",
    "snow_moss",
]

volcanic_life_forms_id = [
    "ash_spores",
    "black_fungus",
    "cinder_lichen",
    "lava_algae",
    "magma_crust",
    "sulfur_moss",
]

deep_life_forms_id = [
    "cave_fungus",
    "cave_moss",
    "crystal_spores",
    "deep_algae",
    "stone_lichen",
    "stone_mat"
]

geothermal_life_forms_id = [
    "heat_crust",
    "heat_lichen",
    "hot_spores",
    "steam_moss",
    "vent_algae",
    "vent_fungus"
]

plant_biomes = [
    "frozen",
    "coastal",
    "volcanic",
    "deep",
    "geothermal"
]

life_form_dock_name = {
    "frozen": "drone_station_lrg_3",
    "coastal":"drone_station_lrg_2",
    "volcanic":"drone_station_lrg_4",
    "deep": "drone_station_lrg_5",
    "geothermal": "drone_station_lrg_6"
}

life_forms_dict = {
    "frozen": frozen_life_forms_id,
    "coastal": coasta_life_forms_id,
    "volcanic": volcanic_life_forms_id,
    "deep": deep_life_forms_id,
    "geothermal": geothermal_life_forms_id
}

class cDrone():

    base_couple = {
        0: "electric_thruster",
        1: "cargo_pod_large",
        2: "portable_bio_scanner",
        3: "portable_bio_extractor",
        4: "battery_pack",
        5: "battery_pack"
    }
    
    mount_storage = {
        "electric_thruster": "large_warehouse_4",
        "cargo_pod_large": "large_warehouse_4",
        "portable_bio_scanner": "shop",
        "portable_bio_extractor": "shop",
        "battery_pack": "large_warehouse_3",
    }
    
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

    def travel_to(self,x:int,y:int,throttle:float|None = None,ignore_battery:bool=False,bio_collect:bool=False):
        self.drone.set_throttle(throttle if throttle else THROTTLE)
        self.drone.go_to(x,y)
        while self.drone.status() == "traveling":
            if(
                bio_collect
                and not self.is_biosite_ready([x,y])
            ):
                break
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

    def couple_base(self):
        self.drone.go_to_station("drone_station_lrg_1")
        for slot_index,module_id in self.base_couple.items():
            while (status := self.drone.couple(slot_index,module_id).status) == "item_not_in_inventory":
                storage_id = self.mount_storage.get(module_id)
                if storage_id == "shop":
                    shop = get_component("shop")
                    shop.buy(module_id,1)
                else:
                    storage:Warehouse = get_component(storage_id)
                    while storage.transfer_to("inventory",module_id,1).status == "busy":
                        pass
                pass
            print(slot_index,module_id,status)

    def get_LifeFormScanResult_biome(self,biome_name:str) -> list[LifeFormScanResult]:
        
        bio_list = []
    
        for bio_coord in journal.biomass_coords():
            if not bio_coord.is_empty:
                if bio_coord.life_forms[0].biome == biome_name:
                    bio_list.append(bio_coord)
        
        return bio_list
    
    def get_LifeFormScanResult_dict(self) -> dict[str,dict[str,dict[str,list[dict]]]]:
        life_forms_dict = {}
    
        for bio in journal.biomass_coords():
            for life_form in bio.life_forms:
                biome = life_forms_dict.setdefault(life_form.biome, {})
                rarity = biome.setdefault(life_form.rarity, {})
                life_forms = rarity.setdefault(life_form.type, [])
    
                life_forms.append({
                    "coord": bio.coord,
                    "tons": life_form.tons,
                    "remaining_tons": life_form.remaining_tons,
                })
    
        return life_forms_dict

    def print_LifeFormScanResult_dict(self):
        for biome, rarities in self.get_LifeFormScanResult_dict().items():
            print(biome)
            for rarity,life_forms in rarities.items():
                print(f"\t{rarity}")
                for life_form,vals in life_forms.items():
                    print(f"\t\t{life_form}")
                    for val in vals:
                        print(f"\t\t\t{val}")
        return

    def is_biosite_ready(self,biosite_coords:list[int])->bool:
        if biosite_coords is None:
            return False
        return journal.is_ready(biosite_coords[0],biosite_coords[1])

    def unload_cargo(self,unload_target_station_id=None):
        if self.drone.cargo.count() > 0:
            for item_id,amount in self.drone.cargo.contents().items():
                if unload_target_station_id:
                    self.travel_to_station(unload_target_station_id)
                    self.drone.cargo.unload(item_id,amount)
                else:
                    for biome, biome_plants in life_forms_dict.items():
                        if item_id in biome_plants:
                            self.travel_to_station(life_form_dock_name.get(biome))
                            self.drone.cargo.unload(item_id,amount)
        self.recharge()
        return

    def discard_cargo(self):
        for item_id,amount in self.drone.cargo.contents().items():
            self.drone.cargo.discard(item_id,amount)
        return

    def extract_entry(self,entry):
        if self.is_biosite_ready(entry.get("coord")):
            self.travel_to(
                entry.get("coord")[0],
                entry.get("coord")[1],
                bio_collect=True
                )
        if (
            self.is_biosite_ready(entry.get("coord"))
            and self.drone.get_distance_to(
                entry.get("coord")[0],
                entry.get("coord")[1]
            ) < 2
        ):
            self.drone.bio_extractor.extract()
        return

    def extract_life_form_entry(self,life_form,entry):
        
        if entry.get("remaining_tons") == 0:
            return
    
        while(
            self.is_biosite_ready(entry.get("coord"))
            and not life_form in self.drone.cargo.contents().keys()
        ):
            self.extract_entry(entry)
            if not life_form in self.drone.cargo.contents().keys():
                self.discard_cargo()
        return

    def collect_life_form(self,biome_name,rarity,life_form,life_forms_data=None,unload_target_station_id=None):
        
        if life_forms_data is None:
            life_forms_data = self.get_LifeFormScanResult_dict()
            
        entries = life_forms_data.get(biome_name,{}).get(rarity,{}).get(life_form,[])
        
        for entry in entries:
            self.extract_life_form_entry(life_form,entry)
            self.unload_cargo(unload_target_station_id)
        
        return

    def collect_biome_rarity(self,biome_name,rarity,life_forms_data=None,unload_target_station_id=None):
    
        if life_forms_data is None:
            life_forms_data = self.get_LifeFormScanResult_dict()
            
        for life_form in life_forms_data.get(biome_name,{}).get(rarity,{}).keys():
            self.collect_life_form(biome_name,rarity,life_form,life_forms_data,unload_target_station_id)
        
        return

    def collect_rare_biome(self,biome_name,life_forms_data=None,unload_target_station_id=None):
        self.collect_biome_rarity(biome_name,"rare",life_forms_data,unload_target_station_id)
        return

    def collect_rare_for_essence(self,life_forms_data=None):
    
        for biome_name in plant_biomes:
            if get_component(life_form_dock_name.get(biome_name)).output.count() > 100:
                if self.drone.cargo.count() > 0:
                    for item_id,amount in self.drone.cargo.contents().items():
                        self.drone.cargo.discard(item_id,amount)
                continue
            self.collect_rare_biome(biome_name,life_forms_data,None)
        return

    def task_collect_life_forms(self,biome_to_collect):
        self.recharge()
        life_forms_data = self.get_LifeFormScanResult_dict()
        self.collect_rare_for_essence(life_forms_data)
        
        for rarity in ("rare", "uncommon", "common"):
            for life_form_id, entries in self.get_LifeFormScanResult_dict().get(biome_to_collect, {}).get(rarity, {}).items():
                entry = next(
                    (entry for entry in entries if entry["remaining_tons"] > 0),
                    None,
                )
                if entry:
                    print(rarity, life_form_id, entry)
                    self.collect_life_form(biome_to_collect,rarity,life_form_id,unload_target_station_id="drone_station_lrg_2")
                    # self.unload_cargo("drone_station_lrg_2")







