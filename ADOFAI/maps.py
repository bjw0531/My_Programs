import math
import os
import random
import sys
import threading
import time

import pygame
from pygame import camera
from pygame.color import Color
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.surface import Surface

import variables as var


bg = pygame.image.load('bg2.jpg')
bg = pygame.transform.scale(bg, (var.BGX, var.BGY))
screen = pygame.Surface((var.SURFACEX, var.SURFACEY))
# screen.set_colorkey(var.BLACK)
screen.blit(bg, (-var.SURFACEINITX + var.BX, -var.SURFACEINITY + var.BY))
pathlist = []


class path:
    def __init__(self, start, offset, col1, col2, direction, fpsset=0):
        xoffsets = [0, offset, 0, -offset, 0]
        yoffsets = [0, 0, offset, 0, -offset]
        self.fpsset = fpsset
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.subrect = pygame.Rect(0, 0, 0, 0)
        self.direction = direction
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.xoffset = xoffsets[direction]
        self.yoffset = yoffsets[direction]
        self.color = col1
        self.outline_color = col2

    def draw(self):
        pygame.draw.rect(
            screen, self.color, self.rect)
        pygame.draw.rect(
            screen, self.outline_color, self.rect, 2)

    def getdirection(self):
        return self.direction


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


def automake(l: list):
    for i in l:
        makepath(var.OFFSET, i, var.WHITE, var.BLACK)


def makepath(offset, direction, col1, col2):

    try:
        lastpath = pathlist[len(pathlist) - 1]
    except:
        raise Exception("No lastpath found")

    directrect = midpoint(lastpath.rect.centerx,
                          lastpath.rect.centery, direction)

    pathlist.append(path(directrect.center, offset, col1, col2, direction))


def make():
    for i in pathlist:
        i.draw()
    endpathidx = len(pathlist)
    return screen, endpathidx


def get_path(idx):
    return pathlist[idx]


def map2():
    #   4
    # 3 □ 1
    #   2
    global pathlist
    pathlist.append(
        path([var.SURFACEX / 2, var.SURFACEY / 2], 80, var.WHITE, var.BLACK, 1))

    pattern1 = [1, 1, 1, 1, 2, 2, 2, 2]

    automake(pattern1+pattern1+pattern1 +
             [1, 1, 1, 1, 1]+[4, 4, 4]+pattern1+pattern1+pattern1+[1, 1, 1, 1]+[4, 4, 4, 4]+[1, 1, 1, 1, 1, 1, 1, 1, 1])
