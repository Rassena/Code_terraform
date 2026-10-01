tablet = self.contract.tablet


def dumb_solver():
    result_str = ""
    
    for row in range(tablet.rows):
        for col in range(tablet.cols):
            result = tablet.probe(row, col)
            if result.distance == 0:
                result_str+=result.char
    return result_str


transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, dumb_solver())