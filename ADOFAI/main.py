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
import maps


clock = pygame.time.Clock()
screen = pygame.display.set_mode((var.BGX, var.BGY))
tmpscreen = pygame.Surface((1280, 720))
tmpscreen.fill(var.WHITE)
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
gamecleartxt = font.render("Game Clear", True, var.GREEN)

maps.map2()


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


def gameover(mode):
    replay = 0
    while not replay:
        if mode == 0:   # game over
            screen.blit(
                gameovertxt, [screen.get_rect().centerx - gameovertxt.get_rect().centerx, screen.get_rect().centery-200])
        if mode == 1:   # game clear
            screen.blit(
                gamecleartxt, [screen.get_rect().centerx - gamecleartxt.get_rect().centerx, screen.get_rect().centery-200])

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
spinrect = Rect(0, 0, 0, 0)
pathpos = Rect(0, 0, 0, 0)
pathscreen, endpathidx = maps.make()


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key = event.key

    # hit keyboard
    if key == userinput[0] or key == userinput[1]:

        direction = maps.get_path(nextpath).direction
        flag = False

        if direction > 0:
            pygame.draw.rect(screen, var.RED, maps.midpoint(
                screen.get_rect().centerx, screen.get_rect().centery, direction))
            if not spinrect.colliderect(maps.midpoint(screen.get_rect().centerx, screen.get_rect().centery, direction)):
                gameover(0)
                flag = True

        if nextpath + 1 == endpathidx:
            gameover(1)
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
            xoffset += maps.get_path(nextpath).xoffset
            yoffset += maps.get_path(nextpath).yoffset
            nextpath += 1
        else:
            flag = False

    # draw ball
    x, y = getxy(degree, mode)
    pathrect = maps.pathrect(nextpath)

    screen.blit(pathscreen, (-((var.SURFACEX-var.BGX) / 2) +
                xoffset, -((var.SURFACEY-var.BGY) / 2)+yoffset))

    spinrect = pygame.draw.circle(
        screen, col1, [screen.get_rect().centerx + x, screen.get_rect().centery + y], var.RADIUS)

    # pygame.draw.rect(screen, var.WHITE, spinrect)

    # 공 그리기
    pygame.gfxdraw.aacircle(screen, screen.get_rect().centerx,
                            screen.get_rect().centery, var.RADIUS, col2)
    pygame.gfxdraw.filled_circle(
        screen, screen.get_rect().centerx, screen.get_rect().centery, var.RADIUS, col2)
    coord = font.render(
        f"{640-xoffset}, {360-yoffset}", True, var.RED)
    # screen.blit(coord, [screen.get_rect().centerx, screen.get_rect().centery])

    # rotation
    degree += 3
    if degree >= 360:
        degree = 0

    pygame.display.flip()
    clock.tick(var.FPS)

pygame.quit()
