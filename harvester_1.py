scanner = get_component("scanner_1")

HEAT_BUFFER = 10

def heat_management():
    while  self.get_heat() >= self.get_max_heat() - HEAT_BUFFER:
        sleep(get_component("clock").real_seconds_per_hour() * 1)


def get_not_empty():
    result = scanner.get_scanned()
    for key, item in result.items():
        if item.status == "empty":
            result.pop(key)
    return result
        

def get_not_scanned() -> dict[str,ScanResult]:
    result = scanner.get_scanned()
    for key, item in result.items():
        if item.status == "ok":
            result.pop(key)
    return result
        
def get_next_not_empty(scanned):
    key, item = scanned.popitem()
    while item.status == "empty" and scanned.length>0:
        key, item = scanned.popitem()
    return key, item

def move_to_next():
    scanned = scanner.get_scanned()
    key, item = get_next_not_empty(scanned)
    target_x = key[0]
    target_y = key[1:]
    
    print("Move Next:", target_x,target_y)
    move_to(target_x, target_y)

def move_to_nearest_item():
    key, item = get_nearest_item()

    target_x = key[0]
    target_y = key[1:]
    if key == self.get_position():
        print("Already at:",key)
    else:
        print("Move nearest:", key)
        move_to(target_x, target_y)

def move_to_nearest_not_scanned():
    key, item = get_nearest_not_scanned()

    target_x = key[0]
    target_y = key[1:]
    if key == self.get_position():
        print("Already at:",key)
    else:
        print("Move nearest:", key)
        move_to(target_x, target_y)

def move_to(target_x, target_y):
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]
    
    while current_x != target_x:
        heat_management()
        if ord(current_x) < ord(target_x):
            self.move(str(chr(ord(current_x)+1)+current_y))
        else:
            self.move(str(chr(ord(current_x)-1)+current_y))
        current_x = self.get_position()[0]
        current_y = self.get_position()[1:]

    while current_y != target_y:
        heat_management()
        if int(current_y) < int(target_y):
            self.move(current_x+str(int(current_y)+1))
        else:
            self.move(current_x+str(int(current_y)-1))
        current_x = self.get_position()[0]
        current_y = self.get_position()[1:]


def get_nearest_item():
    scanned = get_not_empty()
    
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]

    nearest = inf
    nearest_key:str
    nearest_item:ScanResult
    
    while scanned.length > 0 :
        key, item = get_next_not_empty(scanned)
        target_x = key[0]
        target_y = key[1:]

        dist = abs(ord(target_x) - ord(current_x)) + abs(int(target_y)-int(current_y))
    
        if dist < nearest:
            nearest=dist
            nearest_key=key
            nearest_item=item

    return nearest_key, nearest_item

def get_nearest_not_scanned():
    not_scanned = get_not_scanned()
    
    current_x = self.get_position()[0]
    current_y = self.get_position()[1:]

    nearest = inf
    nearest_key:str
    nearest_item:ScanResult
    
    while not_scanned.length > 0 :
        key, item = get_next_not_empty(not_scanned)
        target_x = key[0]
        target_y = key[1:]

        dist = abs(ord(target_x) - ord(current_x)) + abs(int(target_y)-int(current_y))
    
        if dist < nearest:
            nearest=dist
            nearest_key=key
            nearest_item=item

    return nearest_key, nearest_item

# while True:
        
#     heat_management()
    
#     # if(get_not_scanned().length > 0):
#     #     move_to_nearest_not_scanned()
#     if(get_not_empty().length > 0):
#         move_to_nearest_item()
#         self.collect()
#         self.store()

move_to("E","13")
# print(self.cell(self.get_position()))

# self.collect()




























