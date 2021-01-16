from typing import Union

from engine.default import *
from engine.window import Window
from numpy import array
from math import sqrt

def distance(point1: array, point2: array) -> float: return sqrt(sum(point1-point2**2))

def getPointProjection(point, win: Window):
    return (point-win.camera.position.getVector())/win.camera.size.getVector()+array(win.size)/2

# def getPointUnProjection(point, win: Window):
#     # return (point-win.camera.position.getVector())/win.camera.size.getVector()+array(win.size)/2
#     return (point-array(win.size))/2*win.camera.size.getVector()+win.camera.position.getVector()

class Rectangular_obj:
    def get_projection(self, out_dtype = None):
        pos = getPointProjection(self.position.getVector(), self.window)
        size = self.size.getVector()/self.window.camera.size.getVector()+1
        return pos, size

class Rect(Rectangular_obj):
    def __init__(self, window: Window, position: Union[list, tuple, array], size: Union[list, tuple, array], color = [255, 255, 255]) -> None:
        self.window = window
        self.position = pos2(position[0], position[1])
        self.size = size2(size[0], size[1])
        self.color = color
    
    def draw(self, projected = False, frame = False, thickness = 5):
        if projected: pos, size = self.position.getVector(), self.size.getVector()
        else: pos, size = self.get_projection()
        if frame:
            self.window.display.draw.rect_frame(self.color, pos, size, thickness)
        else:
            self.window.display.draw.rect(self.color, pos, size)


class Ellipse(Rectangular_obj):
    def __init__(self, window: Window, position: Union[list, tuple, array], size: Union[list, tuple, array], color = [255, 255, 255]) -> None:
        self.window = window
        self.position = pos2(position[0], position[1])
        self.size = size2(size[0], size[1])
        self.color = color
    
    def draw(self, projected = False, frame = False, thickness = 5):
        if projected: pos, size = self.position.getVector(), self.size.getVector()
        else: pos, size = self.get_projection()
        if frame:
            self.window.display.draw.ellipse_frame(self.color, pos, size, thickness)
        else:
            self.window.display.draw.ellipse(self.color, pos, size)

class Circle:
    def __init__(self, window: Window, position: Union[list, tuple, array], radius: Union[int, float], color = [255, 255, 255]) -> None:
        self.window = window
        self.position = pos2(position[0], position[1])
        self.radius = radius
        self.color = color
    
    def draw(self, projected = False, frame = False, thickness = 5):
        if projected: pos, size = self.position.getVector()-self.radius, self.radius*2
        else: pos, size = self.get_projection()
        if frame:
            self.window.display.draw.ellipse_frame(self.color, pos, size, thickness)
        else:
            self.window.display.draw.ellipse(self.color, pos, size)

    def get_projection(self):
        pos = getPointProjection(self.position.getVector()-self.radius, self.window)
        size = 2*self.radius/self.window.camera.size.getVector()
        return pos, size

def is_point_in(point, obj, projected = True, obj_as_class = ...) -> bool:
    if obj_as_class == ...:

        if projected: pos, size = obj.get_projection()
        else:
            if obj.__class__ == Rect or obj.__class__ == Ellipse: pos, size = obj.position.getVector(), obj.size.getVector()
            elif obj.__class__ == Circle: pos, size = obj.position.getVector()-obj.radius, array([obj.radius*2, obj.radius*2])
            else: raise ValueError

        if obj.__class__ == Rect:
            if point[0] >= pos[0] and point[0] <= pos[0]+size[0]:
                if point[1] >= pos[1] and point[1] <= pos[1]+size[1]:
                    return True
            return False
        elif obj.__class__ == Ellipse or Circle:
            c, d = pos
            w, h = size
            x1, y1 = point
            a, b = w/2, h/2
        
            try:
                y2 = sqrt((-(x1-a-c)**2/a**2+1)*b**2)+d+b
                y3 = -sqrt((-(x1-a-c)**2/a**2+1)*b**2)+d+b
            except: return False
            return y2>=y1 and y3<=y1
    elif obj_as_class == Rect:
        if projected: pos, size = obj.get_projection()
        else:
            pos, size = obj.position.getVector(), obj.size.getVector()

        if point[0] >= pos[0] and point[0] <= pos[0]+size[0]:
            if point[1] >= pos[1] and point[1] <= pos[1]+size[1]:
                return True
        return False
    elif obj_as_class == Ellipse:
        if projected: pos, size = obj.get_projection()
        else:
            pos, size = obj.position.getVector()-obj.radius, array([obj.radius*2, obj.radius*2])

        c, d = pos
        w, h = size
        x1, y1 = point
        a, b = w/2, h/2
    
        try:
            y2 = sqrt((-(x1-a-c)**2/a**2+1)*b**2)+d+b
            y3 = -sqrt((-(x1-a-c)**2/a**2+1)*b**2)+d+b
        except: return False
        return y2>=y1 and y3<=y1
        

    else: raise ValueError

