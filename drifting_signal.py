def decode_slabs(slabs, shift):
    result = ""

    for char in slabs:
        if "A" <= char <= "Z":
            result += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
        elif "a" <= char <= "z":
            result += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
        else:
            result += char

    return result


def main():
    device = self.contract.device
    slabs = device.slabs

    # Try all 26 possible offsets.
    for shift in range(26):
        message = decode_slabs(slabs, shift)

        print(shift, message)

        # TODO: identify which message is readable
        # and transmit it.

    transmitter = get_component("transmitter")
    transmitter.connect("earth")
    transmitter.transmit(self.contract.id, "WE HAVE NEVER BEEN ALONE OUT HERE")
main()