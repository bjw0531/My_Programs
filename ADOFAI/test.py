import math
import os
import random
import sys
import threading
import time

import pygame
import pygame.gfxdraw
from pygame import camera
from pygame.color import Color
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.surface import Surface

import map1
import variables as var


class path:
    def __init__(self, start, direction, pathtype, offset, col1, col2):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 1
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.width = 100
        self.camera_offset = offset
        self.color = col1
        self.outline_color = col2

    def draw(self):
        pygame.draw.rect(
            screen, self.color, self.rect)
        pygame.draw.rect(
            screen, self.outline_color, self.rect, 2)

    def getdirection(self):
        return self.direction


def makepath(offset, direction, col1, col2):

    try:
        lastpath = pathlist[len(pathlist) - 1]
    except:
        raise Exception("No lastpath found")

    directrect = midpoint(lastpath.rect.centerx,
                          lastpath.rect.centery, direction)

    pathlist.append(
        path(directrect.center, 1, 1, offset, col1, col2))


def pathrect(idx):
    return pathlist[idx].rect


def midpoint(x, y, mode):
    #   4
    # 3 □ 1
    #   2
    rect = pygame.Rect(0, 0, 0, 0)
    rect.width = var.PATHW
    rect.height = var.PATHH
    rect.centerx = x
    rect.centery = y

    if mode == 1:
        rect.centerx += var.PATHW
        return rect
    elif mode == 2:
        rect.centery += var.PATHH
        return rect
    elif mode == 3:
        rect.centerx -= var.PATHW
        return rect
    elif mode == 4:
        rect.centery -= var.PATHH
        return rect


def make():
    global pathlist

    for i in range(11):
        if i != 9:
            makepath(var.OFFSET, 1, var.WHITE, var.BLACK)
        else:
            makepath(var.OFFSET, 1, var.RED, var.WHITE)


def map():
    for i in range(11):
        pathlist[i].draw()
    endpathidx = len(pathlist)
    return screen, endpathidx


def get_path(idx):
    return pathlist[idx]


clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))
pygame.init()
pathlist = []
pathlist.append(path([var.BX, var.BY], 1, 1, -80, var.WHITE, var.BLACK))
make()

while True:
    screen.blit(map()[0], [0, 0])
    pygame.display.flip()
    clock.tick(60)
