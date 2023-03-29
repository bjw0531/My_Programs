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
import map1


bg = pygame.image.load('bg2.jpg')
bg = pygame.transform.scale(bg, (var.BGX, var.BGY))
screen = pygame.Surface((var.SURFACEX, var.SURFACEY))
screen.blit(bg, (var.SURFACEMIDX - var.BGX / 2, var.SURFACEMIDY - var.BGY / 2))
pathlist = []


class path1:
    def __init__(self, start, pathtype, offset, col1, col2):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 1
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.xoffset = offset
        self.yoffset = 0
        self.color = col1
        self.outline_color = col2

    def draw(self):
        pygame.draw.rect(
            screen, self.color, self.rect)
        pygame.draw.rect(
            screen, self.outline_color, self.rect, 2)

    def getdirection(self):
        return self.direction


class path2:
    def __init__(self, start, pathtype, offset, col1, col2):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 2
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.xoffset = 0
        self.yoffset = offset
        self.color = col1
        self.outline_color = col2

    def draw(self):
        pygame.draw.rect(
            screen, self.color, self.rect)
        pygame.draw.rect(
            screen, self.outline_color, self.rect, 2)

    def getdirection(self):
        return self.direction


class path3:
    def __init__(self, start, pathtype, offset, col1, col2):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 3
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.xoffset = -offset
        self.yoffset = 0
        self.color = col1
        self.outline_color = col2

    def draw(self):
        pygame.draw.rect(
            screen, self.color, self.rect)
        pygame.draw.rect(
            screen, self.outline_color, self.rect, 2)

    def getdirection(self):
        return self.direction


class path4:
    def __init__(self, start, pathtype, offset, col1, col2):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.direction = 4
        self.rect.width = var.PATHW
        self.rect.height = var.PATHH
        self.rect.centerx = start[0]
        self.rect.centery = start[1]
        self.xoffset = 0
        self.yoffset = -offset
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


def make():
    global pathlist
    pathlist.append(
        path1([var.SURFACEMIDX, var.SURFACEMIDY], 1, 80, var.WHITE, var.BLACK))

    for i in range(11):

        makepath(var.OFFSET, 2, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 2, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 2, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 2, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 3, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 3, var.WHITE, var.BLACK)
        makepath(var.OFFSET, 3, var.WHITE, var.BLACK)


def makepath(offset, direction, col1, col2):

    try:
        lastpath = pathlist[len(pathlist) - 1]
    except:
        raise Exception("No lastpath found")

    directrect = midpoint(lastpath.rect.centerx,
                          lastpath.rect.centery, direction)
    if direction == 1:
        pathlist.append(
            path1(directrect.center, 1, offset, col1, col2))
    if direction == 2:
        pathlist.append(
            path2(directrect.center, 1, offset, col1, col2))
    if direction == 3:
        pathlist.append(
            path3(directrect.center, 1, offset, col1, col2))
    if direction == 4:
        pathlist.append(
            path4(directrect.center, 1, offset, col1, col2))


def map():
    for i in pathlist:
        i.draw()
    endpathidx = len(pathlist)
    return screen, endpathidx


def get_path(idx):
    return pathlist[idx]
