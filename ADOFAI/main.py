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
degree = 0
pygame.init()

run = True
userinput = [pygame.K_DOWN, pygame.K_UP]
mode = 0
x = 0
bx, by = var.BX, var.BY
key = ''
pathlist = []
standard = []
col1 = var.RED
col2 = var.BLUE
nextpath = 1
xoffset = 0
yoffset = 0
spinrect = Rect(0, 0, 0, 0)
pathpos = Rect(0, 0, 0, 0)
combo = 0
degreecheck = 0

gameovertxt = var.FONT60.render("Game Over", True, var.RED)
gamecleartxt = var.FONT60.render("Game Clear", True, var.GREEN)

soundtrack = maps.btvirus()
pygame.mixer.init(48000, -16, 1, 1024)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.load(soundtrack)
pygame.mixer.music.play()

pathidxscreen = maps.makeidx()
pathscreen, endpathidx = maps.make()

def getxy(degree, mode):
    if mode == 0:
        x = -math.cos(math.radians(degree) * var.MULTIPLIER) * var.DISTANCE
        y = -math.sin(math.radians(degree) * var.MULTIPLIER) * var.DISTANCE
    elif mode == 1:
        x = -math.cos(math.radians(degree) * var.MULTIPLIER) * var.DISTANCE
        y = math.sin(math.radians(degree) * var.MULTIPLIER) * var.DISTANCE
    return [x, y]


def colorchanger(col):
    if col == var.RED:
        return var.BLUE
    else:
        return var.RED


def gameover(mode):
    replay = 0
    if mode == 0:
        pygame.mixer.music.pause()
        screen.blit(
                gameovertxt, [var.BMIDX - gameovertxt.get_rect().centerx, var.BMIDY-200])
        
    if mode == 1:   # game clear
        screen.blit(
            gamecleartxt, [var.BMIDX - gamecleartxt.get_rect().centerx, var.BMIDY-200])

    while not replay:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global run
                run = False
                replay = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    global nextpath, xoffset, yoffset, degree, pathidxscreen,pathscreen, endpathidx, combo, degreecheck
                    replay = False
                    nextpath = 1
                    xoffset = 0
                    yoffset = 0
                    degree = 0
                    degreecheck = 0
                    combo = 0
                    if (pygame.mixer.music.get_busy == False):
                        pygame.mixer.music.pause()
                    pygame.mixer.music.play()
                    if (maps.get_path(0).fpsset):
                        var.MULTIPLIER = maps.get_path(0).fpsset
                    screen.fill(var.BLACK)
                    pathidxscreen = maps.makeidx()
                    pathscreen, endpathidx = maps.make()

                    return

        pygame.display.flip()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            key = event.key

    # hit keyboard
    if key == userinput[0] or key == userinput[1]:
        direction = maps.get_path(nextpath).direction
        intrsctrect = spinrect.colliderect(maps.midpoint(var.BMIDX, var.BMIDY, direction))
        intrsctrect = spinrect.clip(maps.midpoint(var.BMIDX, var.BMIDY, direction))
        intrsctrect: pygame.Rect
        circlesize = var.RADIUS * var.RADIUS * math.pi
        tmppath = maps.get_path(nextpath)
        flag = False

        if direction > 0:
            pygame.draw.rect(screen, var.RED, maps.midpoint(
                var.BMIDX, var.BMIDY, direction))
            if not intrsctrect:
                gameover(0)
                flag = True
            else:
                intrsctrect_size = intrsctrect.width * intrsctrect.height
                if intrsctrect_size >= circlesize:
                    tmppath.accuracyshow(1)
                    combo += 1
                elif intrsctrect_size >= circlesize / 1.5:
                    tmppath.accuracyshow(2)
                    combo = 0
                else:
                    tmppath.accuracyshow(3)
                    combo = 0

        # hit block
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
            xoffset += tmppath.xoffset
            yoffset += tmppath.yoffset
            if tmppath.fpsset:
                var.MULTIPLIER = tmppath.fpsset
            if tmppath.direction == 1:
                degree = 0
            elif tmppath.direction == 2:
                degree = 90
            elif tmppath.direction == 3:
                degree = 180
            elif tmppath.direction == 4:
                degree = 270
            nextpath += 1
            degreecheck = 0
            combo_random = (random.randint(-10,10), random.randint(-10,10))
        else:
            flag = False

    # draw screen
    x, y = getxy(degree, mode)
    pathrect = maps.pathrect(nextpath)

    screen.blit(pathscreen, (-((var.SURFACEX-var.BGX) / 2) +
                xoffset, -((var.SURFACEY-var.BGY) / 2)+yoffset))
    
    screen.blit(pathidxscreen, (-((var.SURFACEX-var.BGX) / 2) +
                                xoffset, -((var.SURFACEY-var.BGY) / 2)+yoffset))

    # 콤보 텍스트
    if combo:
        combocolor = list(var.YELLOW)
        combocolor[1] -= combo * 3.5

        combotxtboxcolor = list(var.SKYBLUE)
        combotxtboxcolor[0] += combo * 3.5
        combotxtboxcolor[2] -= combo * 3.5
        
        for i in range(0,3):
            if(combocolor[i] < 0):
                combocolor[i] = 0
            if(combocolor[i] > 255):
                combocolor[i] = 255
            if(combotxtboxcolor[i] < 0):
                combotxtboxcolor[i] = 0
            if(combotxtboxcolor[i] > 255):
                combotxtboxcolor[i] = 255

        combotxt = var.FONT25.render(f"{combo} COMBO", True, tuple(combocolor))
        combotxtbox = pygame.Rect(0,0, combotxt.get_rect().right, combotxt.get_rect().bottom)
        combotxtbox.center = (var.BMIDX + combo_random[0], var.BMIDY + var.BMIDY * 2 / 3 + combo_random[1])
        pygame.draw.rect(screen, combotxtboxcolor, combotxtbox)
        screen.blit(combotxt, combotxtbox.topleft)

    spinrect = pygame.draw.circle(
        screen, col1, [var.BMIDX + x, var.BMIDY + y], var.RADIUS)
    
    
    # 공 그리기
    pygame.gfxdraw.aacircle(screen, var.BMIDX,
                            var.BMIDY, var.RADIUS, col2)
    pygame.gfxdraw.filled_circle(
        screen, var.BMIDX, var.BMIDY, var.RADIUS, col2)
    coord = var.FONT60.render(
        f"{var.BX-xoffset}, {var.BY-yoffset}", True, var.RED)
    
    pygame.draw.rect(screen, var.RED, maps.midpoint(
                var.BMIDX, var.BMIDY, 4))
    pygame.draw.rect(screen, var.RED, maps.midpoint(
                var.BMIDX, var.BMIDY, 1))
    pygame.draw.rect(screen, var.RED, maps.midpoint(
                var.BMIDX, var.BMIDY, 2))
    pygame.draw.rect(screen, var.RED, maps.midpoint(
                var.BMIDX, var.BMIDY, 3))

    # rotation
    degree += 3
    degreecheck += 3
    if degree * var.MULTIPLIER >= 360:
        degree = 0
    if degreecheck * var.MULTIPLIER >= 360:
        gameover(0)

    pygame.display.flip()
    clock.tick(var.FPS)

pygame.quit()
