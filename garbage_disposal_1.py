import cStorage as cStor

WASTE_THRESHOLD = 1900


wh_minerals_dict = cStor.get_items_warehouses_minerals_outpost(self.outpost.id)


self.set_enabled(True)
self.set_mode("items")

while True:
    for mineral_id,amount in wh_minerals_dict.items():
        if self.input.count() < self.input.capacity() - 10:
            if amount>WASTE_THRESHOLD:
                wh = cStor.get_nearest_warehouse_with_item(mineral_id,self.outpost.x,self.outpost.y)
                if wh is None:
                    continue
                self.input.connect(wh.id)
                while self.input.take(
                    mineral_id,
                    min(
                        self.input.capacity() - self.input.count(),
                        max(
                            wh.count(mineral_id) - WASTE_THRESHOLD,
                            0
                        )
                    )
                ).status == "busy":
                    pass