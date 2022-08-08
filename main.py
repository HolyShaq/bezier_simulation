from classes import *
from typing import List
import control_panel
import pygame
import sys


def iterecurse_points(_points: List[Point], depth):
    if len(_points) <= 1:
        return []

    _lerp_points = []
    for i, point in enumerate(_points[:-1]):
        p1 = point
        p2 = _points[i + 1]
        p1.head = p2

        _lerp_points.append(LerpPoint(window, p1, p2, window_controls.global_t, WHITE, depth))
    children_lerps = iterecurse_points(_lerp_points, depth+1)
    _lerp_points.extend(children_lerps)

    return _lerp_points


pygame.init()
FPS = 60
clock = pygame.time.Clock()

# Setup window
window_width = 1000
window_height = 800
window = pygame.display.set_mode((window_width, window_height))
title = "Bezier Simulation"
pygame.display.set_caption(title)

# Colors
WHITE = pygame.color.Color("white")
RED = pygame.color.Color("red")

# Setup
window_controls = control_panel.ControlPanel()
points = [
    Point(window, 300, 400, WHITE),
    Point(window, 700, 400, WHITE)
]
window_controls.update_levels(LerpPoint.color_depth_dict, len(points))

# Initialize lerp points
lerp_points = iterecurse_points(points, 1)
drawing_point = lerp_points[-1]
drawing_point.set_drawing()

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                [point.detect_drag() for point in points]

            if event.button == 2:
                mouse_pos = pygame.mouse.get_pos()
                points.append(Point(window, *mouse_pos, WHITE, 0))

                # Set random color for new depth
                if not len(points)-2 in LerpPoint.color_depth_dict.keys():
                    LerpPoint.add_depth_color(len(points)-2)
                lerp_points = iterecurse_points(points, 1)
                drawing_point = lerp_points[-1]
                drawing_point.set_drawing()
                window_controls.update_levels(LerpPoint.color_depth_dict, len(points))

            if event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                for point in points:
                    if point.rect.collidepoint(mouse_pos):
                        points.remove(point)
                        points[-1].head = None
                        lerp_points = iterecurse_points(points, 1)
                        drawing_point = lerp_points[-1]
                        drawing_point.set_drawing()
                        window_controls.update_levels(LerpPoint.color_depth_dict, len(points))
                        break

        if event.type == pygame.MOUSEBUTTONUP:
            for point in points:
                point.dragging = False

    window.fill(pygame.Color("black"))

    # Draw anchor points
    [point.draw() for point in points]

    # Animate Interpolation
    if window_controls.interp_mode.get() == 0:
        window_controls.global_t += window_controls.interp_speed / 1000 * window_controls.d
        if window_controls.global_t >= 1 or window_controls.global_t <= 0:
            window_controls.d *= -1

    # Draw lerp points
    draw_bools = [level.toggle.get() for level in window_controls.levels]
    for point in lerp_points:
        if draw_bools[point.depth]:
            point.draw(window_controls.global_t)

    # Trace path of final lerp point
    acc_points = 1000
    line_points = []
    for tval in range(acc_points + 1):
        _t = 1 / acc_points * tval
        line_points.append(drawing_point.get_pos_from_t(_t))
    pygame.draw.lines(window, LerpPoint.color_depth_dict[0], False, line_points, 3)

    # Calculate interpolation
    for point in lerp_points:
        point.t = window_controls.global_t

    # Update colors based on control panel
    for key, val in LerpPoint.color_depth_dict.items():
        LerpPoint.color_depth_dict.update({key: window_controls.levels[key].color})

    window_controls.master.update()
    clock.tick(FPS)
    pygame.display.flip()
