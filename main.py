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
      self.is_port = False
      self.state = 0          # 0:none   1:◵   2:◴   3:◷   4:◶   5:|   6:―   7:○   8:□

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


BGCOLOR = (84, 130, 156)
BGCOLOR = (84, 130, 156)

#image files below
bg = pygame.image.load("windmap3.png")
turbine = pygame.image.load("windturbineshadow.png")

state_img = []
state_img.append(None)                                # state = 0: nothing overlayed
for i in range(1, 9) :
    state_img.append(pygame.image.load("state" + str(i) + ".png"))

# create a local 2D list, L, that is a 2D list of class objects
L = copy.deepcopy(mapdata.L)
for i in range(len(L)) :
    for j in range(len(L[i])) :
        # L[i][j] is the element
        L[i][j] = Map(L[i][j])
L[12][0].is_port = True          # Churchill
L[26][28].is_port = True         # Sept-Iles
L[30][43].is_port = True         # St John
L[33][35].is_port = True         # Sydney
L[35][31].is_port = True         # Halifax
L[31][23].is_port = True         # Quebec
L[34][20].is_port = True         # Montreal
L[36][24].is_port = True         # Portland
L[38][23].is_port = True         # Boston
L[40][20].is_port = True         # NY
L[41][19].is_port = True         # Phila

def draw_text(text, font, text_COL, x, y):
    img = font.render(text, True, text_COL)
    DISPLAYSURF.blit(img, (x,y))


def draw_canvas():
    global L, ROW, COL
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(bg, (0,0))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN :
            xpos = event.pos[0]
            COL = xpos // 20
            ypos = event.pos[1]
            ROW = ypos // 20
            # overlay image at ROW, COL
            print("mousedown: ", ROW,COL)
            if L[ROW][COL].is_port:
                L[ROW][COL].state = 8 - L[ROW][COL].state
            elif L[ROW][COL].pd != 0.0:
                L[ROW][COL].state = 7 - L[ROW][COL].state
        elif event.type == MOUSEMOTION :
            xpos = event.pos[0]
            COL = xpos // 20
            ypos = event.pos[1]
            ROW = ypos // 20
            print("mousemotion: ", ROW,COL)
    #draw key rectangle (light blue)
    pygame.draw.rect(DISPLAYSURF, (174, 231, 245), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))

    #draw text in key
    draw_text(str(L[ROW][COL].pd) + ", " + str(ROW) + "," + str(COL), TEXTFONT, (0, 0, 0), 1010, 475)

    spaceRect = pygame.Rect(0, 0, 20, 20)

    # draw board
    # for x in range(NUM_CHIPS):
    for i in range(len(L)) :
        for j in range(len(L[i])) :
            spaceRect.topleft = ((j * 20), (i * 20))
            if L[i][j].state == 8 :
                DISPLAYSURF.blit(state_img[8], spaceRect)
            elif L[i][j].state == 7 :
                DISPLAYSURF.blit(state_img[7], spaceRect)
            #elif (i+j*69931+10) % 17 == 0 :
            #    idx = (i+13*j) % 7 + 1
            #    DISPLAYSURF.blit(state_img[idx], spaceRect)

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







