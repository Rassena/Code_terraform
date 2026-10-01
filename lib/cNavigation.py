journal = get_component("journal")
planet = get_component("nocturna")


def calc_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return (x2 - x1) ** 2 + (y2 - y1) ** 2
    
def get_sites() -> list[Site]:
    return journal.discovered_sites("nocturna")

def get_sites_type(site_kind: str) -> list[Site]:
    return [
        site
        for site in get_sites()
        if site.kind() == site_kind
    ]

def get_sites_mineral() -> list[MiningSite]:
    return [site for site in get_sites_type("mineral")]

def get_sites_mineral_with_item(item_id:str)-> list[MiningSite]:
    return [
        site
        for site in get_sites_mineral()
        if site.item_id == item_id
    ]

def get_nearest_construction(constructions:list[Construction], x:float, y:float)->Construction | None:

    if not constructions:
        return None

    return min(
        constructions,
        key=lambda construction: (
            (construction.position.x - x) ** 2
            + (construction.position.y - y) ** 2
        )
    )

def get_nearest_site_mineral(item_id:str, x:float, y:float) -> MiningSite | None:
    mining_sites = get_sites_mineral_with_item(item_id)
    
    if not mining_sites:
        return None

    return min(
        mining_sites,
        key=lambda mining_site: (
            (mining_site.x - x) ** 2
            + (mining_site.y - y) ** 2
        )
    )

def get_points_of_interest() -> list[PointOfInterest]:
    return planet.points_of_interest()

def get_points_of_interest_scanned():
    return [
        point_of_interest
        for point_of_interest
        in planet.points_of_interest()
        if point_of_interest.scanned
    ]
    
def get_points_of_interest_not_scanned():
    return [
        point_of_interest
        for point_of_interest
        in planet.points_of_interest()
        if not point_of_interest.scanned
    ]

def get_nearest_points_of_interest_not_scanned(x:float, y:float) -> PointOfInterest:
    points_of_interest = get_points_of_interest_not_scanned()
    
    if not points_of_interest:
        return None

    return min(
        points_of_interest,
        key=lambda point_of_interest: (
            (point_of_interest.X - x) ** 2
            + (point_of_interest.y - y) ** 2
        )
    )

def get_points_of_interest_dict() -> dict[str,list[PointOfInterest]]:
    points_of_interest = get_points_of_interest()

    points_of_interest_dict = {}
    
    for point_of_interest in points_of_interest:
        points_of_interest_dict[point_of_interest.kind] = points_of_interest_dict.get(point_of_interest.kind,[]) + [point_of_interest]
        
    return points_of_interest_dict


def generate_positions_to_scan(min_x:int, max_x:int, min_y:int, max_y:int, distance:int) -> list[tuple[int,itn]]:
    positions_to_scan = []
    for x in range(min_x,max_x+1,distance):
        for y in range(min_y,max_y+1,distance):
            positions_to_scan.append((x,y))
    return positions_to_scan