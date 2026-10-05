import cStorage as cStor

notebook = get_component("notebook")
clock = get_component("clock")

class cSmelter():
    
    production:Smelter

    MINERAL_THRESHOLD:int
    STORAGE_DYNAMIC_MAX:int
    SMELT_BATCH:int
    SLEEP_TICK:float
    
    def __init__(self,production:Smelter):
        self.production = production
        self._update_constants()
        
    def _update_constants(self):
        constants = notebook.get("constants.smelter",{})

        self.MINERAL_THRESHOLD = constants.get("MINERAL_THRESHOLD",100)
        self.STORAGE_DYNAMIC_MAX = constants.get("STORAGE_DYNAMIC_MAX",1500)
        self.SMELT_BATCH = constants.get("SMELT_BATCH",10)
        self.SMELT_BATCH = constants.get("SLEEP_TICK",1)
        
        return
    
    def is_empty(self) -> bool:
        return (
            self.production.get_input_count() == 0
            and self.production.get_output_count() == 0 
        )

    def get_product_id(self) -> str:
        return self.production.get_recipe().removeprefix("smelt_")
        
    def clear_recipe(self) -> ActionResult:
        while not self.is_empty():
            self.export_item()
        return self.production.clear_recipe()
    
    def set_recipe(self,recipe_id:str) -> ActionResult:
        self.clear_recipe()
        return self.production.set_recipe(recipe_id)
    
    def is_product_below_storage_max(self,product_id:str) -> bool:
        items:dict[str,[str,int]] = notebook.get("storage.outpost_home.items")
        return items.get(product_id,["",0])[1] < self.STORAGE_DYNAMIC_MAX
        
    def _set_input(self,source_id:str) -> ActionResult:
        return self.production.input.connect(source_id)

    def _set_output(self,target_id:str) -> ActionResult:
        return self.production.output.connect(target_id)

    def set_input_storage(self,item_id:str) -> ActionResult:
        storage_items:dict[str,[str,int]] = notebook.get("storage.outpost_home.items")
        return self._set_input(storage_items.get(item_id,["",0])[0][0])

    def set_output_storage(self,item_id: str) -> ActionResult:
        
        storage_items:dict[str,[str,int]] = notebook.get("storage.outpost_home.items")

        if item_id in storage_items.keys():
            return self._set_output(storage_items.get(item_id,["",0])[0][0])
        
        for warehouse_id in notebook.get("storage.warehouses").get("WAREHOUSES_MATERIALS",[]):
            warehouse: Warehouse = get_component(warehouse_id)
    
            if warehouse.space_for(item_id) > 0:
                return self._set_output(warehouse.id)

    def input_item(self,item_id:str,amount:int) -> TransferResult:

        self.set_input_storage(item_id)
        
        result:TransferResult
        
        while (result := self.production.input.take(item_id,amount)).status == "busy":
            sleep(1)
        
        return result
    
    def output_item(self,item_id:str,amount:int) -> TransferResult:

        self.set_output_storage(item_id)
        
        result:TransferResult
        
        while (result := self.production.output.send(item_id,amount)).status == "busy":
            sleep(1)
        
        return result
    
    def recipes_possible_below_threshold(self) -> list[Recipe]:
        in_storage: dict[str, int] = notebook.get("storage.outpost_home.items")
    
        batch = self.SMELT_BATCH
        threshold = self.MINERAL_THRESHOLD
        max_storage = self.STORAGE_DYNAMIC_MAX
        production = self.production


        recipes = production.list_recipes()
        
        return sorted(
            (
                recipe
                for recipe in production.list_recipes()
                if in_storage.get(recipe.output_item, [["",int]])[0][1] < max_storage
                and all(
                    in_storage.get(item_id, [["",int]])[0][1] >= batch * amount + threshold
                    for item_id, amount in recipe.inputs.items()
                )
            ),
            key=lambda recipe: recipe.tier,
        )  

    def import_item(self) -> ActionResult:

        item_id = self.production.get_recipe_inputs().keys()[0]
        
        batch = self.SMELT_BATCH
        threshold = self.MINERAL_THRESHOLD
        max_input = self.production.input.capacity()
    
        current = self.production.get_input_count()
        available = get_component(
            notebook.get("storage.outpost_home.items").get(item_id,[["",0]])[0][0]
        ).count(item_id)-threshold
        
        amount = min(
            max_input - current,
            max(available,0),
            batch
        )
    
        if amount > 0:
            return self.input_item(item_id,amount)
        return
    
    def export_item(self) -> ActionResult:

        if self.production.get_output_count() == 0:
            return

        item_id = self.get_product_id()
        
        batch = self.SMELT_BATCH
        current = self.production.get_output_count()
        available = get_component(self.production.output.connected_to()).space_for(item_id)
    
        amount = min(
            current,
            available,
            batch
        )

        if amount > 0:
            return self.output_item(item_id,amount)    
        return

    def smelt(self):
        
        const_last_update = clock.get_time()[0]
        
        while True:

            if const_last_update != clock.get_time()[0]:
                self._update_constants()
                const_last_update = clock.get_time()[0]
            
            next_recipe = next(self.recipes_possible_below_threshold(),None)

            self.production.get_recipe()
            
            if next_recipe:
                if self.production.get_recipe() != next_recipe.id:
                    self.set_recipe(next_recipe.id)
                else:
                    self.import_item()
                    self.export_item()
            else:
                self.clear_recipe()
            sleep(1)
      
        return











