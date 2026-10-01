import cStorage as cStor
import cOrder

clock = get_component("clock")

ITEM_STORAGE_AMOUNT_THRESHOLD = 50

def print_current_order():
    if order := self.current_order():
        print(f"{order.id} | {order.requires} | {order.status}")
    return

def set_input_storage(item_id:str) -> ActionResult:
    for wh in cStor.get_warehouses_outpost(self.outpost.id):
        if wh.count(item_id) > 0:
            return self.input.connect(wh.id)
    return self.input.disconnect()


def is_fulfilled():
    pass

def transfer_item(item_id: str) -> ActionResult:
    set_input_storage(item_id)

    if(
        self.current_order() is None
        or self.input.connected_to() == ""
    ):
        return
        
    required = self.current_order().requires.get(item_id, 0)
    shipped = self.current_order().shipped.get(item_id, 0)
    current = self.count(item_id)
    available = get_component(self.input.connected_to()).count(item_id)

    amount = min(required - current - shipped, available-ITEM_STORAGE_AMOUNT_THRESHOLD)

    if amount > 0:
        if self.input.take(item_id, amount).status == "busy":
            pass

    return
    
def deploy_order():

    for item_id in self.current_order().requires.keys():
        transfer_item(item_id)
    
    return self.set_enabled(True)


self.input.flush()
self.set_enabled(False)
cOrder.print_orders(cOrder.get_orders_active(self.outpost.id))

self.clear_order()

while True:
    if (
        self.current_order() is not None
        and self.current_dispatch() is None
    ):
        deploy_order()
    elif(
        self.current_dispatch() is None
    ):
        if order := cOrder.get_next_order_possible_instant(self.outpost.id):
            print(self.set_order(order.id))
        elif order := cOrder.get_next_order_possible(self.outpost.id):
                print(self.set_order(order.id))
        else:
            sleep(clock.real_seconds_per_hour())
    















