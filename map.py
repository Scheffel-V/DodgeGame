import config
import rectangle
import pygame

class Map(rectangle.Rectangle):
    def __init__(self, width, height, image):
        super(Map, self).__init__((0, 0), width, height, image)
