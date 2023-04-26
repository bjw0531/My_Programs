import random
import librosa
import pygame
from pygame import camera
from pygame.color import Color
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.surface import Surface

import variables as var
import copy

pygame.init()
bg = pygame.image.load('./bg2.jpg')
bg = pygame.transform.scale(bg, (var.BGX, var.BGY))
screen = pygame.Surface((var.SURFACEX, var.SURFACEY))
screen2 = pygame.Surface((var.SURFACEX, var.SURFACEY), pygame.SRCALPHA)
pathlist = []
pathnum = 0


def resetscreen():
    screen.fill(var.BLACK)
    screen2.fill(var.BLACK)


class path:
    def __init__(self, start, offset, col1, col2, direction, fpsset=0):
        # ─ │ ┌ ┐ └ ┘
        # 1 2 3 4 5 6
        xoffsets = [0, offset, 0, -offset, 0]
        yoffsets = [0, 0, offset, 0, -offset]
        self.fpsset = fpsset

        global pathnum
        self.idx = pathnum
        pathnum += 1

        self.rect = pygame.Rect(0, 0, var.PATHW, var.PATHH)
        self.rect.center = start

        self.bridge1 = pygame.Rect(0,0,var.PATHW - var.MINIRECTW * 2, var.MINIRECTH)
        self.bridge2 = pygame.Rect(0,0,var.PATHW - var.MINIRECTW * 2, var.MINIRECTH)
        self.bridge1.center = start
        self.bridge2.center = start

        self.subrect = pygame.Rect(0, 0, var.SUBPATHW, var.SUBPATHH)
        self.subrect.center = start
        
        mode = 3

        self.direction = direction
        self.xoffset = xoffsets[direction]
        self.yoffset = yoffsets[direction]
        self.color = col1
        self.outline_color = col2



    def draw(self, screen):
        if (self.fpsset != 0):
            pygame.draw.rect(
                screen, var.YELLOW, self.subrect)
        else:
            pygame.draw.rect(
                screen, self.color, self.subrect)

        pygame.draw.rect(screen, var.BLUE, self.bridge1)
        pygame.draw.rect(screen, var.BLUE, self.bridge2)
        # pygame.draw.rect(
        #     screen, self.outline_color, self.subrect, 2)

    def getdirection(self):
        return self.direction

    def drawidx(self, screen):
        self.idxtext = var.FONT30.render(str(self.idx), True, var.GRAY)
        screen.blit(
            self.idxtext, self.rect.topleft)

    def accuracyshow(self, type):   # 1 정확 2 보통 3 나쁨
        if (type == 1):
            text = "Great!"
            color = var.GREEN
        elif (type == 2):
            text = "Good"
            color = var.BLUE
        elif (type == 3):
            text = "Bad"
            color = var.RED
        else:
            text = "?"
            color = var.GRAY

        self.acctext = var.FONT20.render(text, True, color)
        screen.blit(self.acctext, self.rect.topleft)


def pathrect(idx):
    return pathlist[idx].rect


def midpoint(x, y, mode):
    #   4
    # 3 □ 1
    #   2
    rect = pygame.Rect(0, 0, 0, 0)
    rect.width = var.PATHW
    rect.height = var.PATHH
    rect.center = (x, y)

    if mode == 1:
        rect.centerx += var.PATHW
    elif mode == 2:
        rect.centery += var.PATHH
    elif mode == 3:
        rect.centerx -= var.PATHW
    elif mode == 4:
        rect.centery -= var.PATHH

    subrect = copy.deepcopy(rect)
    subrect.size = (var.SUBPATHW, var.SUBPATHH)
    subrect.center = rect.center

    return subrect


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
        i.draw(screen)
    endpathidx = len(pathlist)
    return screen, endpathidx


def makeidx():
    # for i in pathlist:
    #     i.drawidx(screen2)
    return screen2


def get_path(idx):
    return pathlist[idx]


def map2():
    #   4
    # 3 □ 1
    #   2
    screen.fill(var.BLACK)
    pathlist.append(
        path([var.SURFACEX / 2, var.SURFACEY / 2], 80, var.WHITE, var.BLACK, 1))

    pattern1 = [1, 1, 1, 1, 2, 2, 2, 2]
    pattern2 = [4, 4, 4, 4, 4, 4, 4, 4]
    pattern3 = [3, 3, 3, 3, 4, 4, 4, 4]

    automake(pattern1+pattern1+pattern1 + [1, 1, 1, 1, 1] + [4, 4, 4] + pattern1 + pattern1 + pattern1 + [1, 1, 1, 1] + [4, 4, 4, 4] + [
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1] + pattern2 + pattern2 + pattern2 + pattern2 + pattern3 + pattern3 + pattern3 + [3, 3, 3, 3, 3, 2, 2, 2])
    pathlist[0].fpsset = 1
    pathlist[65].fpsset = 1 / 4
    pathlist[69].fpsset = 1 / 2
    pathlist[73].fpsset = 1

    filepath = "soundtracks\stg2.wav"
    return filepath


def btvirus():
    filepath = "./soundtracks/Beethoven_Virus.wav"
    screen.fill(var.BLACK)
    pathlist.append(
        path([var.SURFACEX / 2, var.SURFACEY / 2], 80, var.WHITE, var.BLACK, 1))
    pattern1 = [1, 1, 1, 1, 1, 1]

    patternloop = [[4, 3, 2, 1],
                   [2, 3, 4, 1]]

    automake(pattern1+pattern1+patternloop[random.randint(0, 1)]+pattern1+pattern1+pattern1+patternloop[random.randint(0, 1)]+pattern1+pattern1+patternloop[random.randint(0, 1)]+pattern1+patternloop[random.randint(
        0, 1)]+pattern1+patternloop[random.randint(0, 1)]+pattern1+pattern1+patternloop[random.randint(0, 1)]+pattern1+pattern1+pattern1+pattern1+pattern1+patternloop[random.randint(0, 1)]+pattern1)
    var.FPS = trackbeat(filepath, 100)
    return filepath


def trackbeat(filepath, minimumbpm):
    y, sr = librosa.load(filepath)
    tempo, _ = librosa.beat.beat_track(y=y)
    for i in range(1, 10):
        if int(tempo) * i >= minimumbpm:
            return int(tempo) * i
