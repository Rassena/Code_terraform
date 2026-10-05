import cStorage as cStor

INGREDIENT_THRESHOLD = 50

STORAGE_DYNAMIC_MAX = 200
STORAGE_DYNAMIC_MIN = 10
PRODUCT_BATCH = 10

product_min = True


def clear_recipe():
    if(
        not self.is_running()
        and self.get_output_count() == 0
    ):
        self.clear_recipe()
    return

def set_recipe(recipe_id:str) -> ActionResult | None:
    if(
        not self.is_running()
        and self.get_output_count() == 0
    ):
        return self.set_recipe(recipe_id)
    return None

def set_input_storage(item_id:str) -> ActionResult:
    for wh in cStor.get_warehouses_outpost(self.outpost.id):
        if wh.count(item_id) > 0:
            return self.input.connect(wh.id)
    return None

def set_output_storage(item_id: str) -> ActionResult:
    
    warehouses = cStor.get_warehouses_products_outpost(self.outpost.id)
    warehouse = next(
        (
            wh for wh in warehouses
            if item_id in wh.materials() and wh.space_for(item_id) > 0
        ),
        None
    )
    if warehouse is None:
        warehouse = next(
            (
                wh for wh in warehouses
                if wh.space_for(item_id) > 0
            ),
            None
        )
    
    return self.output.connect(warehouse.id) if warehouse else None

def import_item(item_id: str,threshold:int) -> ActionResult:
    if set_input_storage(item_id) is None:
        return 
        
    required = threshold
    current = self.get_stockpile().get(item_id,0)
    available = get_component(self.input.connected_to()).count(item_id)
    amount = min(required - current, available)

    if amount > 0:
        while self.input.take(item_id, amount).status == "busy":
            continue
        return 
    return
  
def send_item(item_id: str) -> ActionResult:
    if set_output_storage(item_id) is None:
        return
    current = self.get_output_count()
    available = get_component(self.output.connected_to()).space_for(item_id)

    amount = min(current, available)
    if amount > 0:
        while self.output.send(item_id, amount) == "busy":
            continue
        return
    return



def send_byproduct():
    for stack in self.byproduct.stacks():
        if self.byproduct.count() > 0:
            _send_byproduct(stack.id) 
    return

def _send_byproduct(byproduct_id: str) -> ActionResult:
    current = self.byproduct.count()
    available = get_component(self.byproduct.connected_to()).space_for(byproduct_id)

    amount = min(current, available)
    if amount > 0:
        while self.byproduct.send(byproduct_id, amount) == "busy":
            pass
        return
    return
    

def product_below_storage_threshold(product_id:str) -> bool:
    products = cStor.get_items_warehouses_outpost(self.outpost.id)
    return products.get(product_id,0) < (STORAGE_DYNAMIC_MIN if product_min else STORAGE_DYNAMIC_MAX)
    
def ingredients_below_storage_threshold(req_ingredients:dict[str,int]) -> bool:
    ingredients = cStor.get_items_warehouses_outpost(self.outpost.id)
    # print(req_ingredients,
    #         [ingredients.get(req_ingredient_id,0) < (PRODUCT_BATCH*amount + INGREDIENT_THRESHOLD) 
    #     for req_ingredient_id, amount in req_ingredients.items()]
    #      )
    return any(
        ingredients.get(req_ingredient_id,0) < (PRODUCT_BATCH*amount + INGREDIENT_THRESHOLD) 
        for req_ingredient_id, amount in req_ingredients.items()
    )

def refill(dynamic:bool=False):
    if self.get_recipe():
        product_id = self.find_recipe(self.get_recipe()).output_item
        if product_below_storage_threshold(product_id):
            for item_id,val in self.get_recipe_inputs().items():
                    import_item(item_id,floor(PRODUCT_BATCH * val))
        else:
            if not self.is_running():
                stacks = self.input.stacks()
                for stack in stacks:
                    while self.input.eject(
                        cStor.get_warehouse_outpost(stack.id,self.outpost.id).id,
                        stack.id,
                        stack.count
                    ).status == "busy":
                        continue
                send_product()
                clear_recipe()
        
    return

def send_product():
    for stack in self.output.stacks():
        if self.get_output_count() > 0:
            send_item(stack.id)
        
    return
    
def get_recipes_possible() -> list[Recipe]:
    return [
        recipe
        for recipe in sorted(self.list_recipes(), key=lambda recipe: recipe.tier)
        if not ingredients_below_storage_threshold(recipe.inputs)
        and all(
            getattr(self, fluid).connected_to() != ""
            for fluid in recipe.fluid_inputs
        )
    ]
    
def recipes_possible_below_threshold() -> list[Recipe]:
    return [
        recipe
        for recipe in get_recipes_possible()
        if product_below_storage_threshold(recipe.output_item)
    ]

def dynamic_recipes():

    recipes_possible = get_recipes_possible()
    print("\n\n\nPosible:",recipes_possible.length)   
    for recipe in recipes_possible:
        print(recipe.id, recipe.inputs, recipe.fluid_inputs, recipe.output_item, recipe.byproduct_item)


    recipes_possible_below = recipes_possible_below_threshold()
    print("\n\n\nNext to make:",recipes_possible_below.length)
    for recipe in recipes_possible_below:
        print(recipe.id, recipe.inputs, recipe.fluid_inputs, recipe.output_item, recipe.byproduct_item)
    
    return

self.steam_in.connect("gas_tank_1")
self.water_in.connect("liquid_tank_1")
self.oil_in.connect("liquid_tank_2")
self.byproduct.connect("large_warehouse_1")

# if self.input.stacks().length>0:
#     stacks = self.input.stacks()
#     for stack in stacks:
#         set_input_storage(stack.id)
#         while self.input.eject(
#             cStor.get_warehouse_outpost(stack.id,self.outpost.id).id,
#             stack.id,
#             stack.count
#         ).status == "busy":
#             # print("busy:",self.input.eject(
#             # cStor.get_warehouse_outpost(stack.id,self.outpost.id).id,
#             # stack.id,
#             # stack.count))
#             continue
        
    


# while True:
#     clear_recipe()
#     self.set_recipe("craft_dispenser_kit")
#     refill(True)
#     send_product()
#     send_byproduct()



while True:
    if self.byproduct.count() > 0:
        send_byproduct()
    next_recipe = next(recipes_possible_below_threshold(),None)
    if next_recipe:
        if self.get_recipe() != next_recipe.id:
            set_recipe(next_recipe.id)
        else:
            refill(True)
    else:
        product_min = False
        clear_recipe()
    
    
    
    send_product()
    send_byproduct()

      









