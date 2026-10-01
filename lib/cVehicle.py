import cStorage as cSto
import cNavigation as cNav

THROTTLE = 0.5
NAV_DISTANCE_THRESHOLD = 1
CHARGE_BATTERY_THRESHOLD = 1
DISCHARGE_BATTERY_THRESHOLD = 0.2
TRAVEL_SLEEP_TIME = 1
RECHARGE_SLEEP_TIME = 1
ORDER_MINING_CHANNEL = "mining"
ORDER_CONSTRUCTION_CHANNEL = "construction"

comms = get_component("comms")

class cVehicle():
    vehicle:Rover|Pioneer

    base_modules: dict[int, str]
    mounted_setup: dict[int, dict[str, str | list[str]]]

    modules_internal = {
       "battery_holder_small": ["portable_battery"],
       "battery_holder_medium": ["portable_battery","portable_battery"],
       "battery_holder_large": ["portable_battery","portable_battery","portable_battery"],
       "cargo_rack_small": ["portable_bin"],
       "cargo_rack_medium": ["heavy_portable_bin","heavy_portable_bin"],
       "cargo_rack_large": ["heavy_portable_bin","heavy_portable_bin","heavy_portable_bin"]
    }
    
    nav_throttle:float = THROTTLE
    

    
    def __init__(self, vehicle:Rover|Pioneer):
        self.vehicle = vehicle
        self.mounted_setup = self.get_mounted()
        # self.mount_base_setup()
        
    def get_vehicle(self) -> Rover|Pioneer:
        return self.vehicle

    def status(self) -> str:
        return self.vehicle.status()
        
    def _nav_installed(self) -> bool:
        return hasattr(self.vehicle, "nav")
    
    def _sonar_installed(self) -> bool:
        return hasattr(self.vehicle, "sonar")
    
    def _drill_installed(self) -> bool:
        return hasattr(self.vehicle, "drill")
    
    def _battery_installed(self) -> bool:
        return hasattr(self.vehicle, "battery")
    
    def _cargo_installed(self) -> bool:
        return hasattr(self.vehicle, "cargo")

    def battery_below_threshold(self) ->bool:
        if not self._battery_installed():
            return True
        return self.vehicle.battery.level() < DISCHARGE_BATTERY_THRESHOLD
    
    def set_throttle(self,throttle:float=THROTTLE):
        self.nav_throttle = throttle
        return

    def get_throttle(self) -> float:
        return self.nav_throttle
        
    def move_to_position(self,x:int,y:int,throttle:float|None = None,ignore_battery:bool=False):
        
        if not self._nav_installed():
            return
            
        self.vehicle.nav.set_target(x,y)
        self.vehicle.nav.set_throttle(
            throttle if throttle else self.nav_throttle
        )
        while (
            self.vehicle.nav.get_distance_to(x, y) > NAV_DISTANCE_THRESHOLD
        ):
            if not ignore_battery and self.battery_below_threshold():
                self.vehicle.nav.brake()
                self.recharge()
                return
            sleep(TRAVEL_SLEEP_TIME)
        self.vehicle.nav.brake()
        
        return

    def move_to_PointOfInterest(self,target:PointOfInterest,ignore_battery:bool=False):
        if target:
            self.move_to_position(target.x,target.y,ignore_battery=ignore_battery)
        return
    
    def get_nearest_OutpostRef(self) -> OutpostRef:
        if self._nav_installed():
            o_net = get_component("outpost_network")
            pos_x,pos_y = self.vehicle.nav.get_position().__iter__()
            return o_net.nearest(pos_x,pos_y)
        return

    def recharge(self):
        self.move_to_PointOfInterest(self.get_nearest_OutpostRef(),ignore_battery=True)
        while self.vehicle.battery.level() < CHARGE_BATTERY_THRESHOLD:
            sleep(RECHARGE_SLEEP_TIME)
        return
    
    def scan(self):
        
        if not self._sonar_installed():
            return
            
        result = self.vehicle.sonar.scan()
        for site in result.sites:
            if not site.surveyed:
                self.vehicle.sonar.survey(site.id)
        return

    def scan_at_position(self,x,y):
        if not self._sonar_installed() or not self._nav_installed():
            return
        self.move_to_position(x,y)
        self.scan()
        return

    def scan_at_PointOfInterest(self,target:PointOfInterest):
        self.scan_at_position(target.x,target.y)
        return
    
    def mine(self):
        
        if not self._drill_installed() or not self._cargo_installed():
            return
        
        while (
            not self.vehicle.cargo.full()
            and not self.battery_below_threshold()
        ):
            if self.vehicle.drill.mine().status != "ok":
                break
        
        return

    def mine_at_position(self,x:int,y:int):
        
        if (
            not self._drill_installed() 
            or not self._nav_installed()
            or not self._cargo_installed()
        ):
            return
            
        self.move_to_position(x,y)
        self.mine()
        return

    def mine_at_PointOfInterest(self,target:PointOfInterest):
        if target:
            self.mine_at_position(target.x,target.y)
        return

    def mine_mineral(self,mineral_id:str):
            
        if (
            not self._drill_installed() 
            or not self._nav_installed()
            or not self._cargo_installed()
        ):
            return
        
        pos = self.vehicle.nav.get_position()
        mining_site = cNav.get_nearest_site_mineral(mineral_id,pos.x,pos.y)
        self.mine_at_PointOfInterest(mining_site)
        
        return
    
    def get_mining_order(self) -> str | None:
        for mineral_to_mine, vehicles in comms.latest(ORDER_MINING_CHANNEL).items():
            if self.vehicle.id in vehicles:
                return mineral_to_mine 
        return None
       
    def _input_connect(self,target_id:str) -> ActionResult:
        return self.vehicle.input.connect(target_id)

    def _input_take_item(self,item_id:str,count:int):
        if self.vehicle.input.connected_to() == "":
            return
        while self.vehicle.input.take(item_id,count).status == "busy":
            continue
        return
    
    def _output_connect(self,target_id:str) -> ActionResult:
        if target_id:
            return self.vehicle.output.connect(target_id)
        return self.vehicle.output.connect("inventory")
    
    def _output_sent_item(self,item_id:str,count:int):
        if self.vehicle.output.connected_to() == "":
            return
        while self.vehicle.output.send(item_id,count).status == "busy":
            continue
        return
        
    def _output_sent_item_target(self,item_id:str,count:int,target_id:str):
        if self.vehicle.output.connected_to() != target_id:
            self._output_connect(target_id)
            
        while (result:=self.vehicle.output.send(item_id,count)).status == "busy":
            continue
        return

    def output_sent_item_to_warehouse(self,item_id:str,count:int,warehouse:Warehouse):
                
        if not self._cargo_installed() or not self._nav_installed():
            return

        self.move_to_PointOfInterest(warehouse.outpost)
        self._output_connect(warehouse.id)
        self._output_sent_item(item_id,count)
        
        return
    
    def input_take_item_from_warehouse(self,item_id:str,count:int,warehouse:Warehouse):
                
        if(
            warehouse is None
            or not self._cargo_installed()
            or not self._nav_installed()
        ):
            return

        self.move_to_PointOfInterest(warehouse.outpost)
        self._input_connect(warehouse.id)
        self._input_take_item(item_id,count)
        
        return

    def cargo_get_items(self) -> dict[str,int]:

        items = {}

        for itemStack in self.vehicle.cargo.stacks():
            items[itemStack.id] = items.get(itemStack.id, 0) + itemStack.count
    
        return items

    def cargo_import_item(self,item_id:str,amount:int):
        storage = self.get_nearest_warehouse_with_item(item_id)
        self.input_take_item_from_warehouse(item_id,amount,storage)
        return
        
    def get_nearest_warehouse_with_item(self,item_id) -> Warehouse:
        
        if not self._cargo_installed() or not self._nav_installed():
            return

        pos = self.vehicle.nav.get_position()
        return cSto.get_nearest_warehouse_with_item(item_id,pos.x,pos.y)
        
    def dispose_item_to_nearest_warehouse(self,item_id):

        warehouse = self.get_nearest_warehouse_with_item(item_id)
        
        if warehouse is None:
            return

        to_send = min(
            self.cargo_get_items().get(item_id),
            warehouse.space_for(item_id)
                     )
        
        self.output_sent_item_to_warehouse(item_id,to_send,warehouse)
        
        return

    def dispose_cargo_to_warehouses(self):

        if not self._cargo_installed() or not self._nav_installed():
            return

        for item_id,count in self.cargo_get_items().items():
            warehouse = self.get_nearest_warehouse_with_item(item_id)
            
            if warehouse is None:
                break
    
            to_send = min(count,warehouse.space_for(item_id))
            self.output_sent_item_to_warehouse(item_id,to_send,warehouse)
        
        return

    def dispose_minerals(self,outpost_id:str):
        minerals = self.cargo_get_items()

        for mineral_id, count in minerals.items():
            self.output_sent_item_to_warehouse(
                mineral_id,
                count,
                cSto.get_warehouse_mineral_outpost(mineral_id,outpost_id)
            )
        return

    def _buy_module(self,module_name:str,quantity:int=1):
        shop = get_component("shop")
        shop.buy(module_name,quantity)
        return

    def unmount_module(self,index:int):
            
        while (mount_status := self.vehicle.unmount(index).status) == "holder_not_empty":
            for internal_idx in range(
                len(
                    self.mounted_setup.get(index,{}).get("internal_items",[])
                )
            ):
                if self.vehicle.uninstall(index, internal_idx).status == "slot_empty":
                    continue
        return
    
    def mount_module(self,index:int,module_name:str):
        if self.mounted_setup.get(index,{}).get("module_id","") == module_name:
            return
        self.move_to_position(0,0)
        inv = get_component("inventory")
        if inv.count(module_name) == 0:
            self._buy_module(module_name)
        while (mount_status := self.vehicle.mount(index,module_name).status) != "ok":
            if mount_status == "item_not_in_inventory":
                self._buy_module(module_name)
            self.unmount_module(index)
        self.mounted_setup = self.get_mounted()
        
    def mount_module_internal(self,index:int,internal_index:int,module_name:str):
        inv = get_component("inventory")
        if inv.count(module_name) == 0:
            self._buy_module(module_name)

        
        while (install_status := self.vehicle.install(index, internal_index, module_name).status) != "ok":
            if install_status != "internal_slot_occupied":
                break
        
            self.vehicle.uninstall(index, internal_index)
            
        self.mounted_setup = self.get_mounted()

    def mount_base_setup(self):
        if not all(
            self.modules_match(
                self.base_modules,
                self.modules_internal
            )
        ):
            self.move_to_position(0,0)
            for module_slot, module_id in self.base_modules.items():
                if self.mounted_setup.get(module_slot).get("module_id",None) != module_id:
                    self.mount_module(module_slot, module_id)
                
                for internal_slot, internal_id in enumerate(self.modules_internal.get(module_id,[])):
                    if self.mounted_setup.get(module_slot).get('internal_items')[internal_slot] != internal_id:
                        self.mount_module_internal(module_slot,internal_slot,internal_id)
                        
        return

    def get_mounted(self) -> dict[int, dict[str, str | list[str]]]:
        return {
            module.index: {
                "module_id": module.module_id,
                "internal_items": module.internal_items,
            }
            for module in self.vehicle.modules()
        }

    def modules_match(self,
                      wanted_modules: dict[int, str],
                      wanted_internal: dict[str, list[str]],
                     ) -> dict[int, bool]:
        result = {}
        
        for index, module_id in wanted_modules.items():
            module = self.mounted_setup.get(index)

            if module is None:
                result[index] = False
            else:
                actual_items = [
                    item
                    for item in (module.get("internal_items") or [])
                    if item is not None
                ]
    
                wanted_items = wanted_internal.get(module_id) or []
    
                result[index] = (
                    module.get("module_id") == module_id
                    and sorted(actual_items) == sorted(wanted_items)
                )

        return result

        
    
    def startup(self):
        self.mount_base_setup()
        self.dispose_cargo_to_warehouses()
        self.recharge()

    def task_mine(self):
        mineral_id = self.get_mining_order()
        if mineral_id:
            self.mine_mineral(mineral_id)
            self.dispose_minerals("outpost_home")
        self.recharge()

