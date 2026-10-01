import cStorage as cStor

STORAGE_MAX = 1500
SPLIT_IRON_MINE = 5

TEXT_SIZE = 11
DOT_SIZE = 3
MARGIN = 20
NAME_MARGIN = 30
STATUS_MARGIN = 60
Y_ROW = 50
INLINE_SPACE=20
BAR_MARGIN = 360
BAR_W = 110
BAR_H = 10

CONSTRUCTION_VECHICLES = 2

THERMAL_CAPS = [
    get_component("thermal_cap_1"),
    # get_component("thermal_cap_2")
]
GAS_TANKS_STEAM = [
    get_component("gas_tank_1")
]

# def set_steam_intake():
#     for gas_tank in GAS_TANKS_STEAM:
#         pass
        
# set_steam_intake()


while True:
    
    panel.clear()
    panel.label(12, MARGIN, "STEAM", "caption")

       
    for i, thermal_cap in enumerate(
        THERMAL_CAPS
    ):
        panel.draw_text(NAME_MARGIN, Y_ROW + i*INLINE_SPACE, thermal_cap.id, TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*2, Y_ROW + i*INLINE_SPACE, str(thermal_cap.phase()), TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*3, Y_ROW + i*INLINE_SPACE, str(f"{thermal_cap.capture_rate():.2f}"), TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*4, Y_ROW + i*INLINE_SPACE, f"{thermal_cap.pressure()*100:.2f}%", TEXT_SIZE)


    
    for i, gas_tank in enumerate(
        GAS_TANKS_STEAM
    ):
        # print(gas_tank.fill_pct(),gas_tank.level(),gas_tank.inflow_rate())
        i += THERMAL_CAPS.length
        panel.draw_text(NAME_MARGIN, Y_ROW + i*INLINE_SPACE, gas_tank.id, TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*2, Y_ROW + i*INLINE_SPACE, f"{gas_tank.inflow_rate():.2f}", TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*3, Y_ROW + i*INLINE_SPACE, f"{gas_tank.outflow_rate():.2f}", TEXT_SIZE)
        panel.draw_text(STATUS_MARGIN*4, Y_ROW + i*INLINE_SPACE, f"{gas_tank.fill_pct()*100:.2f}%", TEXT_SIZE)
        # panel.draw_text(STATUS_MARGIN*3, Y_ROW + i*INLINE_SPACE, gas_tank, TEXT_SIZE)
        # panel.draw_text(STATUS_MARGIN*4, Y_ROW + i*INLINE_SPACE, str(thermal_cap.pressure()), TEXT_SIZE)
        
    

















        