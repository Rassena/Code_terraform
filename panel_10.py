source_wh = get_component("warehouse_7")
target_wh = get_component("large_warehouse_7")

MAX_TRANSFER = 10

WAREHOUSES_MINERALS:list[Warehouse] = [
    # get_component("large_warehouse_1"),
    get_component("warehouse_1"),
    get_component("warehouse_5")
]

WAREHOUSES_MATERIALS:list[Warehouse] = [
    # get_component("large_warehouse_2"),
    get_component("warehouse_2"),
    get_component("warehouse_12"),
]

WAREHOUSES_PRODUCTS:list[Warehouse] = [
    # get_component("large_warehouse_3"),
    get_component("warehouse_15"),
    get_component("warehouse_16"),
]



def transfer(source_wh:Warehouse,target_wh:Warehouse):
    for item_id in source_wh.materials():
        while source_wh.count(item_id) >0:
            while(
                not source_wh.transfer_to(
                    target_wh.id,item_id,
                    min(
                        MAX_TRANSFER,
                        source_wh.count(item_id)
                    )
                ).status in ["busy","no_op"]
            ):        
                print(
                    source_wh.transfer_to(
                    target_wh.id,item_id,
                    min(
                        MAX_TRANSFER,
                        source_wh.count(item_id)
                    )
                ).status
                )



# for source_wh in WAREHOUSES_PRODUCTS:

transfer(source_wh,target_wh)

