def escape_vault(contract):
    vault = contract.vault

    directions = {
        "north": (-1, 0),
        "south": (1, 0),
        "east": (0, 1),
        "west": (0, -1),
    }

    opposite = {
        "north": "south",
        "south": "north",
        "east": "west",
        "west": "east",
    }

    visited = set()

    def dfs():
        pos = vault.position
        current = (pos.row, pos.col)

        visited.add(current)

        for direction, (dr, dc) in directions.items():
            pos = vault.position
            next_cell = (pos.row + dr, pos.col + dc)

            if next_cell in visited:
                continue

            result = vault.move(direction)

            if result.status == "exit":
                return True

            if result.status == "wall":
                continue

            if dfs():
                return True

            # Backtrack
            vault.move(opposite[direction])

        return False

    if not dfs():
        print("Could not find the exit")
        return

    escape = vault.escape()

    if escape.status != "ok":
        print(escape.message)
        return

    transmitter = get_component("transmitter")
    transmitter.connect("earth")
    transmitter.transmit(contract.id, escape.key)

    print("Vault escaped!")


def main():
    contract = self.contract
    escape_vault(contract)


main()