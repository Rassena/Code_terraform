WAREHOUSES_MINERALS:list[Warehouse] = [
    get_component("large_warehouse_1"),
]

WAREHOUSES_MATERIALS:list[Warehouse] = [
    get_component("large_warehouse_2"),
]

WAREHOUSES_PRODUCTS:list[Warehouse] = [
    get_component("large_warehouse_3"),
    get_component("large_warehouse_4"),
    get_component("large_warehouse_5"),
    get_component("large_warehouse_6"),
]

WAREHOUSES_REAGENTS:list[Warehouse] = [
    get_component("warehouse_7"),
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

outpost_network = get_component("outpost_network")

def get_all_warehouses() -> list[Warehouse]:
    outpost_refs = outpost_network.outposts()
    return [
        get_component(wh_ref.id) 
        for outpost in outpost_refs
        for wh_ref in outpost.buildings("warehouse") + outpost.buildings("large_warehouse")
    ]
    
def get_all_storage_bins() -> list[StorageBin]:
    outpost_refs = outpost_network.outposts()
    return [
        get_component(storage_bin_ref.id) 
        for outpost in outpost_refs
        for storage_bin_ref in outpost.buildings("storage_bin")
    ]

def get_warehouses_outpost(outpost_id:str) -> list[Warehouse]:
    warehouse_refs = get_component(outpost_id).buildings("warehouse") + get_component(outpost_id).buildings("large_warehouse")
    return [
        get_component(warehouse_ref.id)
            for warehouse_ref in warehouse_refs
    ]
    
def get_storage_bins_outpost(outpost_id:str) -> list[StorageBin]:
    storage_bin_refs = get_component(outpost_id).buildings("storage_bin")
    return [
        get_component(storage_bin_ref.id)
            for storage_bin_ref in storage_bin_refs
    ]

def get_warehouse_outpost(item_id:str, outpost_id:str) -> Warehouse|None:

    warehouses = get_warehouses_outpost(outpost_id)

    warehouse = next(
        (
            warehouse
            for warehouse in warehouses 
            if item_id in warehouse.materials()
        ),
        warehouses[0] if warehouses else None
    )
        
    return warehouse
    
def get_storage_bin_outpost(item_id:str, outpost_id:str) -> StorageBin|None:

    storage_bins = get_storage_bins_outpost(outpost_id)

    storage_bin = next(
        (
            storage_bin
            for storage_bin in storage_bins 
            if item_id == storage_bin.get_material()
        ),
        storage_bins[0] if storage_bins else None
    )
        
    return storage_bin

def get_warehouses_minerals_outpost(outpost_id:str) -> list[Warehouse]:
    return [
        warehouse 
        for warehouse in WAREHOUSES_MINERALS 
        if warehouse.outpost.id == outpost_id
    ]

def get_warehouse_mineral_outpost(mineral_id:str, outpost_id:str) -> Warehouse|None:

    warehouses = get_warehouses_minerals_outpost(outpost_id)

    warehouse = next(
        (
            warehouse
            for warehouse in warehouses 
            if mineral_id in warehouse.materials()
        ),
        warehouses[0] if warehouses else None
    )
        
    return warehouse

def get_storage_bins_minerals_outpost(outpost_id:str) -> list[StorageBin]:
    return [
        storage_bin 
        for storage_bin in STORAGE_BINS_MINERALS 
        if storage_bin.outpost.id == outpost_id
    ]

def get_storage_bin_mineral_outpost(mineral_id:str, outpost_id:str) -> StorageBin|None:

    storage_bins = get_storage_bins_minerals_outpost(outpost_id)

    storage_bin = next(
        (
            storage_bin
            for storage_bin in storage_bins 
            if mineral_id == storage_bin.get_material()
        ),
        storage_bins[0] if storage_bins else None
    )
        
    return storage_bin

def get_warehouses_materials_outpost(outpost_id:str) -> list[Warehouse]:
    return [
        warehouse 
        for warehouse in WAREHOUSES_MATERIALS 
        if warehouse.outpost.id == outpost_id
    ]


def get_warehouse_material_outpost(material_id:str, outpost_id:str) -> Warehouse|None:

    warehouses = get_warehouses_materials_outpost(outpost_id)

    warehouse = next(
        (
            warehouse
            for warehouse in warehouses 
            if material_id in warehouse.materials()
        ),
        warehouses[0] if warehouses else None
    )
        
    return warehouse


def get_storage_bins_materials_outpost(outpost_id:str) -> list[StorageBin]:
    return [
        storage_bin 
        for storage_bin in STORAGE_BINS_MATERIALS 
        if storage_bin.outpost.id == outpost_id
    ]


def get_storage_bin_material_outpost(material_id:str, outpost_id:str) -> StorageBin|None:

    storage_bins = get_storage_bins_materials_outpost(outpost_id)

    storage_bin = next(
        (
            storage_bin
            for storage_bin in storage_bins 
            if material_id == storage_bin.get_material()
        ),
        storage_bins[0] if storage_bins else None
    )
        
    return storage_bin


def get_warehouses_products_outpost(outpost_id:str) -> list[Warehouse]:
    return [
        warehouse 
        for warehouse in WAREHOUSES_PRODUCTS 
        if warehouse.outpost.id == outpost_id
    ]


def get_warehouse_product_outpost(product_id:str, outpost_id:str) -> Warehouse|None:

    warehouses = get_warehouses_products_outpost(outpost_id)

    warehouse = next(
        (
            warehouse
            for warehouse in warehouses 
            if product_id in warehouse.materials()
        ),
        warehouses[0] if warehouses else None
    )
        
    return warehouse

def get_warehouses_reagents_outpost(outpost_id:str) -> list[Warehouse]:
    return [
        warehouse 
        for warehouse in WAREHOUSES_REAGENTS 
        if warehouse.outpost.id == outpost_id
    ]


def get_warehouse_reagent_outpost(reagent_id:str, outpost_id:str) -> Warehouse|None:

    warehouses = get_warehouses_reagents_outpost(outpost_id)

    warehouse = next(
        (
            warehouse
            for warehouse in warehouses 
            if reagent_id in warehouse.materials()
        ),
        warehouses[0] if warehouses else None
    )
        
    return warehouse

def get_storage_bins_products_outpost(outpost_id:str) -> list[StorageBin]:
    return [
        storage_bin 
        for storage_bin in STORAGE_BINS_PRODUCTS 
        if storage_bin.outpost.id == outpost_id
    ]

def get_storage_bin_product_outpost(product_id:str, outpost_id:str) -> StorageBin|None:

    storage_bins = get_storage_bins_products_outpost(outpost_id)

    storage_bin = next(
        (
            storage_bin
            for storage_bin in storage_bins 
            if product_id == storage_bin.get_material()
        ),
        storage_bins[0] if storage_bins else None
    )
        
    return storage_bin


def get_items_warehouses_outpost(outpost_id: str) -> dict[str, int]:
    items = {}

    for wh in get_warehouses_outpost(outpost_id):
        for item_id in wh.materials():
            items[item_id] = items.get(item_id, 0) + wh.count(item_id)
    
    return items

def get_items_storage_bins_outpost(outpost_id: str) -> dict[str, int]:
    items = {}

    for storage_bin in get_storage_bins_outpost(outpost_id):
        items[storage_bin.get_material()] = items.get(storage_bin.get_material(), 0) + storage_bin.count(storage_bin.get_material())
    
    return items

def get_items_warehouses_minerals_outpost(outpost_id:str) -> dict[str, int]:
    items = {}

    for wh in get_warehouses_minerals_outpost(outpost_id):
        for item_id in wh.materials():
            items[item_id] = items.get(item_id, 0) + wh.count(item_id)

    return items

def get_items_warehouses_materials_outpost(outpost_id:str) -> dict[str, int]:
    items = {}

    for wh in get_warehouses_materials_outpost(outpost_id):
        for item_id in wh.materials():
            items[item_id] = items.get(item_id, 0) + wh.count(item_id)

    return items

def get_items_warehouses_products_outpost(outpost_id:str) -> dict[str, int]:
    items = {}

    for wh in get_warehouses_products_outpost(outpost_id):
        for item_id in wh.materials():
            items[item_id] = items.get(item_id, 0) + wh.count(item_id)

    return items

def get_warehouses_with_item(item_id: str) -> list[Warehouse]:
    return [
        warehouse
        for warehouse in get_all_warehouses()
        if item_id in warehouse.materials()
    ]

def get_warehouses_with_item_and_space(item_id: str) -> list[Warehouse]:
    return [
        warehouse
        for warehouse in get_all_warehouses()
        if item_id in warehouse.materials()
        and warehouse.space_for(item_id) > 0
    ]

def get_nearest_warehouse_with_item(item_id:str, x:int, y:int) -> Warehouse | None:
    warehouses = get_warehouses_with_item(item_id)

    if not warehouses:
        return None

    return min(
        warehouses,
        key=lambda warehouse: (
            (warehouse.outpost.position().x - x) ** 2
            + (warehouse.outpost.position().y - y) ** 2
        )
    )

def get_refs_warehouses_outpost(outpost_id:str) -> list[BuildingRef]:
    return get_component(outpost_id).buildings("warehouse")

def get_refs_items_warehouses_outpost(outpost_id:str) -> list[ItemStack]:
    return






























