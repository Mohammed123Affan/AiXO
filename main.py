import sys
import copy
import random
import pygame
import numpy as np
from constant import *

# PYGAME SETUP
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_color)


class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        self.empty_sqrs = self.squares
        self.mark_sqrs = 0

    def final_state(self, show=False):
        """
        return:  0 if there is no win yet
        return:  1 if player 1 win
        return:  2 if player 2 win
        """
        # vertical win
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] == self.squares[4][col] != 0:
                if show:
                    color = circ_color if self.squares[0][col] == 2 else cross_color
                    ipos = (col * sqsize + sqsize // 2, 12)
                    fpos = (col * sqsize + sqsize // 2, height - 12)
                    pygame.draw.line(screen, color, ipos, fpos, line_width)
                return self.squares[0][col]
        # horizontal win
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] == self.squares[row][4] != 0:
                if show:
                    color = circ_color if self.squares[row][0] == 2 else cross_color
                    ipos = (12, row * sqsize + sqsize // 2)
                    fpos = (width - 12, row * sqsize + sqsize // 2)
                    pygame.draw.line(screen, color, ipos, fpos, line_width)
                return self.squares[row][0]
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] == self.squares[4][4] != 0:
            if show:
                color = circ_color if self.squares[1][1] == 2 else cross_color
                ipos = (12, 12)
                fpos = (width - 12, height - 12)
                pygame.draw.line(screen, color, ipos, fpos, cross_width)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[0][4] == self.squares[1][3] == self.squares[2][2] == self.squares[3][1] == self.squares[4][0] != 0:
            if show:
                color = circ_color if self.squares[2][2] == 2 else cross_color
                ipos = (12, height - 12)
                fpos = (width - 12, 12)
                pygame.draw.line(screen, color, ipos, fpos, cross_width)
            return self.squares[1][1]

        # No win yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.mark_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.mark_sqrs == 25

    def isempty(self):
        return self.mark_sqrs == 0


def rnd(board):
    empty_sqrs = board.get_empty_sqrs()
    idx = random.randrange(0, len(empty_sqrs))

    return empty_sqrs[idx]


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def minimax(self, board, maximizing):
        print("find")
        # terminal case
        case = board.final_state()

        # player 1 win
        if case == 1:
            return 1, None  # eval , move
        # player 2 win
        if case == 2:
            return -1, None  # eval , move
        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)
        print(f'AI has chosen to mark the square in pos {move} with an eval of {eval}')
        return move


def show_lines():
    # BG
    screen.fill(BG_color)
    # vertical
    pygame.draw.line(screen, line_color, (sqsize, 0), (sqsize, height), line_width)
    pygame.draw.line(screen, line_color, (2*sqsize, 0), (2*sqsize, height), line_width)
    pygame.draw.line(screen, line_color, (width - 2*sqsize, 0), (width - 2*sqsize, height), line_width)
    pygame.draw.line(screen, line_color, (width - sqsize, 0), (width - sqsize, height), line_width)
    # horizontal
    pygame.draw.line(screen, line_color, (0, sqsize), (width, sqsize), line_width)
    pygame.draw.line(screen, line_color, (0, 2*sqsize), (width, 2*sqsize), line_width)
    pygame.draw.line(screen, line_color, (0, height - 2*sqsize), (width, height - 2*sqsize), line_width)
    pygame.draw.line(screen, line_color, (0, height - sqsize), (width, height - sqsize), line_width)


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'  # pvp or ai
        self.running = True
        show_lines()

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def draw_fig(self, row, col):
        if self.player == 1:
            # DRAW CROSS
            # desc line
            start_desc = (col * sqsize + offset, row * sqsize + offset)
            end_desc = (col * sqsize + sqsize - offset, row * sqsize + sqsize - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)
            # asc line
            start_asc = (col * sqsize + offset, row * sqsize + sqsize - offset)
            end_asc = (col * sqsize + sqsize - offset, row * sqsize + offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)
        elif self.player == 2:
            # DRAW CIRCLE
            center = (col * sqsize + sqsize // 2, row * sqsize + sqsize // 2)
            pygame.draw.circle(screen, circ_color, center, radius, circ_width)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def reset(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()


def main():
    # object
    game = Game()
    board = game.board
    ai = game.ai
    # main loop
    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                # r-restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // sqsize
                col = pos[0] // sqsize

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update the screen
            pygame.display.update()
            # AI methods
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False

        pygame.display.update()


main()
