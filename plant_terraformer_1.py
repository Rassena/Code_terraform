self.water_in.connect("liquid_tank_1")
inventory = get_component("inventory")
warehouse = get_component("large_warehouse_2")

BATCH = 10


def move_forage_to_warehouse():
    if inventory.count("forage")>0:
        while (status:= inventory.transfer_to(
            warehouse.id,
            "forage",min(
                inventory.count("forage"),
                BATCH
            )
        ).status == "busy"):
            pass

def insert_forage_from_warehouse():
    if self.input.capacity()>0:
        self.input.connect(warehouse.id)
        if warehouse.count("forage")>0:
            while (status:= self.input.take(
                "forage",
                min(
                    warehouse.count("forage"),
                    max(
                        self.input.capacity() - self.input.count(),
                        0
                    ),
                    BATCH
                )
            ).status == "busy"):
                pass
    pass

def insert_forage_from_inventory():
    if self.input.capacity()>0:
        self.input.connect("inventory")
        if inventory.count("forage")>0:
            while (status:= self.input.take(
                "forage",
                min(
                    inventory.count("forage"),
                    max(
                        self.input.capacity() - self.input.count(),
                        0
                    ),
                )
            ).status == "busy"):
                pass
    pass

self.set_enabled(True)

while True:
    insert_forage_from_inventory()
    insert_forage_from_warehouse()
    move_forage_to_warehouse()
