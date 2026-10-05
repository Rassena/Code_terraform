scanner = get_component("scanner_1")
seed_maker = get_component("seed_maker_1")
inventory = get_component("inventory")
seed_storage = get_component("large_warehouse_10")

HEAT_BUFFER = 10
BATCH = 10
SEEDS_IN_INVENTORY_MAX = 20

def heat_management():
    while  self.get_heat() >= self.get_max_heat() - HEAT_BUFFER:
        sleep(get_component("clock").real_seconds_per_hour() * 1)

def get_not_empty():
    result = scanner.get_scanned()
    for key, item in result.items():
        if item.status == "empty":
            result.pop(key)
    return result
        
def get_not_scanned() -> dict[str,ScanResult]:
    result = scanner.get_scanned()
    for key, item in result.items():
        if item.status == "ok":
            result.pop(key)
    return result
        
def get_next_not_empty(scanned):
    key, item = scanned.popitem()
    while item.status == "empty" and scanned.length>0:
        key, item = scanned.popitem()
    return key, item

def move_to_next():
    scanned = scanner.get_scanned()
    key, item = get_next_not_empty(scanned)
    target_x = key[0]
    target_y = key[1:]
    
    print("Move Next:", target_x,target_y)
    move_to(target_x, target_y)

def move_to_nearest_item():
    key, item = get_nearest_item()

    target_x = key[0]
    target_y = key[1:]
    if key == self.get_position():
        print("Already at:",key)
    else:
        print("Move nearest:", key)
        move_to(target_x, target_y)

def move_to_nearest_not_scanned():
    key, item = get_nearest_not_scanned()

    target_x = key[0]
    target_y = key[1:]
    if key == self.get_position():
        print("Already at:",key)
    else:
        print("Move nearest:", key)
        move_to(target_x, target_y)

def move_to_cell(cell):
    move_to(cell[0],cell[1:])
    
def move_to(target_x, target_y):
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]
    
    while current_x != target_x:
        heat_management()
        if ord(current_x) < ord(target_x):
            self.move(str(chr(ord(current_x)+1)+current_y))
        else:
            self.move(str(chr(ord(current_x)-1)+current_y))
        current_x = self.get_position()[0]
        current_y = self.get_position()[1:]

    while current_y != target_y:
        heat_management()
        if int(current_y) < int(target_y):
            self.move(current_x+str(int(current_y)+1))
        else:
            self.move(current_x+str(int(current_y)-1))
        current_x = self.get_position()[0]
        current_y = self.get_position()[1:]
    pass
    
def get_nearest_item():
    scanned = get_not_empty()
    
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]

    nearest = inf
    nearest_key:str
    nearest_item:ScanResult
    
    while scanned.length > 0 :
        key, item = get_next_not_empty(scanned)
        target_x = key[0]
        target_y = key[1:]

        dist = abs(ord(target_x) - ord(current_x)) + abs(int(target_y)-int(current_y))
    
        if dist < nearest:
            nearest=dist
            nearest_key=key
            nearest_item=item

    return nearest_key, nearest_item

def get_nearest_cell(cells):
    
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]

    nearest_distance = inf
    nearest_cell:str
    
    for cell in cells:
        target_x = cell[0]
        target_y = cell[1:]

        dist = abs(ord(target_x) - ord(current_x)) + abs(int(target_y)-int(current_y))
    
        if dist < nearest_distance:
            nearest_distance=dist
            nearest_cell=cell
            
    return nearest_cell

def get_nearest_not_scanned():
    not_scanned = get_not_scanned()
    
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]

    nearest = inf
    nearest_key:str
    nearest_item:ScanResult
    
    while not_scanned.length > 0 :
        key, item = get_next_not_empty(not_scanned)
        target_x = key[0]
        target_y = key[1:]

        dist = abs(ord(target_x) - ord(current_x)) + abs(int(target_y)-int(current_y))
    
        if dist < nearest:
            nearest=dist
            nearest_key=key
            nearest_item=item

    return nearest_key, nearest_item

# while True:
        
#     heat_management()
    
#     # if(get_not_scanned().length > 0):
#     #     move_to_nearest_not_scanned()
#     if(get_not_empty().length > 0):
#         move_to_nearest_item()
#         self.collect()
#         self.store()


# print(self.cells())

seed_packfern_cells = [
    f"{y}{x}"
    for x in range(12,15)
    for y in ["D","E","F"]
    if f"{y}{x}" != "E13"
]
crowncap_add_1 = [
    f"{y}{x}"
    for x in range(1,10)
    for y in ["A", "B", "C", "D", "E", "F", "G", "H"]
    if f"{y}{x}" not in  [
        "C3","F3",
        "C8","F8",
        "C13","F13",
        "C18","F18",
        "C23","F23",
    ]
]

crowncap_add_2 = [
    f"{y}{x}"
    for x in range(18,25)
    for y in ["A", "B", "C", "D", "E", "F", "G", "H"]
    if f"{y}{x}" not in  [
        "C3","F3",
        "C8","F8",
        "C13","F13",
        "C18","F18",
        "C23","F23",
    ]
]

cells_plant_dict = {
    "seed_packfern":["C11","C12","D11","D12"],
    "seed_shadeleaf": ["D13","E14","F13"],
    "seed_crowncap":
    [
        "A11", "B11",
        "B12", "A12",
        "A13", "B13",
        "B14", "A14",
        "A15", "B15",
        "C15", "D15",
        "D14", "C14"
    ]+crowncap_add_1+crowncap_add_2,
    "seed_dewmoss": ["E17"],
    "seed_lonethorn": ["G11"],
    "seed_brinethorn": ["H12"],
    "seed_saltbloom": ["F12","E12"],
    "seed_saltmate": ["E11"],
    "seed_spitebud": ["H10","H16"],
    "seed_sunspur": ["H14"],
    "seed_sunpetal": ["G13"],
    "seed_grandbloom":["F14","G15"],
    "seed_twinvine": ["F17"],
    "seed_glowvine": ["E15","F16"],
    "seed_pondmoss": ["C16","D16","D17"],
}

cells_deploys_dict = {
    "sprinkler_kit": ["E16","G14"],
    "grow_lamp_kit": ["H13","F15"],
    "dispenser_kit": ["G12","F11"],
    "crop_automator_kit": [
        "C3","F3",
        "C8","F8",
        "C13","F13",
        "C18","F18",
        "C23","F23",
    ]
}

deploy_kits_type = {
    "sprinkler_kit": "sprinkler",
    "grow_lamp_kit": "grow_lamp",
    "dispenser_kit": "dispenser",
    "crop_automator_kit": "crop_automator",
}


needs_light = [
    "seed_sunspur",
    "seed_sunpetal",
    # "seed_glowvine"
]
needs_water = [
    "seed_dewmoss",
    # "seed_glowvine"
]


for recipe in seed_maker.recipes():
    print(recipe.seed_id,recipe.requirements,recipe.base_yield,recipe.growth_time)

def test():
    self.load_seed("seed_saltmate")
    self.deploy("crop_automator_kit")


def deploy_kits():
    for kit,cells in cells_deploys_dict.items():
        harvesting_machines = get_component("outpost_home").harvesting_machines(deploy_kits_type.get(kit))
        for cell in cells:
            correct_kit = False
            if self.cell(cell).status == "provider":
                for harvesting_machine in harvesting_machines:
                    if (
                        harvesting_machine.position == cell
                        and harvesting_machine.type_id == deploy_kits_type.get(kit)
                    ):
                        correct_kit =True
                        continue
            if correct_kit:
                continue
                
            move_to_cell(cell)
            if self.cell(cell).plant:
                if self.cell(cell).status == "mature":
                    self.harvest()
                else:
                    self.uproot()
            self.deploy(kit)
    return

    
def manage_inventory():
    for seed_id in get_seeds_id():
        amount_in_inventory = inventory.count(seed_id)
        amount_in_seed_storage = seed_storage.count(seed_id)
        if (
            amount_in_inventory < SEEDS_IN_INVENTORY_MAX
            and amount_in_seed_storage > 0
        ):
            while (
                (
                    result:= seed_storage.transfer_to(
                        "inventory",
                        seed_id,
                        min(
                            BATCH,
                            SEEDS_IN_INVENTORY_MAX - amount_in_inventory,
                            amount_in_seed_storage
                        )
                    ).status) == "busy"
            ):
                pass
        elif (
            amount_in_inventory > SEEDS_IN_INVENTORY_MAX
        ):
            while (
                (
                    result:= inventory.transfer_to(
                        seed_storage.id,
                        seed_id,
                        min(
                            BATCH,
                            amount_in_inventory-SEEDS_IN_INVENTORY_MAX,
                        )
                    ).status) == "busy"
            ):
                pass
    return

def get_seeds_id()-> list[str]:
    return [recipe.seed_id for recipe in seed_maker.recipes()]




# print(self.deployables())

# print(get_seeds_id())

def check_needs():
    
    check_plants = needs_light+needs_water
    check_cells = []
    
    for check_plant in check_plants:
        check_cells += cells_plant_dict.get(check_plant) 
        
    pass

def plant_seed(seed_id):
    if seed_id is None:
        return
    cells_to_plant = [
        cell
        for cell in cells_plant_dict.get(seed_id,[])
        if (
            self.cell(cell).plant != seed_id.removeprefix("seed_")
        )
    ]
    
    # print(cells_to_plant)
    # nearest_cell = get_nearest_cell(cells_to_plant)
    
    for cell in cells_to_plant:
        if self.get_held():
            self.store()
        if inventory.count(seed_id) >0:
            move_to_cell(cell)
            if self.cell(cell).status == "mature":
                self.harvest()
            else:
                self.uproot()
            if self.cell(cell).status == "provider":
                self.undeploy()
            self.load_seed(seed_id)
            self.plant(self.get_held())
            # if seed_id in needs_light:
            #     self.light()
            # if seed_id in needs_water:
            #     self.water()
    return
    
def harvest_seed(seed_id):
    if seed_id is None:
        return
    cells_to_harvest = [
        cell
        for cell in cells_plant_dict.get(seed_id,[])
        if self.cell(cell).status == "mature"
    ]
    print(cells_to_harvest)

    for cell in cells_to_harvest:
        move_to_cell(cell)
        self.harvest()
        if (holding:=self.get_held()):
            if holding != seed_id:
                self.store()
        self.load_seed(seed_id)
        if self.get_held() == seed_id:
            self.plant(self.get_held())
            if seed_id in needs_light:
                self.light()
            if seed_id in needs_water:
                self.water()
    if self.get_held():
        self.store()
    return

# move_to("E","13")
# print(self.cell(self.get_position()))

# self.collect()

# self.refill_water()


# move_to_cell("C16")
# self.deploy("sprinkler_kit")


print(self.cell("C14"))

while True:

    deploy_kits()
    
    for seed_id in cells_plant_dict.keys():
        manage_inventory()
        plant_seed(seed_id)
    for seed_id in cells_plant_dict.keys():
        manage_inventory()
        if seed_id in [
            "seed_packfern",
            "seed_shadeleaf",
            "seed_crowncap",
            # "seed_dewmoss"
        ]:
            harvest_seed(seed_id)
    for cell in [
        cell
        for plant_id in needs_light
        for cell in cells_plant_dict.get(plant_id)
        if not self.cell(cell).lit
    ]:
        move_to_cell(cell)
        self.light()
    
# move_to_cell("E12")
# self.harvest()
# print(self.get_held())















