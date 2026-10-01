pressure_sensor = get_component("pressure_sensor")

pressure_val = pressure_sensor.get_value()

pressure_sensor.stabilize(
    pressure_val 
    if pressure_val%2==0 
    else pressure_val+1
)