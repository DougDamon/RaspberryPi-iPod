import mmap

import pygame


class FramebufferDisplay:
    def __init__(
        self,
        device="/dev/fb0",
        width=320,
        height=240,
        bits_per_pixel=32,
        stride=1280,
    ):
        self.device = device
        self.width = width
        self.height = height
        self.bits_per_pixel = bits_per_pixel
        self.bytes_per_pixel = bits_per_pixel // 8
        self.stride = stride
        self.size = stride * height

        self.file = open(
            self.device,
            "r+b",
            buffering=0,
        )

        self.fb = mmap.mmap(
            self.file.fileno(),
            self.size,
            mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE,
        )

    def update(self, surface, rect):
        rect = pygame.Rect(rect)

        region = surface.subsurface(rect)

        pixel_data = pygame.image.tobytes(
            region,
            "BGRA",
        )

        source_stride = rect.width * self.bytes_per_pixel

        for row in range(rect.height):
            source_start = row * source_stride
            source_end = source_start + source_stride

            framebuffer_start = (
                (rect.y + row) * self.stride
                + rect.x * self.bytes_per_pixel
            )

            framebuffer_end = (
                framebuffer_start + source_stride
            )

            self.fb[
                framebuffer_start:framebuffer_end
            ] = pixel_data[
                source_start:source_end
            ]

    def update_many(self, surface, rects):
        for rect in rects:
            self.update(surface, rect)

    def update_full(self, surface):
        self.update(
            surface,
            pygame.Rect(
                0,
                0,
                self.width,
                self.height,
            ),
        )

    def close(self):
        if self.fb is not None:
            self.fb.close()
            self.fb = None

        if self.file is not None:
            self.file.close()
            self.file = None
