import cStorage as cStor

ITEM_STORAGE_AMOUNT_THRESHOLD = 50


def print_orders(orders:list[Order]):
    for order in orders:
        print(order.id,order.requires,order.status)

def get_orders_all() -> list[Order]:
    orders = get_component("orders")
    return (orders.list_orders() + orders.list_weekly_orders())

def get_orders_active(outpost_id:str) -> list[Order]:
    orders = get_orders_all()
    storage = cStor.get_items_warehouses_outpost(outpost_id)
    return [ 
        order
        for order in orders 
        if order.status == "active"
    ]

def get_orders_possible(outpost_id:str) ->list[Order]:
    orders = get_orders_all()
    storage = cStor.get_items_warehouses_outpost(outpost_id)
    return [ 
        order
        for order in orders if
        all(
            item_id in storage.keys() 
            and order.status == "active"
            for item_id in order.requires.keys()
        )
    ]
    
def get_orders_possible_instant(outpost_id:str) ->list[Order]:
    orders = get_orders_all()
    storage = cStor.get_items_warehouses_outpost(outpost_id)
    return [ 
        order
        for order in orders if
        all(
            item_id in storage.keys() 
            and order.requires.get(item_id) < storage.get(item_id) - ITEM_STORAGE_AMOUNT_THRESHOLD
            and order.status == "active"
            for item_id in order.requires.keys()
        )
    ]

def get_next_order_possible(outpost_id:str) -> Order:
    return next(get_orders_possible(outpost_id),None)

def get_next_order_possible_instant(outpost_id:str) -> Order:
    return next(get_orders_possible_instant(outpost_id),None)













