from cPioneer import cPioneer
import cConstructionBlueprint as cConB
import cStorage as cStor
import cNavigation as cNav

dict_mining = {
    "iron_ore": "iron_ore",
    "silicon": "silicon",
    "titanium": "titanium",
    "cobalt": "cobalt",
    "rare_earth": "rare_earth",
    "neutronium": "neutronium",
    "lead_ore": "lead_ore",
}

# cConB.construction_blueprint.plan_power_line(-600,0,-600,300)
# cConB.construction_blueprint.plan_pipe("steam",-600,0,-600,300)
# cConB.construction_blueprint.plan_pipe("water",-600,0,-600,300)

self = cPioneer(self)
self.dispose_cargo_to_warehouses()


# self.output_sent_item_to_warehouse("lead_ore",1,get_component("warehouse_5"))

cConB.construction_blueprint.plan_power_line(0,500,50,500)
# cConB.construction_blueprint.plan_power_line(0,0,-600,0)
# cConB.construction_blueprint.plan_pipe("oil",10,560,10,460)
# cConB.construction_blueprint.plan_pipe("water",0,-500,-450,-500)
# cConB.construction_blueprint.plan_pipe("water",-450,-500,-450,-450)


    # self.recharge()
    # self.vehicle.input.connect("inventory")
    # self.vehicle.input.take("outpost_kit",1)
    # self.move_to_position(0,-500)
    # self.constructor_execute("outpost_blueprint_6",0,-500)


    # build_flee = [pioneer.id for pioneer in get_component("fleet").vehicles() if pioneer.kind == "pioneer"]
    # to_build = cConB.construction_blueprint.pending_constructions()
    # part_lenght = ceil(to_build.length/build_flee.length)
    # start = build_flee.index(self.vehicle.id) * part_lenght
    # end = start + part_lenght
    # my_part = to_build[max(0,start):min(end,to_build.length-1)]
 


REAGENT_THRESHOLD = 200
REAGENT_BUFFER = 50

def task_simple_scan_world():

    # scan_flee = [pioneer.id for pioneer in get_component("fleet").vehicles() if pioneer.kind == "pioneer"]
    scan_flee = [
        "pioneer_1",
        "pioneer_2",
        "pioneer_3",
        "pioneer_4"
        ]
       
    to_scan = cNav.generate_positions_to_scan(-500,500,-500,500,500)

    part_lenght = ceil(to_scan.length/scan_flee.length)
    start = scan_flee.index(self.vehicle.id) * part_lenght
    end = start + part_lenght
    my_part = to_scan[max(0,start):min(end,to_scan.length-1)]
 
    while my_part:
        if self.battery_below_threshold():
            self.recharge()
        position = next(my_part,None)
        self.scan_at_position(position[0],position[1])

    self.move_to_position(0,0)

    
    pass

def get_reagent(reagent_id:str,amount:int=1):

    inv = get_component("inventory")
    shop = get_component("shop")
    
    available_inv = inv.count(reagent_id)
    available_cargo = self.cargo_get_items().get(reagent_id,0)
    available = available_cargo + available_inv
    
    possible_cargo = self.vehicle.cargo.capacity()
    
    if(
        amount < available_cargo
    ):
        self.move_to_position(0,0)

    
    if (
        available<amount
        and amount-available > 0
    ):
        shop.buy(reagent_id,amount-available)

    self._input_connect("inventory")
    self._input_take_item(reagent_id,min(amount,possible_cargo))
    
    pass
    
def get_reagent_outpost(reagent_id:str,outpost_id:str,amount:int=REAGENT_THRESHOLD):

    get_reagent(reagent_id,amount)

    warehouse = cStor.get_warehouse_reagent_outpost(reagent_id,outpost_id)
    
    self.output_sent_item_to_warehouse(reagent_id,amount,warehouse)
    
    pass

def main():    

    scan_flee = [
        # "pioneer_1",
        "pioneer_2",
        "pioneer_3",
        "pioneer_4",
        ]

    # reagents_id = [
    #     # "alkaline_buffer",
    #     "cryo_solvent",
    #     "protein_marker",
    #     # "chelating_agent",
    #     # "enzyme_solution",
    # ]
    # outpost_id = "outpost_2"

    self.mount_base_setup()
    # self.recharge()
    self.dispose_cargo_to_warehouses()
    
    # while True:
    #     for reagent_id in reagents_id:
    #         self.recharge()            
    #         warehouse = cStor.get_warehouse_reagent_outpost(reagent_id,outpost_id)
            
    #         if warehouse.count(reagent_id)<REAGENT_BUFFER:
    #             get_reagent_outpost(reagent_id,outpost_id,REAGENT_THRESHOLD)

    
    
    # self.mount_module(2,"constructor_module")

    while True:
        self.dispose_cargo_to_warehouses()
        if self.vehicle.id in scan_flee:
            self.mount_module(1,"sonar_module_deep")
            task_simple_scan_world()
        elif self.get_mining_order():
            self.dispose_minerals("outpost_home")
            self.mount_module(2,"drill_module_industrial")
            self.task_mine()
        else:
            self.mount_module(2,"constructor_module")
            self.task_construction(None,None)
            self.recharge()
            pass
        pass

    # shop = get_component("shop")



main()





















    