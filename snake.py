import random
import curses
import time

def stdin(inp):  # type: (object) -> str
    return raw_input(inp)

# To run the game on Windows, install windows-curses:
# pip install windows-curses

class Snake():
    def __init__(snek, name):
        snek.name = name
        # Pick food with python before init of _CursesWindow
        snek.foodChoice = snek.pickFood()
        snek.cursesWindow = curses.initscr()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        snek.maxYX = snek.cursesWindow.getmaxyx()
        snek.windowHeight = snek.maxYX[0]
        snek.windowWidth = snek.maxYX[1]
        snek.x = snek.windowWidth / 4
        snek.y = snek.windowHeight / 2
        snek.pos = [
            [snek.y, snek.x],
            [snek.y, snek.x - 1],
            [snek.y, snek.x - 2]
        ]
        snek.highScore = 0
        snek.food = [snek.windowHeight / 2, snek.windowWidth / 2]
        # Supported key presses - other input will be ignored
        snek.supportedKeys = [curses.KEY_RIGHT,
                              curses.KEY_DOWN, curses.KEY_UP, curses.KEY_LEFT, -1]
        # Initial direction of snek
        snek.key = curses.KEY_RIGHT
        snek.bodyType = curses.ACS_BLOCK
        snek.foodTypes = {
            "diamond": curses.ACS_DIAMOND,
            "sterling": curses.ACS_STERLING,
            "lantern": curses.ACS_LANTERN
        }
        snek.foodType = snek.foodTypes.get(
            snek.foodChoice) or snek.foodTypes.get("diamond")
        snek.window = curses.newwin(
            snek.windowHeight-1, snek.windowWidth-1, 0, 0)
        snek.window.keypad(1)
        snek.window.timeout(100)
        snek.addFood()
        snek.alive = True

    def setHighscore(snek, inc=0):  # type: (int) -> None
        snek.highScore += inc
        snek.window.addnstr(0, 0, "{}'s Highscore: {}".format(
            snek.name, str(snek.highScore)), snek.windowWidth)

    def addFood(snek):
        while snek.food is None:
            newFood = [
                random.randint(1, snek.windowHeight-1),
                random.randint(1, snek.windowWidth-1)
            ]
            snek.food = newFood if newFood not in snek.pos else None
        snek.window.addch(int(snek.food[0]), int(snek.food[1]), snek.foodType)

    def pickFood(snek):
        pick = stdin("Pick your snake's poison? (y/n) ").strip()
        if pick == "" or pick == None or pick.startswith("n"):
            return

        if not pick.startswith("y"):
            return
    
        avFood = {1: "diamond", 2: "lantern", 3: "sterling"}
        print("Available poison: {}".format(avFood))
        pref = stdin("Your poison preference (pick number) ").strip()

        try:
            foodPref = int(pref)
            if foodPref in avFood:
                return avFood.get(foodPref)

            print("No such poison.", foodPref)
        except:
            print("No such poison.", pref)

        time.sleep(1)
        return avFood.get(1)

    def move(snek):
        newPos = [snek.pos[0][0], snek.pos[0][1]]

        if snek.key == curses.KEY_DOWN:
            newPos[0] += 1
        if snek.key == curses.KEY_UP:
            newPos[0] -= 1
        if snek.key == curses.KEY_LEFT:
            newPos[1] -= 1
        if snek.key == curses.KEY_RIGHT:
            newPos[1] += 1

        snek.pos.insert(0, newPos)

    def start(snek):
        # Set initial highscore
        snek.setHighscore()
        while snek.alive:
            snek.nextKey = snek.window.getch()
            if snek.nextKey in snek.supportedKeys:
                snek.key = snek.key if snek.nextKey == -1 else snek.nextKey

            if snek.pos[0][0] in [0, snek.windowHeight] or snek.pos[0][1] in [0, snek.windowWidth] or snek.pos[0] in snek.pos[1:]:
                snek.endGame()

            snek.move()

            if snek.pos[0] == snek.food:
                snek.food = None
                snek.setHighscore(1)
                snek.addFood()
            else:
                tail = snek.pos.pop()
                snek.window.addch(int(tail[0]), int(tail[1]), ' ')

            try:
                snek.window.addch(int(snek.pos[0][0]), int(
                    snek.pos[0][1]), snek.bodyType)
            except:
                continue

    def endGame(snek):
        snek.window.clear()
        snek.window.addnstr(snek.y, (snek.windowWidth * 45) / 100,
                            "Game over, food eaten: {}".format(str(snek.highScore)), snek.windowWidth)
        snek.window.refresh()
        time.sleep(3)
        snek.alive = False
        curses.nocbreak()
        snek.window.keypad(0)
        curses.echo()
        curses.endwin()
        quit()


newSnake = Snake(stdin("Your snake's name: "))
newSnake.start()
