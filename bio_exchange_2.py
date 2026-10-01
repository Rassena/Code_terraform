shop = get_component("shop")
inventory = get_component("inventory")
self.input.connect("inventory")
self.output.connect("inventory")
# collector=get_component("bio_collector_1")

collectors = [
    # get_component("bio_collector_1"),
    get_component("bio_collector_2"),
    # get_component("bio_collector_3") 
]



collectable = [
    item.fragment_id
    for collector in collectors
    for item in collector.scan()
]

def get_orders_possible_to_finish():
    possible = []
    for order in self.orders():
        if order.status == "available":
            missing = False
            for wanted, _ in order.requires.items():
                if wanted not in collectable:
                    missing = True
            if(
                not missing
                and order.target_glow is None
            ):
                print(order.id,order.target_glow,order.required_genes)
                possible.append(order)
    return possible

def get_next_order():
    if self.active_order() is None:
        if get_orders_possible_to_finish().length > 0:
            next_order = get_orders_possible_to_finish()[0]
            print(next_order)
            self.set_order(next_order.id)
        

def collect_missing():
    print("req:", self.active_order().requires)
    print("inv:")
    for key, _ in self.active_order().requires.items():
        print("   ",key, inventory.count(key))


def deliver():
    if self.active_order():
        for key, item in self.active_order().requires.items():
            if inventory.count(key) > 0:
                print("min", inventory.count(key),item)
                self.input.take(key,min(inventory.count(key),item - self.active_order().delivered.get(key)))
        if self.input.stacks():
            self.deliver()


# get_next_order()

self.input.flush()
self.clear_order()

while True:
    get_next_order()
    deliver()













