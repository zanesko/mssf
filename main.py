'''
project SCIFAIR!
zelda 08/09/24
'''

import random, copy, sys, pygame, io, math, mapdata, heapq
from pygame.locals import *
#global variables
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
NUMPORTS = 0


class Map:
  def __init__(self, pd, row, col, cost=1, parent=None) :
      self.pd = pd
      self.row = row
      self.col = col
      self.is_port = False
      self.state = 0          # 0:none   1:◵   2:◴   3:◷   4:◶   5:|   6:―   7:○   8:□
      self.cost = cost  # g-score (distance from start)
      self.parent = parent
      self.heuristic = 0  # h-score (estimated distance to goal)
      self.total_cost = 0  # f-score (g + h)

  def set_row_col(self, row, col) :
      self.row = row
      self.col = col

  def __lt__(self, other):
        return self.total_cost < other.total_cost

  def __str__(self) :
      return f"Map(pd={self.pd}, row={self.row}, col={self.col})"





'''
INITIALIZATION CODE
'''

#image files below
bg = pygame.image.load("windmap3.png")
turbine = pygame.image.load("windturbineshadow.png")

state_img = []
state_img.append(None)
# state = 0: nothing overlayed
for i in range(1, 9) :
    if i == 7:
        DFLT_IMG_SZ = (20,20)
        img7 = pygame.image.load("windmill.png")
        img7 = pygame.transform.scale(img7, DFLT_IMG_SZ)
        state_img.append(img7)
    else:
        state_img.append(pygame.image.load("state" + str(i) + ".png"))


# create a local 2D list, L, that is a 2D list of class objects
L = copy.deepcopy(mapdata.L)
for i in range(len(L)) :
    for j in range(len(L[i])) :
        # L[i][j] is the element
        L[i][j] = Map(L[i][j], i, j, 1, None)
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
L[41][19].is_port = True         # Philly



'''
ASTAR FUNCTIONS
'''
#distance formula - heuristic = hacky
def heuristic(a, b):
    """Manhattan distance heuristic for grid traversal."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(L, start_row, start_col, goal):
    """Finds the shortest path in a grid using A* algorithm."""
    rows, cols = len(L), len(L[0])
    open_set = []
    heapq.heappush(open_set, Map(-2, start_row, start_col, 0, None))
    closed_set = set()

    while open_set:
        current = heapq.heappop(open_set)

        if (current.row, current.col) in closed_set:
            continue
        closed_set.add((current.row, current.col))

        if (current.row, current.col) == goal:
            path = []
            while current:
                path.append((current.row, current.col))
                current = current.parent
            return path[::-1]  # Reverse the path

        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
            nrow, ncol = current.row + drow, current.col + dcol

            if 0 <= nrow < rows and 0 <= ncol < cols and L[nrow][ncol] != 0:  # Ensure within bounds & not an obstacle
                move_cost = 1
                neighbor = Map(nrow, ncol, current.cost + move_cost, current)
                neighbor.heuristic = heuristic((nrow, ncol), goal)
                neighbor.total_cost = neighbor.cost + neighbor.heuristic
                heapq.heappush(open_set, neighbor)

    return None  # No path found


def find_nearest_goal(L, start_row, start_col):
    """Finds the nearest goal using A* distance."""
    goals = []
    if L[12][0].state == 8: goals.append((12,0))
    if L[26][28].state == 8: goals.append((26,28))
    if L[30][43].state == 8: goals.append((30,43))
    if L[33][35].state == 8: goals.append((33,35))
    if L[35][31].state == 8: goals.append((35,31))
    if L[31][23].state == 8: goals.append((31,23))
    if L[34][20].state == 8: goals.append((34,20))
    if L[36][24].state == 8: goals.append((36,24))
    if L[38][23].state == 8: goals.append((38,23))
    if L[40][20].state == 8: goals.append((40,20))
    if L[41][19].state == 8: goals.append((41,19))


    best_path = None
    best_goal = None
    best_cost = float('inf')

    for goal in goals:
        path = a_star(L, start_row, start_col, goal)
        if path and len(path) < best_cost:
            best_cost = len(path)
            best_goal = goal
            best_path = path

    return best_goal, best_path

#pygame functions
def draw_text(text, font, text_COL, row, col):
    img = font.render(text, True, text_COL)
    DISPLAYSURF.blit(img, (row, col))


def draw_canvas():
    global L, ROW, COL, NUMPORTS
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(bg, (0,0))
    # draw key rectangle (light blue)
    pygame.draw.rect(DISPLAYSURF, (174, 231, 245), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN :
            xpos = event.pos[0]
            COL = xpos // 20
            ypos = event.pos[1]
            ROW = ypos // 20
            # overlay image at ROW, COL
            print("mousedown: ", ROW,COL)
            if L[ROW][COL].is_port:
                if L[ROW][COL].state == 8 and NUMPORTS > 1:
                    L[ROW][COL].state = 0
                    NUMPORTS -= 1
                elif L[ROW][COL].state == 0:
                    NUMPORTS += 1
                    L[ROW][COL].state = 8
            elif L[ROW][COL].pd > 0 :
                if L[ROW][COL].state == 7 :
                    L[ROW][COL].state = 0
                elif NUMPORTS > 0:
                    L[ROW][COL].state = 7
                    find_nearest_goal(L, L[ROW][COL])
                    #run astar algorithm
        elif event.type == MOUSEMOTION :
            xpos = event.pos[0]
            COL = xpos // 20
            ypos = event.pos[1]
            ROW = ypos // 20
            print("mousemotion: ", ROW,COL)


    #draw text in key
    if L[ROW][COL].pd > 0:
        draw_text(str(L[ROW][COL].pd) + ", " + str(ROW) + "," + str(COL), TEXTFONT, (0, 0, 0), 1010, 475)
    elif L[ROW][COL].pd < 0:
        draw_text(str(ROW) + "," + str(COL), TEXTFONT, (0, 0, 0), 1010, 475)


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







