import cConstructionBlueprint as cCoB


self.coastal_essence_in.connect("liquid_tank_3")
self.frozen_essence_in.connect("liquid_tank_4")
self.volcanic_essence_in.connect("liquid_tank_5")
self.deep_essence_in.connect("liquid_tank_6")
self.geothermal_essence_in.connect("liquid_tank_7")

# cCoB.construction_blueprint.plan_pipe("frozen_essence",20,-25,340,-25)
cCoB.construction_blueprint.plan_pipe("frozen_essence",20,-100,20,-490)
# cCoB.construction_blueprint.plan_bridge("frozen_essence",20,0,"vertical")


while True:
    pass