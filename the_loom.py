loom = self.contract.loom

probe_a = "abcdefghijklmnopqrstu"
probe_b = "ABCDEFGHIJKLMNOPQRSTU"

woven = loom.weave(probe_a, probe_b)

positions_a = {}
positions_b = {}

for output_index, char in enumerate(woven):
    if char in probe_a:
        positions_a[probe_a.index(char)] = output_index
    else:
        positions_b[probe_b.index(char)] = output_index

record = self.contract.record

thread_a = [""] * 21
thread_b = [""] * 21

for index, output_index in positions_a.items():
    thread_a[index] = record[output_index]

for index, output_index in positions_b.items():
    thread_b[index] = record[output_index]

thread_a = "".join(thread_a)
thread_b = "".join(thread_b)

print("Thread A:", thread_a)
print("Thread B:", thread_b)

message = thread_a if thread_a else thread_b

transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, message)