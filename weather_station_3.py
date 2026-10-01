
clock = get_component("clock")

def observe():
    if self.last_report().age_gh() > 1:
        self.observe()

printed = False
self.signal_board.clear()
while True:
    self.observe()

    transmissions = self.signal_receiver.transmissions()

    if transmissions and not printed:
        printed = True
        for trans in transmissions:
            checksum = sum(
                ord(
                    str(
                        char
                    )
                ) for char in trans.data)
            # print(checksum)
            if checksum == trans.checksum:
                self.signal_board.reveal(trans)
                print(
                    trans.number,
                    trans.event_id,
                    trans.data,
                    trans.checksum,
                    trans.channel,
                    checksum
                )
            else:
                print("\t\t",
                    trans.number,
                    trans.event_id,
                    trans.data,
                    trans.checksum,
                    trans.channel,
                    checksum
                )
                self.signal_board.reject(trans)
    if not transmissions:
        printed = False
    sleep(1)
















    