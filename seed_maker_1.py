notebook = get_component("notebook")
inv = get_component("inventory")

warehouses = [
    get_component("large_warehouse_7"),
    get_component("large_warehouse_8"),
    get_component("large_warehouse_9")
]

seed_storage = get_component("large_warehouse_10")
SEED_IN_STORAGE_MAX = 300
BATCH_SEED_MAKE = 100

def is_in_warehouses(combination):

    available = []

    for warehouse in warehouses:
        available+=warehouse.materials()


    return all(
        life_form_id in available
        for life_form_id in combination
    )

def get_life_form(life_form_id):
    for warehouse in warehouses:
        if warehouse.count(life_form_id)>0:
            self.input.connect(warehouse.id)
            while self.input.take(life_form_id,1).status =="busy":
                pass

def export_seed():
    for stack in self.output.stacks():
        sent = False
        for warehouse in warehouses:
            if warehouse.count(stack.id)>0:
                self.output.connect(warehouse.id)
                while self.output.send(stack.id,1).status == "busy":
                    pass
        if not sent:
            for warehouse in warehouses:
                if warehouse.space_for(stack.id)>0:
                    self.output.connect(warehouse.id)
                    while self.output.send(stack.id,stack.count).status == "busy":
                        pass
accepted_life_forms = self.life_forms()

def get_recipes():
    recipes = {}

    for recipe in self.recipes():
        recipes[recipe.seed_id] = recipe.blend

    return recipes

def create_seed(seed_id):
    combination = get_recipes().get(seed_id)
    if combination:
        if (
            is_in_warehouses(combination)
        ):
            for life_form_id in combination:
                get_life_form(life_form_id)
            while (result := self.combine(combination).status) == "busy":
                pass
            if result == "seed_found":
                export_seed()
                print("Created:",seed_id)
    pass


# notebook.set("seed_maker.checked",{"checked":[]})
self.input.flush()
export_seed()

while True:
    for seed_id in get_recipes().keys():
        if not is_in_warehouses([seed_id]):
            if seed_storage.count(seed_id)<SEED_IN_STORAGE_MAX:
                for _ in range(BATCH_SEED_MAKE):
                    create_seed(seed_id)
 

# for combination in reversed(combinations(accepted_life_forms,3)):

#     checked:list 
#     while (checked := notebook.get("seed_maker.checked").get("checked",[])) is None:
#         pass
        
#     if (
#         list(combination) not in checked
#         and is_in_warehouses(combination)
#     ):
#         for life_form_id in combination:
#             get_life_form(life_form_id)
#         while (result := self.combine(combination).status) == "busy":
#             pass
#         if result == "seed_found":
#             export_seed()
#             print("seed_found")

#         while (checked := notebook.get("seed_maker.checked").get("checked",[])) is None:
#             pass
#         if result == "sludge":
#             checked.append(combination)
#             while notebook.set("seed_maker.checked",{"checked":checked}).status != "ok":
#                 pass







