inv = get_component("inventory")
shop = get_component("shop")

drone_station = get_component(self.id)

self.input.connect(inv.id)
self.output.connect(self.id)

reagents_id = [
    "alkaline_buffer",
    "cryo_solvent",
    "protein_marker",
    "chelating_agent",
    "enzyme_solution",
]

def fill_reagents():

    for reagent_id in reagents_id:
    
    pass
    
    