seed_storage = get_component("large_warehouse_10")
plant_terraformer = get_component("plant_terraformer_1")


BATCH = 100

crowncap_add_1 = [
    f"{y}{x}"
    for x in range(1,10)
    for y in ["A", "B", "C", "D", "E", "F", "G", "H"]
    if f"{y}{x}" not in  [
        "C3","F3",
        "C8","F8",
        "C13","F13",
        "C18","F18",
        "C23","F23",
    ]
]

crowncap_add_2 = [
    f"{y}{x}"
    for x in range(18,25)
    for y in ["A", "B", "C", "D", "E", "F", "G", "H"]
    if f"{y}{x}" not in  [
        "C3","F3",
        "C8","F8",
        "C13","F13",
        "C18","F18",
        "C23","F23",
    ]
]

cells_plant_dict = {
    "seed_packfern":["C11","C12","D11","D12"],
    "seed_shadeleaf": ["D13","E14","F13"],
    "seed_crowncap":
    [
        "A11", "B11",
        "B12", "A12",
        "A13", "B13",
        "B14", "A14",
        "A15", "B15",
        "C15", "D15",
        "D14", "C14"
    ]+crowncap_add_1+crowncap_add_2,
    "seed_dewmoss": ["E17"],
    "seed_lonethorn": ["G11"],
    "seed_brinethorn": ["H12"],
    "seed_saltbloom": ["F12","E12"],
    "seed_saltmate": ["E11"],
    "seed_spitebud": ["H10","H16"],
    "seed_sunspur": ["H14"],
    "seed_sunpetal": ["G13"],
    "seed_grandbloom":["F14","G15"],
    "seed_twinvine": ["F17"],
    "seed_glowvine": ["E15","F16"],
    "seed_pondmoss": ["C16","D16","D17"],
}

revert_cell_plant_dict = {
    cell: seed
    for seed, cells in cells_plant_dict.items()
    for cell in cells
}


needs_light = [
    "seed_sunspur",
    "seed_sunpetal",
    # "seed_glowvine"
]

needs_water = [
    "seed_dewmoss",
    # "seed_glowvine"
]
needs_salt = [
    "seed_saltbloom",
    "seed_saltmate",
    "seed_brinethorn",
]

# for cell,seed_id in revert_cell_plant_dict.items():
#     print(cell,seed_id)


self.clear_queue()

while result:= self.next_result().status !="empty":
    print(result)



while True:
    for cell in self.cells():
        cell_id = cell.id
        if self.cell(cell_id).status == "mature":
            self.harvest(cell_id)
            while self.queue_count()>0:
                pass
        if self.cell(cell_id).status == "empty":
            if cell_id not in revert_cell_plant_dict.keys():
                continue
            self.input.connect(seed_storage.id)
            while (result:=self.input.take(revert_cell_plant_dict.get(cell_id),1)).status == "busy":
                pass
            self.plant(cell_id, revert_cell_plant_dict.get(cell_id))
            while self.queue_count()>0:
                pass
        # if self.cell(cell_id).plant.removeprefix("seed_") in needs_salt:
        #     self.input.connect("large_warehouse_1")
        #     while (result:=self.input.take("salt",1)).status == "busy":
        #         pass
        #     while self.queue_count()>0:
        #         pass
        pass
    self.output.connect("plant_terraformer_1")
    while (
        result:=self.output.send(
            "forage",
            min(
                BATCH,
                self.output.count(),
                plant_terraformer.batch_requirements().get("forage") - plant_terraformer.batch_size()
            )
            
        )
    ).status == "busy":
        pass

job = self.current_job()
if job is not None and job.blocker == "no_seed":
    moved = self.move_job(job.id, self.queue_count())
    if moved.status != "ok":
        print(moved.message)
    pass

















    