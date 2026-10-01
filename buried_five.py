analyzer = self.contract.analyzer
transmission = self.contract.transmission

for _ in range(self.contract.layers):
    decoded = []

    for i in range(0, len(transmission), 5):
        group = transmission[i:i + 5]
        decoded.append(analyzer.read(group))

    transmission = decoded

message = "".join(transmission)

transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, message)