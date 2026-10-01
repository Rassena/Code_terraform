A = 65
H = 72

X_MIN = A
X_MAX = H
Y_MIN = 1
Y_MAX = 24

def scan_all_sectors():
    for x in range(X_MIN,X_MAX+1):
        for y in range(Y_MIN,Y_MAX+1):
            sector = chr(x) + str(y)
            result = self.scan(sector)
            print(sector, ":", result.status, result.name, result.value)



def print_scanned():
    for key, value in self.get_scanned().items():
        print(key, value)



def get_not_empty() -> dict:
    result = self.get_scanned()
    for key, value in result.items():
        if value.status == "empty":
            result.pop(key)
    return result
            

def print_not_empty():
    for key, value in get_not_empty().items():
        print(key, value.name, value.value)


scan_all_sectors()






















