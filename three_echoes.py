def main():
    broadcast = self.contract.broadcast

    a = broadcast.freq_a
    b = broadcast.freq_b
    c = broadcast.freq_c

    subject = ""

    for i in range(max(len(a), len(b), len(c))):
        if i < len(a):
            subject += a[i]

        if i < len(b):
            subject += b[i]

        if i < len(c):
            subject += c[i]

    subject = subject.lower()

    transmitter = get_component("transmitter")
    transmitter.connect("earth")
    transmitter.transmit(
        self.contract.id,
        subject
    )


main()