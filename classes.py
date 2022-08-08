import random

import pygame


class Point:
    radius = 7

    def __init__(self, master, x, y, color, head=None):
        self.master = master
        if x is not None:
            self.x = x
            self.y = y
        self.color = color
        self.head: Point = head

        self.dragging = False

    @property
    def rect(self):
        _rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        return _rect

    @property
    def pos(self):
        return self.x, self.y

    def detect_drag(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.dragging = True

    def draw(self):
        if self.dragging:
            self.x, self.y = pygame.mouse.get_pos()

        if self.head:
            pygame.draw.line(self.master, self.color, self.pos, self.head.pos)
        pygame.draw.circle(self.master, self.color, self.pos, self.radius)

    def __str__(self):
        return f"X:{self.x}, Y:{self.y}"


class LerpPoint(Point):
    color_depth_dict = {
        0: [255, 0, 0]
    }
    radius = 3

    def __init__(self, master, p1, p2, t, color, depth, x=None, y=None):
        super().__init__(master, x, y, color)

        self.p1 = p1
        self.p2 = p2
        self.t = t
        self.depth = depth

    @property
    def x(self):
        return self.p1.x + self.t * (self.p2.x - self.p1.x)

    @property
    def y(self):
        return self.p1.y + self.t * (self.p2.y - self.p1.y)

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, var):
        pass

    def draw(self, tval=None):
        tval = tval if tval else self.t
        self.t = tval

        if self.head:
            pygame.draw.line(self.master, self.color_depth_dict[self.depth], self.pos, self.head.pos)
        pygame.draw.circle(self.master, self.color_depth_dict[self.depth], self.pos, self.radius)

    def get_pos_from_t(self, tval):
        if not isinstance(self.p1, LerpPoint):
            p_x = self.p1.x + tval * (self.p2.x - self.p1.x)
            p_y = self.p1.y + tval * (self.p2.y - self.p1.y)
            return p_x, p_y

        p1_x, p1_y = self.p1.get_pos_from_t(tval)
        p2_x, p2_y = self.p2.get_pos_from_t(tval)
        return p1_x + tval * (p2_x - p1_x), p1_y + tval * (p2_y - p1_y)

    def set_drawing(self):
        self.depth = 0
        self.radius = 7

    def detect_drag(self):
        pass

    @classmethod
    def add_depth_color(cls, depth_key):
        _col = [random.randint(0, 255) for _ in range(3)]
        cls.color_depth_dict.update({depth_key: _col})
        pass
