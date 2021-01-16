from engine.default import *
from typing import Union
import numpy
import pygame
import os

class _display:
    class _draw:
        def __init__(self, _pygame_display) -> None:
            self._pygame_display = _pygame_display

        def rect(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], size: Union[list, tuple, numpy.array]):
            pygame.draw.rect(self._pygame_display, color, pygame.Rect(position[0], position[1], size[0], size[1]))
        def circle(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], radius: Union[int, float]):
            pygame.draw.circle(self._pygame_display, color, position, radius)
        def line(self, color: Union[list, tuple, numpy.array], start_point: Union[list, tuple, numpy.array], end_point: Union[list, tuple, numpy.array], thickness: Union[int, float]):
            pygame.draw.line(self._pygame_display, color, start_point, end_point, thickness)
        def aaline(self, color: Union[list, tuple, numpy.array], start_point: Union[list, tuple, numpy.array], end_point: Union[list, tuple, numpy.array]):
            pygame.draw.aaline(self._pygame_display, color, start_point, end_point)
        def ellipse(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], size: Union[list, tuple, numpy.array]):
            pygame.draw.ellipse(self._pygame_display, color, pygame.Rect(position[0], position[1], size[0], size[1]))
        def polygon(self, color: Union[list, tuple, numpy.array], points: Union[list, tuple, numpy.array]):
            pygame.draw.polygon(self._pygame_display, color, points)

        def rect_frame(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], size: Union[list, tuple, numpy.array], thickness: Union[int, float]):
            pygame.draw.rect(self._pygame_display, color, pygame.Rect(position[0], position[1], size[0], size[1]), thickness)
        def circle_frame(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], radius: Union[int, float], thickness: Union[int, float]):
            pygame.draw.circle(self._pygame_display, color, position, radius, thickness)
        def ellipse_frame(self, color: Union[list, tuple, numpy.array], position: Union[list, tuple, numpy.array], size: Union[list, tuple, numpy.array], thickness: Union[int, float]):
            pygame.draw.ellipse(self._pygame_display, color, pygame.Rect(position[0], position[1], size[0], size[1]), thickness)
        def polygon_frame(self, color: Union[list, tuple, numpy.array], points: Union[list, tuple, numpy.array], thickness: Union[int, float]):
            pygame.draw.polygon(self._pygame_display, color, points, thickness)

    def __init__(self, window) -> None:
        self.fill = window._pygame_display.fill
        self.draw = self._draw(window._pygame_display)
        self.rawdraw = pygame.draw
        self.get_mouse_pos = pygame.mouse.get_pos

class _camera:
    def __init__(self, position: pos2, size: size2) -> None:
        self.position = position
        self.size = size

class Window:
    def __init__(self, size: Union[list, tuple, numpy.array], caption: str, FPS = 30, flags = 0) -> None:
        self._clock = pygame.time.Clock()
        self.FPS = FPS
        self.size = size
        self.caption = caption
        self._pygame_display = pygame.display.set_mode(self.size, flags = flags)
        self.display = _display(self)
        self.camera = _camera(pos2(), size2(1, 1))
        self._event_list = []
        self.pressedKeys = {}
        self.justpressedKeys = {}

        pygame.display.set_caption(caption)
        self.set_caption = pygame.display.set_caption
        self.get_fps = self._clock.get_fps

        if os.name != "nt":
            self.get_screen_size = pygame.display.get_window_size
        else:
            def get_screen_size(self): return self.size
            self.get_screen_size = lambda: get_screen_size(self)

    def is_holding(self, key) -> bool:
        if key in self.pressedKeys:
            return self.pressedKeys[key]
        return False

    def is_just_tapped(self, key) -> bool:
        return key in self.justpressedKeys

    def get_event_list(self):
        event_list = pygame.event.get()
        self.justpressedKeys = {}
        for event in event_list:
            if event.type == pygame.QUIT: exit(0)
            elif event.type == pygame.KEYDOWN:
                self.pressedKeys[event.key] = True
                self.justpressedKeys[event.key] = True
            elif event.type == pygame.KEYUP: self.pressedKeys[event.key] = False

        return event_list

    def win_size_update(self):
        self.size = self.get_screen_size()


    def update(self):
        self.win_size_update()
        event_list = self.get_event_list()
        if event_list != []: self._event_list = event_list

        pygame.display.flip()
        self._clock.tick(self.FPS)
        return event_list
