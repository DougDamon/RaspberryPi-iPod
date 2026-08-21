import time

import pygame

from common.ui.framebuffer_display import FramebufferDisplay


WIDTH = 320
HEIGHT = 240

BACKGROUND = (0, 0, 0)
TEXT = (235, 235, 235)
SECONDARY_TEXT = (160, 160, 160)
SELECTION = (70, 70, 70)

ROW_HEIGHT = 28
LIST_TOP = 24
LIST_LEFT = 12
LIST_WIDTH = 296
VISIBLE_ROWS = 7


pygame.font.init()

surface = pygame.Surface(
    (WIDTH, HEIGHT),
    depth=32,
)

display = FramebufferDisplay()

font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 18)


items = [
    "Playlist 01",
    "Playlist 02",
    "Playlist 03",
    "Playlist 04",
    "Playlist 05",
    "Playlist 06",
    "Playlist 07",
    "Playlist 08",
    "Playlist 09",
    "Playlist 10",
    "Playlist 11",
    "Playlist 12",
    "Playlist 13",
    "Playlist 14",
    "Playlist 15",
]


selected_index = 0
first_visible_index = 0


list_rect = pygame.Rect(
    LIST_LEFT,
    LIST_TOP,
    LIST_WIDTH,
    ROW_HEIGHT * VISIBLE_ROWS,
)


def update_visible_window():
    global first_visible_index

    if selected_index < first_visible_index:
        first_visible_index = selected_index

    elif selected_index >= first_visible_index + VISIBLE_ROWS:
        first_visible_index = (
            selected_index - VISIBLE_ROWS + 1
        )


def draw_screen():
    surface.fill(BACKGROUND)

    visible_items = items[
        first_visible_index:
        first_visible_index + VISIBLE_ROWS
    ]

    for row, item in enumerate(visible_items):
        item_index = first_visible_index + row

        y = LIST_TOP + row * ROW_HEIGHT

        row_rect = pygame.Rect(
            LIST_LEFT,
            y,
            LIST_WIDTH,
            ROW_HEIGHT,
        )

        if item_index == selected_index:
            pygame.draw.rect(
                surface,
                SELECTION,
                row_rect,
            )

        label = font.render(
            item,
            True,
            TEXT,
        )

        surface.blit(
            label,
            (
                LIST_LEFT + 8,
                y + 5,
            ),
        )

    position_text = small_font.render(
        f"{selected_index + 1} / {len(items)}",
        True,
        SECONDARY_TEXT,
    )

    surface.blit(
        position_text,
        (
            WIDTH - position_text.get_width() - 10,
            220,
        ),
    )


def refresh():
    draw_screen()
    display.update_full(surface)


draw_screen()
display.update_full(surface)

print("Scrolling list test")
print("j = down")
print("k = up")
print("q = quit")

try:
    while True:
        command = input("> ").strip().lower()

        if command == "q":
            break

        elif command == "j":
            if selected_index < len(items) - 1:
                selected_index += 1

        elif command == "k":
            if selected_index > 0:
                selected_index -= 1

        update_visible_window()
        refresh()

except KeyboardInterrupt:
    pass

finally:
    display.close()
    pygame.quit()
