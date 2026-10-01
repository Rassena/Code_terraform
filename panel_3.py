import cStorage as cStor

TEXT_SIZE = 11

LABEL_MARGIN_X = 10
LABEL_MARGIN_Y = 20

NAME_MARGIN = 10
NEXT_COLUMN_MARGIN = 240
STATUS_MARGIN = 200

Y_ROW = 50
INLINE_SPACE=20

CHANGE_PAGE_TIME = 5
ITEMS_PER_COLUMN = 15


while True:

    for type in ["minerals", "materials", "products"]:
        panel.clear()
        panel.label(LABEL_MARGIN_X, LABEL_MARGIN_Y, f"Warehouse {type}", "caption")

        get_items = getattr(
            cStor,
            f"get_items_warehouses_{type}_outpost",
        )

        for i, (item_id, val) in enumerate(
            get_items("outpost_home").items()
        ):
            x = NAME_MARGIN if i <= ITEMS_PER_COLUMN else NEXT_COLUMN_MARGIN
            row = i if i <= ITEMS_PER_COLUMN else i - (ITEMS_PER_COLUMN + 1)
            y = Y_ROW + row * INLINE_SPACE
            
            panel.draw_text(x, y, f"{item_id}", TEXT_SIZE)
            panel.draw_text(x + STATUS_MARGIN, y, str(val), TEXT_SIZE)
        sleep(CHANGE_PAGE_TIME)
        