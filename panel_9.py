import cStorage as Cstor


notebook = get_component("notebook")
nocturna = get_component("nocturna")
journal = get_component("journal")
outpost_network = get_component("outpost_network")
clock = get_component("clock")

WAREHOUSES_MINERALS:list[str] = [
    "large_warehouse_1",
]

WAREHOUSES_MATERIALS:list[str] = [
    "large_warehouse_2",
]

WAREHOUSES_PRODUCTS:list[str] = [
    "large_warehouse_3",
    "large_warehouse_4",
    "large_warehouse_5",
    "large_warehouse_6",
]

WAREHOUSES_REAGENTS:list[str] = [
    "large_warehouse_7",
]
WAREHOUSES_LIFE_FORMS:list[str] = [
    "large_warehouse_7",
    "large_warehouse_8",
    "large_warehouse_9",
]

STORAGE_BINS_MINERALS:list[Warehouse] = [
    # get_component("storage_bin_2"),
    # get_component("storage_bin_3"),
]

STORAGE_BINS_MATERIALS:list[Warehouse] = [
    # get_component("storage_bin_1"),
    # get_component("storage_bin_6")
]

STORAGE_BINS_PRODUCTS:list[Warehouse] = [
    # get_component("storage_bin_4"),
    # get_component("storage_bin_5")
]

constants = {

}

smelter = {
    "MINERAL_THRESHOLD": 100,
    "PRODUCT_MAX": 1500,
    "SMELT_BATCH": 10
}

storage_warehouses = {
    "WAREHOUSES_MINERALS":WAREHOUSES_MINERALS,
    "WAREHOUSES_MATERIALS":WAREHOUSES_MATERIALS,
    "WAREHOUSES_PRODUCTS":WAREHOUSES_PRODUCTS,
    "WAREHOUSES_REAGENTS":WAREHOUSES_REAGENTS,
    "WAREHOUSES_LIFE_FORMS":WAREHOUSES_LIFE_FORMS,
}

mining_drill={
    "iron_ore": ["mining_drill_heavy_4",(30,30)],
    "silicon": ["mining_drill_heavy_5",(-70,-150)],
    "titanium": ["mining_drill_heavy_7",(-140,250)],
    "cobalt": ["mining_drill_heavy_6",(240,-60)],
    "rare_earth": ["mining_drill_heavy_1",(100,560)],
    "neutronium": ["mining_drill_heavy_3",(750,-80)],
    "lead_ore": ["mining_drill_heavy_2",(-510,270)],
}


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




def create_items_watehouse_dict() -> dict[str,[str,int]]:
    
    material_warehouses = {}
    
    for warehouse_ids in storage_warehouses.values():
        for warehouse_id in warehouse_ids:
            warehouse: Warehouse = get_component(warehouse_id)
    
            for item_id in warehouse.materials():
                material_warehouses.setdefault(item_id, []).append(
                    (warehouse_id, warehouse.count(item_id))
                )
    return material_warehouses

while True:
    written = notebook.set("lifeform.biomes.items_id", life_forms_dict)
    if written.status != "ok":
        print(written.message)
    
    written = notebook.set("lifeform.biomes.drone_station", life_form_dock_name)
    if written.status != "ok":
        print(written.message)
    
    written = notebook.set("constants.smelter", smelter)
    if written.status != "ok":
        print(written.message)
    
    written = notebook.set("storage.warehouses", storage_warehouses)
    if written.status != "ok":
        print(written.message)
    
    written = notebook.set("storage.outpost_home.items", create_items_watehouse_dict())
    if written.status != "ok":
        print(written.message)
    
    written = notebook.set("mining_drill.mineral", mining_drill)
    if written.status != "ok":
        print(written.message)
    
    sleep(clock.real_seconds_per_hour()/4)
    



































