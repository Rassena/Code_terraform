from cRover import cRover


self = cRover(self)

dict_mining = {
    "iron_ore": "iron_ore",
    "silicon": "silicon",
    "titanium": "titanium",
    "cobalt": "cobalt",
    "rare_earth": "rare_earth",
    "neutronium": "neutronium",
    "lead_ore": "lead_ore",
}

storage_bin = {
    "iron_ore": "storage_bin_2",
    "silicon": "storage_bin_3"
}

rovers = [
    rover.id 
    for rover 
    in get_component("fleet").vehicles() 
    if rover.kind == "rover"
]

ROVERS_IRON = 15


manual_rover_mine_task = {
    "iron_ore": rovers[:ROVERS_IRON],
    "silicon": rovers[ROVERS_IRON:]
}

# self.cargo.discard(0)



def dumb_task_get_salt():
    

    water_pump = get_component("water_pump_1")
    position = water_pump.well().position()
    self.move_to_position(position.x,position.y)
    self._input_connect(water_pump.id)
    self._input_take_item(
        "salt",
        min(
            self.vehicle.cargo.capacity()-self.vehicle.cargo.count(),
            water_pump.output.count()
        )
    )
    self.move_to_position(0,0)
    self._output_sent_item_target(
        "salt",
        self.cargo_get_items().get("salt",0),
        "large_warehouse_1"
    )
    self.recharge()





def main(self):

    # self.mount_base_setup()
    # self.startup()
    
    while True:
        dumb_task_get_salt()
        pass
    
    # self.scan_at_position(300,-20)

    # mineral_id = ""

    # for key,val in manual_rover_mine_task.items():
    #     if self.vehicle.id in val:
    #         mineral_id = key
    
    # while True:
    #     if mineral_id:
    #         if self.vehicle.cargo.count()>0:
    #             self.move_to_position(0,0)
    #             self._output_sent_item_target(mineral_id,self.vehicle.cargo.count(),storage_bin.get(mineral_id))
    #         self.mine_mineral(mineral_id)
    #         self.move_to_position(0,0)
    #         self._output_connect(storage_bin.get(mineral_id))
    #         self._output_sent_item_target(mineral_id,self.vehicle.cargo.count(),storage_bin.get(mineral_id))
    #     self.recharge()




main(self)



                                        