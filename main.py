import pygame as pg
import random

# window params & init
WIDTH = 940
HEIGHT = 660
RES = WIDTH, HEIGHT
TICK_RATE = 3

pg.init()

# main surface
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()

# board params
colors = {"background": (62, 67, 72),
          "board_bg":   (142, 36, 38),
          "black":      (142, 36, 38),
          "white":      (255, 251, 219),
          "dark_gray":  (40, 40, 40)}

# kill feeds
whites = []
blacks = []

# interface builds from this number, default value is 64
# no auto-resize and auto-center for figures (and window), change this at your own risk
square_size = 64

# borders
s_pos = 20      # distance from top left corner of the window
ib = 3          # inner border
ta = 24         # text area
ob = 5          # outer border
board_size = (square_size * 8)
inner_size = board_size + ib * 2
text_area_size = inner_size + ta * 2
outer_size = text_area_size + ob * 2

# figures "prices"
values = {"king": 9, "queen": 7, "bishop": 2, "knight": 2, "rook": 2, "pawn": 1}


class Figure(object):
    def __init__(self, name, pos, board):
        self.name = name
        self.pos = list(pos)

        # autorun methods
        self.put_on_board(board)

    def put_on_board(self, board):
        x = self.pos[0]
        y = self.pos[1]
        for i in range(len(board)):
            if board[i][0] == x and board[i][1] == y:
                board[i][3] = self.name

    def move(self, board):
        # getting self color, figure type and position
        col = self.name.split("_")[0]
        fig = self.name.split("_")[1]
        ln = len(board)
        current = 0
        for i in range(ln):
            if board[i][3] == self.name:
                current = i

        # pawns move and attack
        if fig == "pawn":
            pawn_move_list = []
            pawn_attack_list = []
            if col == "w":
                p_move = -1
            else:
                p_move = 1

            for j in range(ln):
                if board[j][0] == board[current][0] + p_move:
                    if board[j][1] == board[current][1]:
                        pawn_move_list.append(j)

                    elif board[j][1] - 1 == board[current][1] or board[j][1] + 1 == board[current][1]:
                        pawn_attack_list.append(j)

            # create move and attack list
            for item in pawn_move_list:

                # if all fields are empty
                if board[item][3] == "none":
                    if board[item][1] == board[current][1]:
                        board[current][3] = "none"
                        board[item][3] = self.name

                # if any field has enemy figure
                elif board[item][3] != "none" and board[item][3].split("_")[0] != col:
                    target = self.choose_target(pawn_attack_list, board)
                    board[current][3] = "none"
                    board[target][3] = self.name

        # other figs go here

    def choose_target(self, moves, board):
        threat_list = []
        new_list = []
        highest = 0

        for move in moves:
            name = board[move][3]
            if name != "none":
                fig = name.split("_")[1]
                value = values[fig]
                threat_list.append([move, value])
                if value >= highest:
                    highest = value

        for item in threat_list:
            if item[1] >= highest:
                new_list.append(item[0])

        print(new_list)

        quant = len(threat_list)
        if quant > 1:
            rand = random.randrange(0, quant)
            return new_list[rand]

        else:
            return new_list[0]  # FIX THIS | sometimes the list is empty


def make_board():
    # board struct [y, x, color, figure]
    board = []
    for i in range(0, 8):
        if i % 2 == 0:
            switch = 0
            for j in range(0, 8):
                if switch == 0:
                    board.append([i, j, 0, "none"])
                    switch = 1
                else:
                    board.append([i, j, 1, "none"])
                    switch = 0
        if i % 2 != 0:
            switch = 1
            for j in range(0, 8):
                if switch == 0:
                    board.append([i, j, 0, "none"])
                    switch = 1
                else:
                    board.append([i, j, 1, "none"])
                    switch = 0
    return board


def draw_board(board):
    # surfaces
    outer_surface = pg.Surface((outer_size, outer_size))
    outer_surface.fill(colors["black"])

    text_surface = pg.Surface((text_area_size, text_area_size))
    text_surface.fill(colors["white"])

    inner_surface = pg.Surface((inner_size, inner_size))
    inner_surface.fill(colors["black"])

    board_surface = pg.Surface((board_size, board_size))

    # 8x8 field
    for i in range(len(board)):
        if board[i][2] == 0:
            pg.draw.rect(board_surface, colors["white"],
                         rect=(board[i][0] * square_size, board[i][1] * square_size, square_size, square_size))
        if board[i][2] == 1:
            pg.draw.rect(board_surface, colors["black"],
                         rect=(board[i][0] * square_size, board[i][1] * square_size, square_size, square_size))

    # letters
    font = pg.font.SysFont("Arial-black", int(square_size * 0.4))

    letters = ("A", "B", "C", "D", "E", "F", "G", "H")
    letters_start_x = ob + ta * 1.5 + ib + square_size / 2
    letters_start_up = ob + ta
    letters_start_down = ob + ib * 2 + board_size + ta * 2

    # numbers
    numbers = ("8", "7", "6", "5", "4", "3", "2", "1")
    numbers_start_y = ob + ta * 1.5 + ib + square_size / 2
    numbers_left = ob + ta * 1.2
    numbers_right = ob + ib * 2 + board_size + ta * 2

    # draw section
    # draw all surfaces
    screen.blit(outer_surface, (s_pos, s_pos))
    screen.blit(text_surface, (s_pos + ob, s_pos + ob))
    screen.blit(inner_surface, (s_pos + ob + ta, s_pos + ob + ta))
    screen.blit(board_surface, (s_pos + ob + ta + ib, s_pos + ob + ta + ib))

    # draw letters
    shift = 0
    for letter in letters:
        img = font.render(letter, True, (colors["black"]))
        screen.blit(img, (letters_start_x + shift, letters_start_up))
        screen.blit(img, (letters_start_x + shift, letters_start_down))
        shift += square_size

    # draw numbers
    shift = 0
    for number in numbers:
        img = font.render(number, True, (colors["black"]))
        screen.blit(img, (numbers_left, numbers_start_y + shift))
        screen.blit(img, (numbers_right, numbers_start_y + shift))
        shift += square_size

    # draw figures
    ln = len(board)

    for i in range(ln):
        if board[i][3] == "none":
            continue
        else:
            color = board[i][3].split("_")[0]
            figure = board[i][3].split("_")[1]

        icon = ""
        if color == "w":
            if figure == "pawn":
                icon = "wpawn.png"

            elif figure == "rook":
                icon = "wrook.png"

            elif figure == "knight":
                icon = "wknight.png"

            elif figure == "bishop":
                icon = "wbishop.png"

            elif figure == "queen":
                icon = "wqueen.png"

            elif figure == "king":
                icon = "wking.png"
        else:
            if figure == "pawn":
                icon = "bpawn.png"

            elif figure == "rook":
                icon = "brook.png"

            elif figure == "knight":
                icon = "bknight.png"

            elif figure == "bishop":
                icon = "bbishop.png"

            elif figure == "queen":
                icon = "bqueen.png"

            elif figure == "king":
                icon = "bking.png"

        link = "figures/" + icon
        pos = [board[i][1], board[i][0]]

        for j in range(len(pos)):
            pos[j] = (pos[j] * square_size) + s_pos + ob + ta + ib

        img = pg.image.load(link)
        screen.blit(img, pos)


def draw_kill_feed():
    # grid size of kill feed should have space for 16 figures, basic size is 4x4
    row = square_size * 4
    line = square_size * 4
    font_size = int(square_size * 0.25)

    font = pg.font.SysFont("Arial", font_size)
    whites_taken = "White figures taken:"
    blacks_taken = "Black figures taken:"

    w_text = font.render(whites_taken, True, (colors["white"]))
    b_text = font.render(blacks_taken, True, (colors["white"]))

    # render text
    screen.blit(w_text, (s_pos * 3 + outer_size, s_pos))
    screen.blit(b_text, (s_pos * 3 + outer_size, s_pos * 3 + row))

    # render surfaces
    border = pg.Surface((row + ob * 2, line + ob * 2))
    border.fill(colors["black"])

    inner_field = pg.Surface((row, line))
    inner_field.fill(colors["dark_gray"])

    # kill feed for whites
    border.blit(inner_field, (ob, ob))
    screen.blit(border, (s_pos * 3 + outer_size, s_pos * 2))

    # kill feed for blacks
    border.blit(inner_field, (ob, ob))
    screen.blit(border, (s_pos * 3 + outer_size, s_pos * 3 + font_size * 1.2 + row))


def make_white_figures(board):
    figs = []
    # first row
    w_king = Figure("w_king", [7, 4], board)
    figs.append(w_king)

    w_queen = Figure("w_queen", [7, 3], board)
    figs.append(w_queen)

    w_bishop1 = Figure("w_bishop_1", [7, 2], board)
    figs.append(w_bishop1)

    w_bishop2 = Figure("w_bishop_2", [7, 5], board)
    figs.append(w_bishop2)

    w_knight1 = Figure("w_knight_1", [7, 1], board)
    figs.append(w_knight1)

    w_knight2 = Figure("w_knight_2", [7, 6], board)
    figs.append(w_knight2)

    w_rook1 = Figure("w_rook_1", [7, 0], board)
    figs.append(w_rook1)

    w_rook2 = Figure("w_rook_2", [7, 7], board)
    figs.append(w_rook2)

    # pawns row
    w_pawn1 = Figure("w_pawn_1", [6, 0], board)
    figs.append(w_pawn1)

    w_pawn2 = Figure("w_pawn_2", [6, 1], board)
    figs.append(w_pawn2)

    w_pawn3 = Figure("w_pawn_3", [6, 2], board)
    figs.append(w_pawn3)

    w_pawn4 = Figure("w_pawn_4", [6, 3], board)
    figs.append(w_pawn4)

    w_pawn5 = Figure("w_pawn_5", [6, 4], board)
    figs.append(w_pawn5)

    w_pawn6 = Figure("w_pawn_6", [6, 5], board)
    figs.append(w_pawn6)

    w_pawn7 = Figure("w_pawn_7", [6, 6], board)
    figs.append(w_pawn7)

    w_pawn8 = Figure("w_pawn_8", [6, 7], board)
    figs.append(w_pawn8)

    return figs


def make_black_figures(board):
    figs = []
    # first row
    b_king = Figure("b_king", [0, 4], board)
    figs.append(b_king)

    b_queen = Figure("b_queen", [0, 3], board)
    figs.append(b_queen)

    b_bishop1 = Figure("b_bishop_1", [0, 2], board)
    figs.append(b_bishop1)

    b_bishop2 = Figure("b_bishop_2", [0, 5], board)
    figs.append(b_bishop2)

    b_knight1 = Figure("b_knight_1", [0, 1], board)
    figs.append(b_knight1)

    b_knight2 = Figure("b_knight_2", [0, 6], board)
    figs.append(b_knight2)

    b_rook1 = Figure("b_rook_1", [0, 0], board)
    figs.append(b_rook1)

    b_rook2 = Figure("b_rook_2", [0, 7], board)
    figs.append(b_rook2)

    # pawns row
    b_pawn1 = Figure("b_pawn_1", [1, 0], board)
    figs.append(b_pawn1)

    b_pawn2 = Figure("b_pawn_2", [1, 1], board)
    figs.append(b_pawn2)

    b_pawn3 = Figure("b_pawn_3", [1, 2], board)
    figs.append(b_pawn3)

    b_pawn4 = Figure("b_pawn_4", [1, 3], board)
    figs.append(b_pawn4)

    b_pawn5 = Figure("b_pawn_5", [1, 4], board)
    figs.append(b_pawn5)

    b_pawn6 = Figure("b_pawn_6", [1, 5], board)
    figs.append(b_pawn6)

    b_pawn7 = Figure("b_pawn_7", [1, 6], board)
    figs.append(b_pawn7)

    b_pawn8 = Figure("b_pawn_8", [1, 7], board)
    figs.append(b_pawn8)

    return figs


def main():
    screen.fill(colors["background"])
    board = make_board()

    # create figures
    w_figures = make_white_figures(board)
    b_figures = make_black_figures(board)

    while True:
        [exit() for i in pg.event.get() if i.type == pg.QUIT]

        # draw surfaces every tick
        draw_board(board)
        draw_kill_feed()

        # pawns are 8 - 15
        # w_figures[9].move(board)

        # r_fig = random.randrange(8, 16)
        # w_figures[r_fig].move(board)
        # r_fig = random.randrange(8, 16)
        # b_figures[r_fig].move(board)

        # press space for manual moves
        # override TICK_RATE to 200
        TICK_RATE = 200
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    rand_w = random.randrange(8, 16)
                    rand_b = random.randrange(8, 16)
                    w_figures[rand_w].move(board)
                    b_figures[rand_b].move(board)


        # keep at the end
        pg.display.flip()
        clock.tick(TICK_RATE)



if __name__ == '__main__':
    main()
