import cStorage as cStor
import cConstructionBlueprint as cBlue

TEXT_SIZE = 11

LABEL_MARGIN_X = 10
LABEL_MARGIN_Y = 20

NAME_MARGIN = 10
STATUS_MARGIN = 120

Y_ROW = 50
INLINE_SPACE=20

STORAGE_MAX = 1500

clock = get_component("clock")
comms = get_component("comms")
OUTPOST_ID = "outpost_home"


def get_vehicles() -> dict[str:list[str]]:
    vehicles = {}
    
    for vehicle in get_component("fleet").vehicles():
        vehicles.setdefault(vehicle.kind, []).append(vehicle.id)
    
    return vehicles

def split_mineral_mine() -> dict[str, list[str]]:
    
    # print(get_nearest_site_mineral("iron_ore"))
    # print(get_nearest_site_mineral("silicon"))
    # print(get_nearest_site_mineral("titanium"))
    # print(get_nearest_site_mineral("cobalt"))
    # print(get_nearest_site_mineral("rare_earth"))
    # print(get_nearest_site_mineral("neutronium"))
    # print(get_nearest_site_mineral("lead_ore"))
        
    rovers,pioneers = get_vehicles().values()
    weights = set_mineral_weight(cStor.get_items_warehouses_minerals_outpost(OUTPOST_ID))


    pioneers = pioneers[4:]
    
    pioneer_ignore_mineral = [
        # "iron_ore",
        # "silicon",
        # "titanium",
        # "cobalt",
        "lead_ore",
        # "rare_earth"
    ]

    rover_total_weight = (weights.iron_ore + weights.silicon) or 1
    rover_iron_end = floor(rovers.length * weights["iron_ore"] / rover_total_weight)
    rover_silicon_end = None if weights["silicon"] else rover_iron_end

    for mineral_id in pioneer_ignore_mineral:
        weights[mineral_id] = 0
        
    pioneer_total_weight = sum(weights.values()) or 1
    pioneer_iron_end = floor(pioneers.length * weights["iron_ore"] / pioneer_total_weight)
    pioneer_silicon_end = pioneer_iron_end + floor(pioneers.length * weights["silicon"] / pioneer_total_weight)
    pioneer_titanium_end = pioneer_silicon_end + floor(pioneers.length * weights["titanium"] / pioneer_total_weight)
    pioneer_cobalt_end = pioneer_titanium_end + floor(pioneers.length * weights["cobalt"] / pioneer_total_weight)
    pioneer_lead_ore_end = pioneer_cobalt_end + floor(pioneers.length * weights["lead_ore"] / pioneer_total_weight)
    pioneer_rare_earth_end = None if weights["rare_earth"] else pioneer_lead_ore_end

    # print(
    #     pioneers.length * weights["iron_ore"],
    #     pioneer_total_weight,
    #     rover_total_weight,
    #     pioneer_total_weight,
    #     pioneer_iron_end,
    #     pioneer_silicon_end,
    #     pioneer_titanium_end,
    #     pioneer_cobalt_end,
    #     pioneer_lead_ore_end,
    #     pioneer_rare_earth_end
    # )
    
    result = {
        "iron_ore": rovers[:rover_iron_end]+ pioneers[:pioneer_iron_end],
        "silicon": rovers[rover_iron_end:rover_silicon_end] + pioneers[pioneer_iron_end:pioneer_silicon_end],
        "titanium": pioneers[pioneer_silicon_end:pioneer_titanium_end],
        "cobalt": pioneers[pioneer_titanium_end:pioneer_cobalt_end],
        "lead_ore": pioneers[pioneer_cobalt_end:pioneer_lead_ore_end],
        "rare_earth": pioneers[pioneer_lead_ore_end:pioneer_rare_earth_end],
    }

    # print(result)
    return result

def set_mineral_weight(storage:dict[str:int]):
    result_weight = {
        "iron_ore": 1,
        "silicon": 1,
        "titanium": 1,
        "cobalt": 1,
        "lead_ore": 1,
        "rare_earth": 1
    }
    for mineral,_ in result_weight.items():
        if storage.get(mineral,0) < STORAGE_MAX:
            result_weight[mineral] = 1
        else:
            result_weight[mineral] = 0
    # print(result_weight)
    return result_weight

def order_get_mineral():
    mining_orders = split_mineral_mine()
    comms.broadcast("mining",mining_orders)
    return

while True:

    panel.clear()
    panel.label(LABEL_MARGIN_X, LABEL_MARGIN_Y, f"Tasks Vehicle", "caption")

    order_get_mineral()
    
    # if clock.get_time()[1] == 0:
    #     order_contruct()
    
    for i, (mineral_id, vehicles) in enumerate((comms.latest("mining").items())):
        x = NAME_MARGIN
        y = Y_ROW + i * INLINE_SPACE
        
        panel.draw_text(x, y, f"Mine {mineral_id}", TEXT_SIZE)
        panel.draw_text(x + STATUS_MARGIN, y, str(len(vehicles)), TEXT_SIZE)
    
    sleep(clock.real_seconds_per_hour())













        