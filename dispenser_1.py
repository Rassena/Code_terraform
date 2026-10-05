salt_warehouse = get_component("large_warehouse_1")

self.input.connect(salt_warehouse.id)

BATCH = 10

self.set_enabled(True)

while True:

    if self.buffer() <1:
        while (
            result := self.input.take(
                "salt",
                min(
                    BATCH,
                    self.input.capacity()-self.input.count(),
                    salt_warehouse.count("salt")
                )
            )
        ).status == "busy":
            pass

    
    pass