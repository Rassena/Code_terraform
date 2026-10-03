import cStorage as cStor


inv = get_component("inventory")
shop = get_component("shop")

drone_station = get_component(self.id)
wh = get_component("warehouse_7")

drone_transporter = get_component("drone_1")

REAGENTS_BUFFER = 40
REAGENTS_MAX = 100

self.input.connect(inv.id)
# self.output.connect(inv.id)

REAGENTS_ID = [
    "alkaline_buffer",
    "cryo_solvent",
    "protein_marker",
    "chelating_agent",
    "enzyme_solution",
]
outpost_id = "outpost_2"


def get_stack() -> dict[str,int]:
    result = {}

    for stack in self.output.stacks():
        result[stack.id] = result.get(stack.id,0) + stack.count
    return result


print(wh.materials())


print(drone_transporter.status())


accept_mineral = [
    "neutronium"
]

while True:
    for reagent_id in REAGENTS_ID:
        in_storage = wh.count(reagent_id)
        if in_storage<REAGENTS_MAX:
            in_inventory = inv.count(reagent_id)
            in_station = get_stack().get(reagent_id,0)
            to_buy = REAGENTS_BUFFER - (in_inventory+in_station)
            print(reagent_id)
            print("\tstation",in_station)
            print("\tinv",in_inventory)
            print("\tbuy",to_buy)
            if to_buy > 0:
                shop.buy(reagent_id,to_buy)
    
    for reagent_id in REAGENTS_ID:
        in_dock = get_stack().get(reagent_id,0)
        if inv.count(reagent_id) > 0:
            self.input.take(reagent_id,min(inv.count(reagent_id),REAGENTS_BUFFER-in_dock))

    for mineral_id in accept_mineral:
        in_dock = get_stack().get(mineral_id,0)
        mineral_whs = cStor.get_warehouses_with_item_and_space(self.outpost.id)
        mineral_wh = next(mineral_whs,None)
        if mineral_wh is None:
            mineral_whs = cStor.get_warehouses_minerals_outpost(self.outpost.id)
            for mineral_wh in mineral_whs:
                if mineral_wh.space_for(mineral_id) < 0:
                    break
            self.output.connect(mineral_wh.id)
    
            free_space = mineral_wh.space_for(mineral_id)
            while self.output.send(mineral_id,min(in_dock,free_space)).status != "busy":
                pass

            
        
    sleep(10)


    