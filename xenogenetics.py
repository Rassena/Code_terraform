c = self.contract
print(c)

unknown = []

def dumb_serach():
    for gen in c.samples:
        if gen not in c.earth_ref:
            unknown.append(gen)
    return unknown

c = self.contract
transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(c.id, dumb_serach())