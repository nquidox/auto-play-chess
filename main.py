import pygame as pg


WIDTH = 1280
HEIGHT = 768
RES = WIDTH, HEIGHT

pg.init()
screen = pg.display.set_mode(RES)
main_surface = pg.Surface(RES)
clock = pg.time.Clock()

colors = {"background": (62, 67, 72),
          "board_bg":   (142, 36, 38),
          "black":      (142, 36, 38),
          "white":      (255, 251, 219)}


def make_board():
    board = []
    for i in range(0, 8):
        if i % 2 == 0:
            switch = 0
            for j in range(0, 8):
                if switch == 0:
                    board.append((i, j, 0))
                    switch = 1
                else:
                    board.append((i, j, 1))
                    switch = 0
        if i % 2 != 0:
            switch = 1
            for j in range(0, 8):
                if switch == 0:
                    board.append((i, j, 0))
                    switch = 1
                else:
                    board.append((i, j, 1))
                    switch = 0
    return board


def draw_board():
    board = make_board()

    # board params
    square_size = 64    # interface builds from this number

    # borders
    s_pos = 20
    ib = 3      # inner border
    ta = 24     # text area
    ob = 5      # outer border
    board_size = (square_size * 8)
    inner_size = board_size + ib * 2
    text_area_size = inner_size + ta * 2
    outer_size = text_area_size + ob * 2

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
    font = pg.font.SysFont(None, int(square_size * 0.4))

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


def main():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        main_surface.fill(colors["background"])
        screen.blit(main_surface, (0, 0))
        draw_board()

        # keep at the end
        pg.display.flip()
        clock.tick(60)


main()
