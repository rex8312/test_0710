__author__ = 'rex8312'

import time
import numpy as np
import pylab as pl
from AI import *


def update(state):
    _state = [[(list(), list()) for x in range(3)] for y in range(3)]

    for y in range(3):
        for x in range(3):
            for team in (TEAM.RED, TEAM.BLUE):
                for entity in state[y][x][team]:
                    if entity.hp > 0:
                        _x, _y = entity.next_move
                        _state[_y][_x][team].append(entity)
    return _state


def draw(state_view, progress_view, state, tick):
    print
    state_view.cla()
    values = np.zeros((3, 4))
    for y in range(3):
        for x in range(3):
            for entity in state[y][x][TEAM.RED]:
                values[y][x] += entity.hp
            for entity in state[y][x][TEAM.BLUE]:
                values[y][x] -= entity.hp
            values[y][x] = min(values[y][x], 100)
            values[y][x] = max(values[y][x], -100)

    values[0][3] = 100
    values[1][3] = 0
    values[2][3] = -100

    print values
    state_view.imshow(values, interpolation='nearest', cmap='bwr')

    progress_view.cla()
    xs = np.arange(0, 2 * np.pi, 0.01)
    ys = np.sin(xs + tick * 0.1)
    progress_view.plot(ys)

    pl.pause(1./FPS)


def game():
    tick = 0
    state = [[(list(), list()) for x in range(3)] for y in range(3)]

    red_hq = HQ(TEAM.RED, 1, 0)
    blue_hq = HQ(TEAM.BLUE, 1, 2)

    state[0][1][TEAM.RED].append(red_hq)
    state[2][1][TEAM.BLUE].append(blue_hq)

    red_player_ai = RedPlayerAI(red_hq)
    blue_player_ai = BluePlayerAI(blue_hq)

    fig, (state_view, progress) = pl.subplots(2, 1)

    while True:
        if red_player_ai.hq.hp <= 0 and blue_player_ai.hq.hp <= 0:
            return RESULT.DRAW
        elif red_player_ai.hq.hp <= 0:
            return RESULT.BLUE_WIN
        elif blue_player_ai.hq.hp <= 0:
            return RESULT.RED_WIN

        print 'R', red_player_ai.money, red_hq.hp
        print 'B', blue_player_ai.money, blue_hq.hp
        state = red_player_ai.act(state)
        state = blue_player_ai.act(state)
        state = group_ai(state)
        state = update(state)
        red_player_ai.money += 1
        blue_player_ai.money += 1
        state = update(state)
        draw(state_view, progress, state, tick)
        tick += 1



if __name__ == '__main__':
    pl.ion()
    print game()
