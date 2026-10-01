TEXT_SIZE = 11
DOT_SIZE = 3
MARGIN = 20
NAME_MARGIN = 30
STATUS_MARGIN = 120
COORDS_MARGIN = 200
Y_ROW = 50
INLINE_SPACE=20
BAR_MARGIN = 360
BAR_W = 110
BAR_H = 10

fleet = get_component("fleet")

while True:

    panel.clear()
    panel.label(12, MARGIN, "FLEET PIONEERS", "caption")

    for i,pioneer_ref in enumerate(
        vehicle_ref 
        for vehicle_ref in fleet.vehicles() 
        if vehicle_ref.kind == "pioneer"
    ):
        y_row = Y_ROW + i*INLINE_SPACE
        panel.status_dot(MARGIN, y_row, DOT_SIZE, "running")
        panel.draw_text(NAME_MARGIN, y_row, pioneer_ref.name, TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN, y_row, pioneer_ref.status, TEXT_SIZE)
        panel.draw_text(
            COORDS_MARGIN,
            y_row,
            f"x={pioneer_ref.x:.2f}, y={pioneer_ref.y:.2f}",
            TEXT_SIZE)
        panel.progress_bar(BAR_MARGIN, y_row, BAR_W, BAR_H, pioneer_ref.battery_level, "success")
        