from blessed import Terminal
from math import floor
from random import randint
from sys import exit
import sacred

t = Terminal()
scene = sacred.Scene()
moves = []  # like jagger
claims = []
full = []
lastmove = (0, 0)
map = {
    1: [floor(t.width / 2) - 12,
        floor(t.height / 2) + 2],
    2: [floor(t.width / 2) - 5, floor(t.height / 2) + 2],
    3: [floor(t.width / 2) + 3, floor(t.height / 2) + 2],
    4: [floor(t.width / 2) - 12,
        floor(t.height / 2) - 5],
    5: [floor(t.width / 2) - 5, floor(t.height / 2) - 5],
    6: [floor(t.width / 2) + 3, floor(t.height / 2) - 5],
    7: [floor(t.width / 2) - 12,
        floor(t.height / 2) - 12],
    8: [floor(t.width / 2) - 5,
        floor(t.height / 2) - 12],
    9: [floor(t.width / 2) + 3,
        floor(t.height / 2) - 12],
}


def notzero(n):
    if n >= 1:
        return 1
    else:
        return 0


def clearbrd():
    global board
    global claims
    board = []
    claims = []
    for _ in range(9):
        board.append([0 for i in range(9)])
        claims.append(0)


def keyinput(prompt, x, y, i=True):
    with t.cbreak():
        scene.txt(prompt, x, y)
        scene.render()
        with t.location(1, 1):
            if i:
                try:
                    return int(t.inkey())

                except ValueError:
                    print("Please select a", t.bold("NUMBER"))
                    enter()
            else:
                return t.inkey()


def enter():
    input(t.bold_red_on_bright_yellow("[Press Enter]"))


def chkboard(sub):  #fills board with the correct symbol.
    p = 9
    for i in reversed(board[sub - 1]):
        if i != 0:
            scene.obj("objs/{}.json".format(i), map[p][0], map[p][1])
        p -= 1


def add_move(sub, move, player):
    board[sub - 1][int(move) - 1] = player
    global lastmove
    global moves
    lastmove = (sub, int(move))
    moves.append((sub, int(move)))
    scene.reset()


def summary():
    a = [t.black_on_blue(" "), t.black_on_green("X"), t.black_on_yellow("O")]
    ptrn = [0, 3, 6]
    s = 0
    for i in ptrn:
        scene.txt(
            "{}{}{}{} {}{}{}{} {}{}{}{}".format(
                i + 1, a[board[0 + i][0]], a[board[0 + i][1]],
                a[board[0 + i][2]], i + 2, a[board[1 + i][0]],
                a[board[1 + i][1]], a[board[1 + i][2]], i + 3,
                a[board[2 + i][0]], a[board[2 + i][1]], a[board[2 + i][2]]),
            t.width - 16, 12 - i - s)
        scene.txt(
            " {}{}{}  {}{}{}  {}{}{}".format(
                a[board[0 + i][3]], a[board[0 + i][4]], a[board[0 + i][5]],
                a[board[1 + i][3]], a[board[1 + i][4]], a[board[1 + i][5]],
                a[board[2 + i][3]], a[board[2 + i][4]], a[board[2 + i][5]]),
            t.width - 16, 11 - i - s)
        scene.txt(
            " {}{}{}  {}{}{}  {}{}{}".format(
                a[board[0 + i][6]], a[board[0 + i][7]], a[board[0 + i][8]],
                a[board[1 + i][6]], a[board[1 + i][7]], a[board[1 + i][8]],
                a[board[2 + i][6]], a[board[2 + i][7]], a[board[2 + i][8]]),
            t.width - 16, 10 - i - s)
        s += 1


def check(sub, move, player, comp=False):
    try:
        if int(move) == 0:
            if not comp:
                print("Choice not valid")
                enter()
            return False
        elif board[sub - 1][int(move) - 1] != 0:
            if not comp:
                print("Already played")
                enter()
            return False
        elif board[int(move) - 1].count(0) > 1:
            add_move(sub, int(move), player)
            return True
        elif board[int(move) - 1].count(0) == 1:
            if board[int(move) - 1].index(0) == int(move) - 1:
                if not comp:
                    print("Choice not valid (FreezeGame)")
                    enter()
                return False
            else:
                add_move(sub, int(move), player)
                return True
        elif int(move) - 1 in full:
            if board[sub - 1].count(0) == 1:
                if board[sub - 1].index(0) == (sub - 1):
                    print(t.bold("TIE GAME"))
                    clearbrd()
                    enter()
                    return "TIE"
                if board[sub - 1].index(0) in full:
                    print(t.bold("TIE GAME"))
                    clearbrd()
                    enter()
                    return "TIE"
            else:
                if not comp:
                    print("SUB BOARD FULL")
                    enter()
                return False
        else:
            add_move(sub, int(move), player)
            return True
    except ValueError:
        if not comp:
            print("Choice not valid")
            enter()
        return False


def grid(sub, player, num=0):
    id = ["X", "O"]
    while True:
        scene.reset()
        scene.box()
        scene.obj("objs/subgrid.json",
                  floor(t.width / 2) - 12,
                  floor(t.height / 2) - 12)
        chkboard(sub)
        summary()
        scene.txt(
            t.black_on_bright_yellow("{}: Make your move".format(
                id[player - 1])), 4, 6)
        scene.txt("Press 'q' to exit", 4, 7)
        scene.txt("Sub board: {}".format(t.bold(str(lastmove[1]))), 4, 8)
        scene.txt("Press 'd' to export debug info", t.width - 31, t.height - 2)
        scene.render()

        move = keyinput("", 0, 0, i=False)
        if move.lower() == "q":
            scene.reset()
            clearbrd()
            return "QUIT"
        if move.lower() == "d":
            with open("debug.txt", "w+") as f:
                f.write(str(moves))
                f.write(str(board))
                continue
        c = check(sub, move, player)
        if c == False:
            continue
        if c == "TIE":
            return "QUIT"
        else:
            return


def start():
    scene.reset()
    scene.box()
    scene.obj("objs/gridguide.json",
              floor(t.width / 2) - 12,
              floor(t.height / 2) - 11)
    global start
    global full
    full = []
    while True:
        sub = keyinput("Select sub-board (1-9)", 4, 6)
        if sub == 0:
            print("Choices are 1-9")
            enter()
            continue
        else:
            global lastmove
            lastmove = (0, int(sub))
            break

    sacred.clear()
    q = grid(sub, 1)
    if q == "QUIT":
        return "QUIT"


def runlocal():
    q = start()
    if q == "QUIT":
        return
    grid(lastmove[1], 2)
    while True:
        for i in range(1, 3):
            winchk = win()
            if winchk == 1:
                print(t.bold("WINNER IS X"))
                clearbrd()
                enter()
                return
            if winchk == 2:
                print(t.bold("WINNER IS O"))
                clearbrd()
                enter()
                return
            if len(full) == 8:
                print(t.bold("TIE GAME"))
                clearbrd()
                enter()
                return
            else:
                q = grid(lastmove[1], i)
                if q == "QUIT":
                    return


def runsingle():
    q = start()
    if q == "QUIT":
        return
    check(lastmove[1], randint(1, 9), 2, comp=True)
    while True:
        winchk = win()
        if winchk == 1:
            print(t.bold("WINNER IS X"))
            clearbrd()
            enter()
            return
        if winchk == 2:
            print(t.bold("WINNER IS THE COMPUTER!"))
            clearbrd()
            enter()
            return
        if len(full) == 8:
            print(t.bold("TIE GAME"))
            clearbrd()
            enter()
            return
        else:
            q = grid(lastmove[1], 1)
            if q == "QUIT":
                return
            c = 0
            while True:
                mv = check(lastmove[1], randint(1, 9), 2, comp=True)
                if not mv:
                    c += 1
                    if c == 32:
                        print(t.bold("TIE GAME"))
                        clearbrd()
                        enter()
                        return
                    continue
                else:
                    break


def win():
    global claims
    chkwin = []
    brdchk = claims
    s = 0
    for i in board:  #chks sub board victory
        try:
            i.index(0)
        except:
            if s not in full:
                full.append(s)
        for n in range(0, 3):
            chkwin.append(i[n] * i[n + 3] * i[n + 6])
            chkwin.append(i[n * 3] * i[n * 3 + 1] * i[n * 3 + 2])
        chkwin.append(i[0] * i[4] * i[8])
        chkwin.append(i[2] * i[4] * i[6])
        for n in chkwin:
            if n == 8:
                if brdchk[s] == 0:
                    brdchk[s] = 2
                    break
            if n == 1:
                if brdchk[s] == 0:
                    brdchk[s] = 1
                    break
        chkwin.clear()
        s += 1

    claims = brdchk
    if brdchk == [0] * 9:
        return False
    else:
        for n in range(0, 3):  #checks main board victory
            chkwin.append(brdchk[n] * brdchk[n + 3] * brdchk[n + 6])
            chkwin.append(brdchk[n * 3] * brdchk[n * 3 + 1] * brdchk[n * 3 + 2])
        chkwin.append(brdchk[0] * brdchk[4] * brdchk[8])
        chkwin.append(brdchk[2] * brdchk[4] * brdchk[6])
        for n in chkwin:
            if n == 8:
                return 2
            if n == 1:
                return 1
        return False


try:
    clearbrd()
    moves = []
    while True:
        scene.reset()
        sacred.clear()

        scene.box()
        scene.obj("objs/grid.json",
                  floor(t.width / 2) - 12,
                  floor(t.height / 2) - 11)
        scene.txt(
            t.green("For best gameplay, use numpad and 80x24 terminal"),
            t.width - 49, t.height - 2)
        scene.txt("1) Single Player", 4, 5)
        scene.txt("2) Local Multiplayer", 4, 6)
        scene.txt("3) Help", 4, 7)
        scene.txt("4) Exit", 4, 8)
        scene.txt(
            t.bright_yellow("Ultimate Tic Tac Toe TERMINAL EDITION"), 0, 0)
        scene.render()

        val = keyinput("", 0, 0)
        if val == 1:
            sacred.clear()
            runsingle()
        elif val == 2:
            scene.reset()
            sacred.clear()
            runlocal()
        elif val == 3:
            scene.txt(
                t.green("Use the numpad with the corresponding position."), 0,
                15)
            scene.txt(
                "See rules here: https://docs.riddles.io/ultimate-tic-tac-toe/rules",
                0, 16)
            scene.render()
            enter()
        elif val == 4:
            exit()
        elif val == None:
            continue
        elif val > 3:
            print("Choice not valid")
            enter()

except KeyboardInterrupt:
    sacred.clear()
    cleared = True
    print("Quitting")

finally:
    cleared = False
    if cleared != True:
        sacred.clear()
