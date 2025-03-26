'''
project SCIFAIR!
zelda 08/09/24
'''

import random, copy, sys, pygame, io, math, mapdata, heapq, pprint
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
TEXTFONT = None #splash screen font and size
TEXTFONT2 = None #key title font and size
TEXTFONT3 = None #wind power (key) font and size
BGCOLOR = (84, 130, 156)
NUMPORTS = 0
NUMFARMS = 0
PORTCOST = 2
FARMCOST = 5
PATHCOST = 0.5
BUDGET = 100
SCORE = 0
MODE = 0  #user instructions splash screen, MODE = 1 is the regular game



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
    elif i == 1:
        DFLT_IMG_SZ = (20, 20)
        img1 = pygame.image.load("state1.png")
        img1 = pygame.transform.scale(img1, DFLT_IMG_SZ)
        state_img.append(img1)
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

        for drow, dcol in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Up, Down, Left, Right
            nrow, ncol = current.row + drow, current.col + dcol

            if 0 <= nrow < rows and 0 <= ncol < cols and (L[nrow][ncol].pd != 0.0 or L[nrow][ncol].is_port):  # Ensure within bounds & not an obstacle
                move_cost = math.sqrt(drow**2 + dcol**2)
                neighbor = Map(-2, nrow, ncol, current.cost + move_cost, current)
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
    print("DEBUG :: " + str(best_goal) + ", " + str(best_path))
    return best_path

#pygame functions
def draw_text(text, font, text_COL, row, col):
    img = font.render(text, True, text_COL)
    DISPLAYSURF.blit(img, (row, col))


def draw_canvas():
    global L, ROW, COL, NUMPORTS, NUMFARMS, MODE, BUDGET, SCORE
    DISPLAYSURF.fill(BGCOLOR)
    DISPLAYSURF.blit(bg, (0,0))
    if MODE == 0:
        KEYXMARGIN = 240
        KEYYMARGIN = 373
        KEYXSIZE = 824
        KEYYSIZE = 104
        pygame.draw.rect(DISPLAYSURF, (232, 255, 240), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #white border
        KEYXMARGIN = 247
        KEYYMARGIN = 380
        KEYXSIZE = 810
        KEYYSIZE = 90
        pygame.draw.rect(DISPLAYSURF, (166, 207, 218), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #blue rectangle
        draw_text("Please select up to 5 ports before placing a wind farm.", TEXTFONT, (0,0,0), 348, 385)
        draw_text("Click anywhere to continue.", TEXTFONT, (0,0,0), 518, 430) #user instructions
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN :
                MODE = 1
    else:
        # draw key rectangle (light blue)
        KEYXMARGIN = 993
        KEYYMARGIN = 423
        KEYXSIZE = 264
        KEYYSIZE = 404
        pygame.draw.rect(DISPLAYSURF, (232, 255, 240), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #white border
        KEYXMARGIN = 1000
        KEYYMARGIN = 430
        KEYXSIZE = 250
        KEYYSIZE = 390
        pygame.draw.rect(DISPLAYSURF, (166, 207, 218), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #blue box
        KEYXMARGIN = 1030
        KEYYMARGIN = 550
        KEYXSIZE = 90
        KEYYSIZE = 270
        pygame.draw.rect(DISPLAYSURF, (118, 151, 93), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #money bar
        KEYXMARGIN = 1130
        KEYYMARGIN = 810
        KEYXSIZE = 90
        KEYYSIZE = 10
        pygame.draw.rect(DISPLAYSURF, (87, 95, 149), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE)) #carbon offset bar
        for event in pygame.event.get():
            if MODE == 1:
                if event.type == MOUSEBUTTONDOWN :
                    xpos = event.pos[0]
                    COL = xpos // 20
                    ypos = event.pos[1]
                    ROW = ypos // 20
                    # overlay image at ROW, COL
                    #print("mousedown: ", ROW,COL)
                    if L[ROW][COL].is_port and NUMFARMS == 0:
                        if L[ROW][COL].state == 8 and NUMPORTS > 1:
                            L[ROW][COL].state = 0
                            NUMPORTS -= 1
                            BUDGET += PORTCOST
                            KEYXMARGIN = 1030
                            KEYYMARGIN = 539 # -2% of 550 - box starts earlier (to increase)
                            KEYXSIZE = 90
                            KEYYSIZE = 281 # +2% of 270 - height increases
                            pygame.draw.rect(DISPLAYSURF, (118, 151, 93), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # money bar
                        elif L[ROW][COL].state == 0 and NUMPORTS < 5:
                            NUMPORTS +=1
                            L[ROW][COL].state = 8
                            BUDGET -= PORTCOST
                            KEYXMARGIN = 103 #1030! change for test run
                            KEYYMARGIN = 561  #+2% of 550 - box starts later (to decrease)
                            KEYXSIZE = 90
                            KEYYSIZE = 259  # -2% of 270 - height decreases
                            pygame.draw.rect(DISPLAYSURF, (118, 151, 93), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # money bar
                    elif L[ROW][COL].pd > 0 and L[ROW][COL].state != 7:
                        if 0 < NUMPORTS <= 5:
                            L[ROW][COL].state = 7
                            NUMFARMS += 1
                            BUDGET -= FARMCOST
                            KEYXMARGIN = 1030
                            KEYYMARGIN = 577.5  # +5 m% of 550 - box starts later (to decrease)
                            KEYXSIZE = 90
                            KEYYSIZE = 256.5  # -5% of 270 - height decreases
                            pygame.draw.rect(DISPLAYSURF, (118, 151, 93), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # money bar
                            SCORE += L[ROW][COL].pd * 10
                            MODE = 1 #test run
                            KEYXMARGIN = 113 #1130! changed for test run
                            KEYYMARGIN = 810 - (L[ROW][COL].pd * 10) # -score change (to increase)
                            KEYXSIZE = 90
                            KEYYSIZE = 10 + (L[ROW][COL].pd * 10) # +score change (gets taller)
                            pygame.draw.rect(DISPLAYSURF, (87, 95, 149), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # carbon offset bar
                            path = find_nearest_goal(L, ROW, COL)
                            for i in range(len(path)):
                                if i != len(path)-1 and i != 0 and L[path[i][0]][path[i][1]].state != 7:
                                    L[path[i][0]][path[i][1]].state = 1
                                    BUDGET -= PATHCOST
                            #run astar algorithm
                elif event.type == MOUSEMOTION :
                    xpos = event.pos[0]
                    COL = xpos // 20
                    ypos = event.pos[1]
                    ROW = ypos // 20
                if BUDGET <= 0:
                    MODE = 2
            else:
                if event.type == MOUSEBUTTONDOWN:
                    MODE = 1
                    # clear state
                    for i in range(len(L)):
                        for j in range(len(L[i])):
                            L[i][j].state = 0
                    NUMPORTS = 0
                    NUMFARMS = 0
                    BUDGET = 100
                    SCORE = 0

        #draw text in key
        if L[ROW][COL].pd > 0:
            draw_text("Wind Power Density", TEXTFONT2, (0, 0, 0), 1010, 438)
            draw_text("Cost vs Generated Power", TEXTFONT2, (0, 0, 0), 1010, 510)
            draw_text(str(L[ROW][COL].pd) + " kW/m²", TEXTFONT3, (0, 0, 0), 1010, 470)


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
                elif L[i][j].state == 1:
                    DISPLAYSURF.blit(state_img[1], spaceRect)
                #elif (i+j*69931+10) % 17 == 0 :
                #    idx = (i+13*j) % 7 + 1
                #    DISPLAYSURF.blit(state_img[idx], spaceRect)


        if MODE == 2:
            KEYXMARGIN = 240
            KEYYMARGIN = 373
            KEYXSIZE = 824
            KEYYSIZE = 104
            pygame.draw.rect(DISPLAYSURF, (232, 255, 240), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # white border
            KEYXMARGIN = 247
            KEYYMARGIN = 380
            KEYXSIZE = 810
            KEYYSIZE = 90
            pygame.draw.rect(DISPLAYSURF, (166, 207, 218), pygame.Rect(KEYXMARGIN, KEYYMARGIN, KEYXSIZE, KEYYSIZE))  # blue rectangle
            draw_text("You've generated" + "(this many MW)" + "! Great job!", TEXTFONT, (0, 0, 0), 348, 385)
            draw_text("Click anywhere to play again.", TEXTFONT, (0, 0, 0), 518, 430)  # user instructions

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    MODE = 1
                    #clear state
                    for i in range(len(L)):
                        for j in range(len(L[i])) :
                            L[i][j].state = 0
                    NUMPORTS = 0
                    NUMFARMS = 0
                    BUDGET = 100
                    SCORE = 0

    pygame.display.update()
    FPSCLOCK.tick()


def run_game():
    while True:
        draw_canvas()


def main():
    global FPSCLOCK, DISPLAYSURF
    global WINDOWWIDTH, WINDOWHEIGHT
    global TEXTFONT, TEXTFONT2, TEXTFONT3

    pygame.init()
    TEXTFONT = pygame.font.SysFont("arialrounded", 25)
    TEXTFONT2 = pygame.font.SysFont("Tahoma", 20)
    TEXTFONT3 = pygame.font.SysFont("futura", 23)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('SCIFAIR')
    pprint.pprint(pygame.font.get_fonts())


    while True:
        run_game()

if __name__ == '__main__':
    main()







