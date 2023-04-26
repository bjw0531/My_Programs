import pygame
pygame.font.init()

FPS = 160
BX, BY = 640, 360
DISTANCE = 80
RADIUS = 20
WIDTH = 100
OFFSET = -80
PATHW = 30 * 2 + 20
PATHH = 30 * 2 + 20
SUBPATHW = 60
SUBPATHH = 60
BGX = 1280
BGY = 720
SURFACEX = 22360
SURFACEY = 22360
BMIDX = int(BGX / 2)
BMIDY = int(BGY / 2)
SURFACEMIDX = int(SURFACEX / 2)
SURFACEMIDY = int(SURFACEY / 2)
SURFACEINITX = -SURFACEX + BGX
SURFACEINITY = -SURFACEY + BGY
MULTIPLIER = 1

FONT60 = pygame.font.SysFont("HY견고딕", 60, True, True)
FONT30 = pygame.font.SysFont("HY견고딕", 30, True, True)
FONT25 = pygame.font.SysFont("HY견고딕", 25, False, True)
FONT20 = pygame.font.SysFont("HY견고딕", 20, False, True)
FONT15 = pygame.font.SysFont("HY견고딕", 15, False, True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (134, 142, 150)
YELLOW = (255, 255, 0)
SKYBLUE = (0, 128, 255)
ORANGE = (240, 90, 0)
