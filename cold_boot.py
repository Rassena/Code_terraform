def run_program(program):
    memory = program.copy()
    ip = 0
    output = []

    while True:
        instruction = memory[ip]

        opcode = instruction % 100
        mode1 = (instruction // 100) % 10
        mode2 = (instruction // 1000) % 10

        def get_value(offset, mode):
            value = memory[ip + offset]

            if mode == 0:
                return memory[value]
            elif mode == 1:
                return value

            raise ValueError(f"Unknown parameter mode: {mode}")

        if opcode == 99:
            break

        elif opcode == 1:
            a = get_value(1, mode1)
            b = get_value(2, mode2)
            destination = memory[ip + 3]

            memory[destination] = a + b
            ip += 4

        elif opcode == 2:
            a = get_value(1, mode1)
            b = get_value(2, mode2)
            destination = memory[ip + 3]

            memory[destination] = a * b
            ip += 4

        elif opcode == 4:
            value = get_value(1, mode1)
            output.append(value)
            ip += 2

        elif opcode == 5:
            condition = get_value(1, mode1)
            target = get_value(2, mode2)

            if condition != 0:
                ip = target
            else:
                ip += 3

        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    return output


def decode_output(output):
    return "".join(
        chr(ord("A") + value - 1)
        for value in output
    )


def main():
    program = self.contract.program

    output = run_program(program)
    message = decode_output(output)

    transmitter = get_component("transmitter")
    transmitter.connect("earth")
    transmitter.transmit(
        self.contract.id,
        message
    )


main()