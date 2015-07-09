__author__ = 'rex8312'

import random
from Objects import *
from Consts import *
from sqlitedict import SqliteDict


class PlayerAI:
    next_unit = None
    money = 15
    team = None
    hq = None

    def random_act(self, state):
        if self.next_unit is None:
            x = random.choice(range(3))
            y = random.choice(range(3))
            unit = random.choice([Rock(self.team, x, y),
                                  Paper(self.team, x, y),
                                  Scissors(self.team, x, y)])
            self.next_unit = unit
            print self.team, 'pending', unit.__class__

        unit = self.next_unit
        if unit.cost <= self.money:
            x, y = unit.next_move
            state[y][x][self.team].append(unit)
            self.money -= unit.cost
            self.next_unit = None
            print self.team, 'build', unit.__class__

        return state


class RedPlayerAI(PlayerAI):
    def __init__(self, hq):
        self.team = TEAM.RED
        self.hq = hq
        self.act = self.random_act


class BluePlayerAI(PlayerAI):
    def __init__(self, hq):
        self.team = TEAM.BLUE
        self.hq = hq
        self.act = self.random_act


def group_ai(state):
    for y in range(3):
        for x in range(3):
            for entity in state[y][x][TEAM.RED]:
                if len(state[y][x][TEAM.BLUE]) > 0:
                    target = random.choice(state[y][x][TEAM.BLUE])
                    entity.attack_to(target)
                elif not isinstance(entity, HQ):
                    x = random.choice(range(3))
                    y = random.choice(range(3))
                    entity.move_to(x, y)
            for entity in state[y][x][TEAM.BLUE]:
                if len(state[y][x][TEAM.RED]) > 0:
                    target = random.choice(state[y][x][TEAM.RED])
                    entity.attack_to(target)
                elif not isinstance(entity, HQ):
                    x = random.choice(range(3))
                    y = random.choice(range(3))
                    entity.move_to(x, y)
    return state