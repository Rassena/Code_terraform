shop = get_component("shop")
inventory = get_component("inventory")
exchange = get_component("bio_exchange_1")



def get_next_missing():
    if exchange.active_order():
        for key, item in exchange.active_order().requires.items():
            if inventory.count(key) < item - exchange.active_order().delivered[key]:
                for scan in self.scan():
                    if scan.fragment_id == key:
                        self.collect(scan.coords)
                        return    

def get_next_unknown():
    for scan in self.scan():
        if not scan.cataloged:
            self.collect(scan.coords)


while True:
    if self.cargo is None:
        get_next_missing()
        # get_next_unknown()