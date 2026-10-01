from cVehicle import cVehicle
import cConstructionBlueprint as cConstr
import cStorage as cStor

construction_blueprint = get_component("construction_blueprint")

dict_mining = {
    "iron_ore": "iron_ore",
    "silicon": "silicon",
    "titanium": "titanium",
    "cobalt": "cobalt",
    "rare_earth": "rare_earth",
    "neutronium": "neutronium",
    "lead_ore": "lead_ore",
    }

class cPioneer(cVehicle):
    vehicle:Pioneer
    
    base_modules = {
        0: "nav_module",   
        1: "sonar_module_wide",   
        # 2: "drill_module_industrial",  
        3: "cargo_rack_large",   
        4: "battery_holder_large",   
        5: "battery_holder_large",   
        6: "battery_holder_large",   
        7: "battery_holder_large",   
    }
    
    def get_pioneer(self) -> Pioneer:
        return self.vehicle

    def _constructor_installed(self) -> bool:
        return hasattr(self.vehicle, "constructor")

    def constructor_execute(self,blueprint_id:str,x:int,y:int):
        self.move_to_position(x,y)
        self.vehicle.constructor.execute(blueprint_id)
        return

    def get_nearest_construction_with_item(self,required_item:str,list_contructions:list[Construction]=None) -> Construction:
        
        if not self._cargo_installed() or not self._nav_installed():
            return

        pos = self.vehicle.nav.get_position()
        return cConstr.get_nearest_construction_by_required_item(required_item,pos.x,pos.y)
    
    def task_construction(self,list_contructions:list[Construction]=None,overwrite_required_item_id:str = None):
        
        if not self._constructor_installed():
            self.mount_module(2,"constructor_module")

        for  required_item, required_amount in cConstr.get_required_items(list_contructions).items():

            if(
                # required_item == "outpost_kit"
                # or (
                (
                    overwrite_required_item_id is not None
                    and required_item != overwrite_required_item_id
                )
            ):
                continue
        
            if self.cargo_get_items().get(required_item,0) < required_amount:
                self.cargo_import_item(required_item,required_amount)
    
            while(
                not self.battery_below_threshold()
                and (required_item in self.cargo_get_items().keys() or required_item is None)
            ):
                next_construction = self.get_nearest_construction_with_item(required_item,list_contructions)
                
                if not next_construction:
                    break

                
                self.constructor_execute(next_construction.id,next_construction.position.x,next_construction.position.y)
         
            



    
    # def claim_next_scan_position(self) -> dict[str:int]:
    #     note = get_component("notebook")

    #     positions_to_scan:list[dict[str:int]] = note.get("positions_to_scan")
    #     claimed = positions_to_scan.pop(0)
    #     note.set("positions_to_scan",positions_to_scan)
        
    #     positions_claimed:list[dict[str:int]] = note.get("positions_claimed")
    #     positions_claimed.append(claimed)
    #     note.set("positions_claimed",positions_claimed)
        
    #     return claimed
    
    
    # def add_to_scanned(self,scanned:dict[str:int]):
    #     note = get_component("notebook")

    #     positions_claimed:list[dict[str:int]] = note.get("positions_claimed")
    #     positions_claimed.remove(scanned)
    #     note.set("positions_claimed",positions_claimed)
        
    #     positions_scanned:list[dict[str:int]] = note.get("positions_scanned")
    #     positions_scanned.append(scanned)
    #     note.set("positions_scanned",positions_scanned)
        
    #     return
    
    # def scan_claimed_position(self,claimed:dict[str,int]):
    #     self.scan_at(**claimed)
    #     self.add_to_scanned(claimed)
    #     return

    # def scan_next_position(self):
    #     self.scan_claimed_position(self.claim_next_scan_position())


# bound = get_component("nocturna").get_bounds()
# print(get_component("item_catalog").lookup("iron_ore"))

# for x in range(150,bound.max_x+1,150):
#     for y in range(150,bound.max_y+1,150):
#         if get_component("nocturna").contains(-x,-y):
#             if self.battery.level()<0.3:
#                 recharge()
#             scan_at(-x,-y)
# recharge()

# def build_power_line():
#     empty_cargo()

#     def get_power_line():
#         move_to_position(0,0)
#         self.input.connect("warehouse_2")
#         self.input.take(
#             "power_line_segment",
#             min
#             (
#                 self.cargo.capacity(),
#                 get_component("warehouse_2").count("power_line_segment")
#             )
#         )
        
#     constr = get_component("construction_blueprint")
#     power_line_blueprints = [blueprint for blueprint in constr.pending_constructions() if blueprint.required_item == "power_line_segment"]
    
#     while power_line_blueprints.length > 0:
#         if self.battery.level()<0.2:
#             recharge()
#         if self.cargo.count()==0:
#             get_power_line()
#         build = power_line_blueprints.pop(0)
#         move_to_position(build.position.x,build.position.y)
#         self.constructor.execute(build.id)
#     return






    