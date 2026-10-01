thermometer = get_component("thermometer")
transmitter = get_component("transmitter")

transmitter.connect("earth")

transmitter.transmit("current_temperature",thermometer.get_value())