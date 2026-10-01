lock = self.contract.lock
lock_state=[0, 0, 0, 0, 0, 0]
wanted_result = [True, True, True, True, True, True]

def brute_force(lock:RelayLock):

    result = lock.intercept(lock_state)
    while result != wanted_result:
        for i in range(len(lock_state)):
            result = lock.intercept(lock_state)
            if not result[i]:
               lock_state[i]+=1
        # print(lock_state)

brute_force(lock)
transmitter = get_component("transmitter")
transmitter.connect("earth")
transmitter.transmit(self.contract.id, lock_state)