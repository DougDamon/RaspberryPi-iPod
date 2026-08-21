import time

import pygame

from common.ui.framebuffer_display import FramebufferDisplay


WIDTH = 320
HEIGHT = 240

BACKGROUND = (0, 0, 0)
TEXT = (235, 235, 235)
SECONDARY_TEXT = (160, 160, 160)
BAR_BACKGROUND = (50, 50, 50)
BAR_FOREGROUND = (220, 220, 220)


pygame.font.init()

surface = pygame.Surface(
    (WIDTH, HEIGHT),
    depth=32,
)

display = FramebufferDisplay()

title_font = pygame.font.Font(None, 28)
body_font = pygame.font.Font(None, 22)
small_font = pygame.font.Font(None, 18)

track_title = "Test Track"
artist = "Test Artist"

duration = 245
position = 0

progress_rect = pygame.Rect(
    25,
    170,
    270,
    12,
)

time_rect = pygame.Rect(
    20,
    190,
    280,
    30,
)

dynamic_rect = progress_rect.union(time_rect)


def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes}:{seconds:02d}"


def draw_static_screen():
    surface.fill(BACKGROUND)

    title_surface = title_font.render(
        track_title,
        True,
        TEXT,
    )

    artist_surface = body_font.render(
        artist,
        True,
        SECONDARY_TEXT,
    )

    surface.blit(
        title_surface,
        (20, 35),
    )

    surface.blit(
        artist_surface,
        (20, 70),
    )

    pygame.draw.polygon(
        surface,
        TEXT,
        [
            (145, 105),
            (145, 145),
            (180, 125),
        ],
    )


def draw_position():
    surface.fill(
        BACKGROUND,
        dynamic_rect,
    )

    pygame.draw.rect(
        surface,
        BAR_BACKGROUND,
        progress_rect,
    )

    progress_width = int(
        progress_rect.width
        * position
        / duration
    )

    if progress_width > 0:
        filled_rect = pygame.Rect(
            progress_rect.x,
            progress_rect.y,
            progress_width,
            progress_rect.height,
        )

        pygame.draw.rect(
            surface,
            BAR_FOREGROUND,
            filled_rect,
        )

    elapsed_surface = small_font.render(
        format_time(position),
        True,
        TEXT,
    )

    duration_surface = small_font.render(
        format_time(duration),
        True,
        TEXT,
    )

    surface.blit(
        elapsed_surface,
        (
            progress_rect.left,
            192,
        ),
    )

    surface.blit(
        duration_surface,
        (
            progress_rect.right
            - duration_surface.get_width(),
            192,
        ),
    )


draw_static_screen()
draw_position()

display.update_full(surface)

print("Initial screen drawn.")
print("Press Ctrl+C to stop.")

try:
    while True:
        time.sleep(1)

        position += 1

        if position > duration:
            position = 0

        draw_position()

        display.update(
            surface,
            dynamic_rect,
        )

except KeyboardInterrupt:
    pass

finally:
    display.close()
    pygame.quit()
