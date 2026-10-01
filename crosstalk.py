input_x = self.contract.input_x
input_y = self.contract.input_y
min_length = self.contract.min_length

def extract_bits(signal):
    bits = []

    for i in range(len(signal)):
        if signal[i] not in ("0", "1"):
            continue

        # Need at least 2 characters on each side.
        if i < 2 or i + 2 >= len(signal):
            continue

        # The letters around the bit must mirror:
        # A B 1 B A
        if (
            signal[i - 2] == signal[i + 2]
            and signal[i - 1] == signal[i + 1]
        ):
            bits.append(int(signal[i]))

    return bits


x = extract_bits(input_x)
y = extract_bits(input_y)

# Combine the two streams using XOR:
# x y' + x' y
result = []

for i in range(len(x)):
    result.append(x[i] ^ y[i])

# Decode 5 bits at a time.
message = ""

for i in range(0, len(result), 5):
    bits = result[i:i + 5]

    if len(bits) < 5:
        break

    value = 0

    for bit in bits:
        value = value * 2 + bit

    if 1 <= value <= 26:
        message += chr(ord("A") + value - 1)

print(message)

transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, message)