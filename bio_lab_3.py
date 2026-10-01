shop = get_component("shop")
inventory = get_component("inventory")
self.input.connect("inventory")
self.output.connect("inventory")
collector=get_component("bio_collector_1")

def buy_missing(recipe):
    for key, item in recipe.items():
        print("Need:",key, item)
        print("Inventory:",key, inventory.count(key))
        if item - inventory.count(key) > 0:
            shop.buy(key, item - inventory.count(key))


def unload_output():
    print( self.output.stacks())
    while self.output.stacks().length > 0:
        item = self.output.stacks().pop()
        self.output.send(item.id,item.count)


def load_recipe(recipe):
    self.unload_reagents()
    self.output.stacks()
    buy_missing(recipe)
    for key, item in recipe.items():
        self.input.take(key,item)
        self.load(key,item)
    print(self.loaded_reagents)
    
self.input.flush()

def main():
    while True:
        if collector.cargo:
            self.take_from(collector)
        if self.specimen:
            if self.specimen.recipe == None:
                self.analyze()
                
            recipe = self.specimen.recipe
            
            print(recipe)
            unload_output()
            load_recipe(recipe)
            if self.loaded_reagents == recipe:
                self.extract()
    


self.output.send(self.output.stacks()[0].id,self.output.stacks()[0].count)
main()

# print(self.output.stacks())
# print(self.input.stacks())



















