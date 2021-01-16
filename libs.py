import engine
import pygame
import numpy
import time
import random

pygame.init()
pygame.font.init()

win_size = 1280, 720
win_caption = "hello"

class Image(engine.objects.Rectangular_obj):
    def __init__(self, window: engine.Window, position, size, path) -> None:
        self.position = engine.default.pos2(position[0], position[1], numpy.int32)
        self.size = engine.default.size2(size[0], size[1], numpy.float32)
        self.path = path
        self.is_mouse_holding = False
        self.window = window
        self.first_calculation()

    def first_calculation(self):
        img = pygame.image.load(self.path)
        pos, size = self.get_projection()
        pos = pos.astype("int32")
        self.img = pygame.transform.scale(img, size.astype("int32"))

    def draw(self):
        pos, size = self.get_projection()
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.window._pygame_display.blit(self.img, self.rect)

class DirtBlock(Image):
    def __init__(self, main, position) -> None:
        self.main = main
        self.click_time = 0
        self.block_pressed = [False, None]
        super().__init__(main.window, position, [200, 200], "resources/textures/dirt_tile.png")
        
    def calculate_press(self):
        
        for obj_i in range(len(self.main.dirt_block_list)):
            obj = self.main.dirt_block_list[len(self.main.dirt_block_list)-obj_i-1]
            is_mouse_active = max(pygame.mouse.get_pressed())
            is_point_in = engine.objects.is_point_in(numpy.array(self.window.display.get_mouse_pos()), obj, True, engine.objects.Rect)
            if not is_mouse_active:
                if obj.is_mouse_holding:
                    obj.position.x -= 25
                    obj.position.y -= 25
                    obj.size.w += 50
                    obj.size.h += 50
                    obj.first_calculation()
                
                if obj == self.block_pressed[1]:
                    self.block_pressed[0] = False

                obj.is_mouse_holding = False
                
            if is_mouse_active and is_point_in and not obj.is_mouse_holding and not self.block_pressed[0]:
                obj.position.x += 25
                obj.position.y += 25
                obj.size.w -= 50
                obj.size.h -= 50
                obj.first_calculation()
                obj.is_mouse_holding = True
                self.block_pressed = [True, obj]
                self.main.money += self.main.money_per_click * self.main.money_multiplier

        
        
class Text:
    def __init__(self, window: engine.Window, text = "", position = [0, 0], size = 24, color = [255, 255, 255], font = None) -> None:
        self.window = window
        self.position = engine.default.pos2(position[0], position[1])
        self.size = size
        self.text = text
        self.color = color
        self.font = font
        self.update_font()
    
    def update_font(self):
        self._font = pygame.font.Font(self.font, self.size)

    def draw(self):
        render = self._font.render(str(self.text), True, self.color)
        rect = render.get_rect()
        rect.left, rect.top = self.position.getVector()
        self.window._pygame_display.blit(render, rect)

class Stats(engine.objects.Rectangular_obj):
    def __init__(self, window: engine.Window, position, size, text = "") -> None:
        self.window = window
        self.text = text
        self.position = engine.default.pos2(position[0], position[1])
        self.size = engine.default.size2(size[0], size[1])
        self.inner_obj_list = [
            engine.objects.Rect(window, position, size, [64, 64, 64]),
            engine.objects.Rect(window, position, size, [255, 255, 255]),
            Text(self.window, self.text, self.position.getVector(), 24, [128, 128, 128]),
        ]
    
    def draw(self):
        offset = numpy.array([410, 10])
        self.inner_obj_list[0].size, self.inner_obj_list[0].position = self.size, self.position
        self.inner_obj_list[1].size, self.inner_obj_list[1].position = self.size, self.position
        pos = self.position.getVector()+offset
        self.inner_obj_list[2].size, self.inner_obj_list[2].position = self.size, engine.default.pos2(pos[0], pos[1])
        self.inner_obj_list[2].text = self.text
        self.inner_obj_list[0].draw(True)
        self.inner_obj_list[1].draw(True, True)
        self.inner_obj_list[2].draw()

class Reset_button(engine.objects.Rectangular_obj):
    def __init__(self, main, position, size, on_click) -> None:
        self.main = main
        self.position = engine.default.pos2(position[0], position[1])
        self.size = engine.default.size2(size[0], size[1])
        self.on_click = on_click
        self.mouse_started_hold = False
        self.inner_obj_list = [
            engine.objects.Rect(main.window, position, size, [64, 64, 64]),
            engine.objects.Rect(main.window, position, size, [0, 255, 255]),
            Text(main.window, "Reset progress (+1 money mul)", position)
        ]

    def is_mouse_on(self):
        return engine.objects.is_point_in(self.main.window.display.get_mouse_pos(), self.inner_obj_list[0], False)

    def draw(self):
        if self.is_mouse_on():
            self.inner_obj_list[1].color = [0, 255, 0]
        else:
            self.inner_obj_list[1].color = [0, 255, 255]

        self.calculate_click()

        self.inner_obj_list[0].position = self.position
        self.inner_obj_list[0].size = self.size
        self.inner_obj_list[0].draw(True)
        
        self.inner_obj_list[1].position = self.position
        self.inner_obj_list[1].size = self.size
        self.inner_obj_list[1].draw(True, True)
        
        self.inner_obj_list[2].position = engine.default.pos2(self.position.x+10, self.position.y+9)
        self.inner_obj_list[2].draw()

    def calculate_click(self):
        is_mouse_active = max(pygame.mouse.get_pressed())

        if not is_mouse_active and self.mouse_started_hold and self.is_mouse_on():
            self.on_click()

        if not is_mouse_active:
            self.mouse_started_hold = False

        if is_mouse_active and self.is_mouse_on():
            if not self.mouse_started_hold:
                self.mouse_started_hold = True
            self.inner_obj_list[1].color = [0, 100, 0]

class Upgrade_list(engine.objects.Rectangular_obj):

    class Upgrade:
        def __init__(self, title: str, cost: float, on_click, money) -> None:
            self.on_click_event = on_click
            self.title = title
            self.cost = cost
            self.money = money
            self.inner_obj_list = [
                engine.objects.Rect(0, [0, 0], [0, 0], [30, 30, 30]),
                engine.objects.Rect(0, [0, 0], [0, 0], [0, 255, 255]),
                Text(0, title, [0, 0], 24),
                Text(0, "Cost: "+str(cost), [0, 0], 24),
            ]
            self.mouse_started_hold = False

        def _error(self):
            raise NotImplementedError(f"Object '{self}' is not initializated before using")

        def is_mouse_on(self):
            if not hasattr(self, "upgrade_list"): self._error()
            return engine.objects.is_point_in(self.upgrade_list.window.display.get_mouse_pos(), self.inner_obj_list[0], False)

        def get_possize(self):
            self_index = self.upgrade_list.upgrades.index(self)
            pos = self.upgrade_list.position.getVector()
            pos[1] += self_index*110
            size = [self.upgrade_list.size.w, 100]
            return pos, size

        def draw(self):
            if not hasattr(self, "upgrade_list"): self._error()

            
            if self.upgrade_list.main.money >= self.cost:
                if self.is_mouse_on():
                    self.inner_obj_list[1].color = [0, 255, 0]
                else:
                    self.inner_obj_list[1].color = [0, 255, 255]
            else:
                if self.is_mouse_on():
                    self.inner_obj_list[1].color = [127, 0, 0]
                else:
                    self.inner_obj_list[1].color = [255, 0, 0]

            self.calculate_click()

            pos, size = self.get_possize()

            if pos[1]+size[1] >= win_size[1]:
                self.upgrade_list.upgrades.pop(0)
            
            self.inner_obj_list[0].position = engine.default.pos2(pos[0], pos[1])
            self.inner_obj_list[0].size = engine.default.size2(size[0], size[1])
            self.inner_obj_list[0].draw(True)

            self.inner_obj_list[1].position = engine.default.pos2(pos[0], pos[1])
            self.inner_obj_list[1].size = engine.default.size2(size[0], size[1])
            self.inner_obj_list[1].draw(True, True)

            self.inner_obj_list[2].position = engine.default.pos2(pos[0]+10, pos[1]+10)
            self.inner_obj_list[2].draw()

            self.inner_obj_list[3].position = engine.default.pos2(pos[0]+size[0]-40-len(float_to_string_short(self.cost)*10), pos[1]+size[1]-20)
            self.inner_obj_list[3].text = f"Cost: {float_to_string_short(self.cost)}"
            self.inner_obj_list[3].draw()

        def calculate_click(self):
            is_mouse_active = max(pygame.mouse.get_pressed())

            if not is_mouse_active and self.mouse_started_hold and self.is_mouse_on():
                self.on_click()

            if not is_mouse_active:
                self.mouse_started_hold = False

            if is_mouse_active and self.is_mouse_on():
                if not self.mouse_started_hold:
                    self.mouse_started_hold = True
                if self.cost <= self.upgrade_list.main.money:
                    self.inner_obj_list[1].color = [0, 100, 0]
            

        def on_click(self):
            if self.cost <= self.upgrade_list.main.money:
                self.upgrade_list.main.money -= self.cost
                self.on_click_event(self, self.upgrade_list.main, self.money)


        def init(self, upgrade_list):
            for obj in self.inner_obj_list:
                obj.window = upgrade_list.window

            upgrade_list.upgrades.append(self)
            self.upgrade_list = upgrade_list


    def __init__(self, main, position, size) -> None:
        self.main = main
        self.money_counter = main.money_counter
        self.window = main.window
        self.position = engine.default.pos2(position[0], position[1])
        self.upgrades = main.upgrades
        self.size = engine.default.size2(size[0], size[1])
        self.inner_obj_list = [
            engine.objects.Rect(main.window, position, size, [64, 64, 64]),
            engine.objects.Rect(main.window, position, size, [255, 255, 255]),
        ]
    
    def draw(self):
        self.inner_obj_list[0].size, self.inner_obj_list[0].position = self.size, self.position
        self.inner_obj_list[1].size, self.inner_obj_list[1].position = self.size, self.position

        self.inner_obj_list[0].draw(True)
        self.inner_obj_list[1].draw(True, True)

        for upgrade in self.upgrades:
            upgrade.draw()

def float_to_string_short(obj: float):
    obj_strlist = str(obj).split(".")
    if len(obj_strlist) > 1:
        obj = obj_strlist[0]+"."+obj_strlist[1][:2]
    return obj