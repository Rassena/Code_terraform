import cNavigation as cNav

TEXT_SIZE = 11

LABEL_MARGIN_X = 10
LABEL_MARGIN_Y = 20

NAME_MARGIN = 10
STATUS_MARGIN = 120

TABLE_OFFSET = 240

Y_ROW = 50
INLINE_SPACE=20


clock = get_component("clock")


print_data = {
    "All": cNav.get_points_of_interest(),
    "Scanned": cNav.get_points_of_interest_scanned(),
    "Not Scanned": cNav.get_points_of_interest_not_scanned()
}

print(cNav.get_points_of_interest_dict())

while True:

    panel.clear()
    panel.label(LABEL_MARGIN_X, LABEL_MARGIN_Y, f"Tasks Vehicle", "caption")

    for i, (type, points_of_interest) in enumerate(print_data.items()):
        x = NAME_MARGIN
        y = Y_ROW + i * INLINE_SPACE
        
        panel.draw_text(x, y, f"{type}", TEXT_SIZE)
        panel.draw_text(x + STATUS_MARGIN, y, str(len(points_of_interest)), TEXT_SIZE)
    
    for i, (kind, points_of_interest) in enumerate(cNav.get_points_of_interest_dict().items()):
        x = TABLE_OFFSET + NAME_MARGIN
        y = Y_ROW + i * INLINE_SPACE
        
        panel.draw_text(x, y, f"{kind}", TEXT_SIZE)
        panel.draw_text(x + STATUS_MARGIN, y, str(len(points_of_interest)), TEXT_SIZE)

    
    sleep(clock.real_seconds_per_hour())













        