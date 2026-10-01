import cNavigation as cNav

construction_blueprint = get_component("construction_blueprint")


def print_pending_constructions():
    for kind, val_dict in get_dict_pending_contructions().items():
        print(f"{kind}:")
        for required_item, blue_vals in val_dict.items():
            print(f"\t{required_item}")
            for blue_val in blue_vals:
                print(f"\t\t{blue_val}")
    return


def get_dict_pending_contructions(list_contructions:list[Construction]=None)-> dict[str,dict[str,tuple[Position,int]]]:
    
    if list_contructions is None:
        list_contructions =construction_blueprint.pending_constructions() + construction_blueprint.paused_constructions()
    
    pending_contructions = {}
    for pending in list_contructions:
        pending_contructions[pending.kind] = {
            pending.required_item:
                pending_contructions.get(pending.kind,{}).get(pending.required_item,[]) + [(pending.position,pending.required_count)],
        }

    return pending_contructions


def get_required_items(list_contructions:list[Construction]=None) -> dict[str,int]:
        
    if list_contructions is None:
        list_contructions =construction_blueprint.pending_constructions() + construction_blueprint.paused_constructions()
  
    required_items = {}
    for pending in list_contructions:
        required_items[pending.required_item] = required_items.get(pending.required_item,0) + pending.required_count
    return required_items

def pending_contructions_required_item(required_item:str,list_contructions:list[Construction]=None) -> lsit[Construction]:
            
    if list_contructions is None:
        list_contructions =construction_blueprint.pending_constructions() + construction_blueprint.paused_constructions()
    
    return [
        construction
        for construction 
        in list_contructions
        if construction.required_item == required_item
    ]

def get_nearest_construction_by_required_item(required_item:str,x:float,y:float,list_contructions:list[Construction]=None) -> Construction:
    return cNav.get_nearest_construction(pending_contructions_required_item(required_item,list_contructions),x,y)