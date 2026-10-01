archive = self.contract.archive

def dumb_solver():
    result_dict = {}
    
    for row in range(archive.rows):
        for col in range(archive.cols):
            word = archive.flip(row,col)
            if result_dict.get(word) is None:
                result_dict[word] = []
            result_dict[word]=result_dict[word] + [row,col]

    return result_dict



print(dumb_solver())

pairs = [pair for _,pair in dumb_solver().items()]

print(pairs)
transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, pairs)    