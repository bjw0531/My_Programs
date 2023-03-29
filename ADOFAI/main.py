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
import pygame.gfxdraw

import variables as var
import map1


clock = pygame.time.Clock()
screen = pygame.display.set_mode((var.BGX, var.BGY))
ballscreen = pygame.Surface((var.SURFACEX, var.SURFACEY))
degree = 0
pygame.init()

run = True
userinput = [pygame.K_DOWN, pygame.K_UP]
mode = 0
x = 0
bx, by = var.BX, var.BY
key = ''
pathlist = []

font = pygame.font.SysFont("dotum", 60, True, True)
font2 = pygame.font.SysFont("dotum", 25, False, True)
gameovertxt = font.render("Game Over", True, var.RED)

map1.make()


def getxy(degree, mode):
    if mode == 0:
        x = -math.cos(math.radians(degree)) * var.DISTANCE
        y = -math.sin(math.radians(degree)) * var.DISTANCE
    elif mode == 1:
        x = -math.cos(math.radians(degree)) * var.DISTANCE
        y = math.sin(math.radians(degree)) * var.DISTANCE
    return [x, y]


def colorchanger(col):
    if col == var.RED:
        return var.BLUE
    else:
        return var.RED


def gameover():
    replay = 0
    while not replay:
        screen.blit(
            gameovertxt, [screen.get_rect().centerx - gameovertxt.get_rect().centerx, screen.get_rect().centery-200])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                replay = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    replay = False
                    global nextpath, xoffset, yoffset
                    nextpath = 1
                    xoffset = 0
                    yoffset = 0

                    return

        pygame.display.flip()


col1 = var.RED
col2 = var.BLUE
nextpath = 1
xoffset = 0
yoffset = 0
# pathlist.append(path([var.BX, var.BY], 1, 1))
pathscreen, endpathidx = map1.map()
spinrect = Rect(0, 0, 0, 0)
pathpos = Rect(0, 0, 0, 0)


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key = event.key

    # hit keyboard
    if key == userinput[0] or key == userinput[1]:

        direction = map1.get_path(nextpath).direction
        flag = False

        if direction > 0:
            pygame.draw.rect(ballscreen, var.RED, map1.midpoint(
                var.BX, var.BY, direction))
            if not spinrect.colliderect(map1.midpoint(var.BX, var.BY, direction)):
                gameover()
                flag = True

        if nextpath + 1 == endpathidx:
            gameover()
            flag = True

        if key == userinput[0]:
            mode = 1

        elif key == userinput[1]:
            mode = 0

        key = ''
        if flag == False:
            col1 = colorchanger(col1)
            col2 = colorchanger(col2)
            degree -= 180
            xoffset += map1.get_path(nextpath).xoffset
            yoffset += map1.get_path(nextpath).yoffset
            nextpath += 1
        else:
            flag = False

    # draw ball
    x, y = getxy(degree, mode)
    pathrect = map1.pathrect(nextpath)

    # pathscreen, endpathidx = map1.map()
    # screen.blit(pathscreen, (-var.SURFACEX + var.BGX +
    #             xoffset, -var.SURFACEY + var.BGY + yoffset))
    pygame.draw.rect(ballscreen, var.RED, (0, 0, 8720+640, 9280+360))
    screen.blit(ballscreen, (-8720, -9280))

    spinrect = pygame.draw.circle(
        ballscreen, col1, [8720+640 + x, 9280+360 + y], var.RADIUS)

    # 공 그리기
    pygame.gfxdraw.aacircle(ballscreen, 8720+640,
                            9280+360, var.RADIUS, col2)
    pygame.gfxdraw.filled_circle(
        ballscreen, 8720+640,  9280+360, var.RADIUS, col2)

    # rotation
    degree += 3
    if degree >= 360:
        degree = 0

    pygame.display.flip()
    clock.tick(var.FPS)

pygame.quit()
