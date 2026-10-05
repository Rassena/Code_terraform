drone_station = get_component("drone_station_lrg_2")
warehouse = get_component("large_warehouse_8")


life_forms_id = [
    # "brine_plankton",
    "coral_fungus",
    # "salt_crust",
    # "sea_algae",
    # "shore_lichen",
    # "tide_moss"
]

self.coastal_essence_out.connect("liquid_tank_3")
self.input.connect(drone_station.id)

# self.input.flush()


while True:
    if self.is_stalled():
        stacks_ref = drone_station.output.stacks()
        for stack_ref in stacks_ref:
            if stack_ref.id in life_forms_id:
                self.input.take(
                    stack_ref.id,
                    min(
                        stack_ref.count,
                        self.input.capacity()-self.input.count()
                    )
                )
    if not self.input.stacks():
        self.input.connect(warehouse.id)
        while self.input.take(
            life_forms_id[0],
            min(
                max(
                    warehouse.count(life_forms_id[0])-10,
                    0
                ),
                self.input.capacity()-self.input.count()
            )
        ).status == "busy":
            pass