terminal = self.contract.terminal

guess = [1 for _ in range(15)]
MIN = 1
MAX = 5


def dumb_solver(guess):
    solution = guess.copy()
    for i in range(len(guess)):
        guess = solution.copy()
        for x in range(MIN,MAX+1):
            guess[i]=x
            if terminal.guess(guess).correct > terminal.guess(solution).correct:
                solution[i]=x
    return solution



transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, dumb_solver(guess))
