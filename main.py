'''
project SCIFAIR!
zelda 08/09/24
'''

import random, copy, sys, pygame, io, math, mapdata
from pygame.locals import *


class Map:
  def __init__(self, pd) :
      self.pd = pd
      self.row = -1
      self.col = -1

  def set_row_col(self, row, col) :
      self.row = row
      self.col = col

  def __str__(self) :
      return f"Map(pd={self.pd}, row={self.row}, col={self.col})"


ROW = 0
COL = 0
FPS = 15
WINDOWWIDTH = 1280
WINDOWHEIGHT = 840
KEYXMARGIN = 1000
KEYYMARGIN = 450
KEYXSIZE = 250
KEYYSIZE = 370
TEXTFONT = None


BGCOLOR = (84, 130, 156)ß
BGCOLOR = (84, 130, 156)ß

#image files below
bg = pygame.image.load("windmap2.png")
turbine = pygame.image.load("windturbineshadow.png")

def draw_text(text, font, text_COL, x, y):
    img = font.render(text, True, text_COL)
    DISPLAYSURF.blit(img, (x,y))


def draw_canvas():
    global ROW
    global COL
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            xpos = event.pos[0]
            COL = xpos // 20
            ypos = event.pos[1]
            ROW = ypos // 20
            print(ROW,COL)
    #draw key rectangle (light blue)
    pygame.draw.rect(DISPLAYSURF, (174, 231, 245), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))
    #draw text in key
    draw_text(str(mapdata.L[ROW][COL]) + ", " + str(ROW) + "," + str(COL), TEXTFONT, (0, 0, 0), 1010, 475)
    pygame.display.update()
    FPSCLOCK.tick()




def run_game():
    while True:
        draw_canvas()


def main():
    global FPSCLOCK, DISPLAYSURF
    global WINDOWWIDTH, WINDOWHEIGHT
    global TEXTFONT

    pygame.init()
    TEXTFONT = pygame.font.SysFont("Arial", 30)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('SCIFAIR')


    while True:
        run_game()

if __name__ == '__main__':
    main()







