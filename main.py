from typing import Deque, List, TypeAlias
from enum import Enum
from dataclasses import dataclass
from itertools import product
from random import randint
from copy import deepcopy
from collections import deque
import curses


class InputKeys(Enum):
    right = curses.KEY_RIGHT
    left  = curses.KEY_LEFT
    up    = curses.KEY_UP
    down  = curses.KEY_DOWN


class BlockType(Enum):
    empty = ' '
    head  = 'o'
    tail  = 'a'
    food  = '@'
    edge  = 'x'


@dataclass
class Vec:
    x: int
    y: int

    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)


class Direction(Enum):
    right = Vec(1, 0)
    left  = Vec(-1, 0)
    up    = Vec(0, -1)
    down  = Vec(0, 1)


@dataclass
class Block:
    type: BlockType
    pos: Vec


Blocks: TypeAlias = List[Block]


class Game:
    def __init__(self, width, height) -> None:
        self._WIDTH, self._HEIGHT = width, height
        assert self._WIDTH > 5 and self._HEIGHT > 5
        self.board: Blocks
        self.player_direction: Direction
        self.running: int
        self.tail_stack: Deque[Vec]
        self.food: int

    def init(self) -> None:
        self.food = 3
        self.board = self.initialize_board()
        self.running = True
        self.tail_stack = deque()

    # legacy
    def print_board(self) -> None:
        m = self.get_pos_matrix()
        for r in m:
            for c in r:
                print(c.value, end='')
            print()

    def initialize_board(self) -> Blocks:
        p = product(range(self._WIDTH), range(self._HEIGHT))
        l = [Block(BlockType.edge, Vec(x, y))
                 if x in [0, self._WIDTH-1] or y in [0, self._HEIGHT-1]
                 else Block(BlockType.empty, Vec(x, y)) for x, y in p]
        while True:
            r = randint(0, len(l)-1)
            if l[r].type == BlockType.empty:
                break
        l[r].type = BlockType.head
        b = self.spawn_food(l)
        return b

    def move_player(self) -> Blocks:
        bs = deepcopy(self.board)
        p = self.get_player_head()
        v = self.player_direction.value
        old_pos = deepcopy(p.pos)
        for i, b in enumerate(bs):  # clear tails
            if b.type == BlockType.tail:
                bs[i] = Block(BlockType.empty, b.pos)
        if self.tail_stack:  # remove tail end
            bs = self.replace_block(bs, 
                Block(BlockType.empty, self.tail_stack.pop()))
            self.tail_stack.appendleft(old_pos)
            for pos in self.tail_stack:
                bs = self.replace_block(bs, Block(BlockType.tail, pos))
        else:
            bs = self.replace_block(bs, Block(BlockType.empty, old_pos))
        match self.get_block(old_pos + v).type:
            case BlockType.empty:
                p = Block(BlockType.head, old_pos + v)
                bs = self.replace_block(bs, p)
            case BlockType.tail:
                self.running = False
            case BlockType.edge:
                self.running = False
            case BlockType.food:
                self.tail_stack.appendleft(old_pos)
                bs = self.replace_block(bs, Block(BlockType.head, old_pos + v))
                bs = self.spawn_food(bs)
        return bs

    def replace_block(self, bs: Blocks, nb: Block) -> Blocks:
        bs = deepcopy(bs)
        for i, b in enumerate(bs):
            if b.pos == nb.pos:
                bs[i] = nb
        return bs

    def get_block(self, p: Vec) -> Block:
        return [b for b in self.board if b.pos == p][0]

    def get_player_head(self) -> Block:
        return [b for b in self.board if b.type is BlockType.head][0]

    def spawn_food(self, bs: Blocks) -> Blocks:
        bs = deepcopy(bs)
        food_count = lambda bs: \
            sum([1 for b in bs if b.type == BlockType.food])
        while food_count(bs) < self.food:
            r = randint(0, len(bs)-1)
            if bs[r].type == BlockType.empty:
                bs[r].type = BlockType.food
        return bs

    def get_pos_matrix(self) -> List[List[BlockType]]:
        m = [[BlockType.empty for _ in range(self._WIDTH)] 
                              for _ in range(self._HEIGHT)]
        for b in self.board:
            x, y = b.pos.x, b.pos.y
            m[y][x] = b.type
        return m


def handle_input(game: Game, c: int) -> None:
    match c:
        case InputKeys.right.value:
            game.player_direction = Direction.right
        case InputKeys.left.value:
            game.player_direction = Direction.left
        case InputKeys.up.value:
            game.player_direction = Direction.up
        case InputKeys.down.value:
            game.player_direction = Direction.down


def draw_board(game: Game) -> None:
    for x, r in enumerate(game.get_pos_matrix()):
        for y, c in enumerate(r):
            stdscr.addch(x, y, f"{c.value}")


def main(stdscr):
    global score
    game = Game(20, 10)
    game.init()

    stdscr.nodelay(False)
    draw_board(game)
    c = stdscr.getch()
    handle_input(game, c)
    stdscr.nodelay(True)
    while game.running:
        assert len(game.board) == 200
        c = stdscr.getch()
        curses.halfdelay(3)
        handle_input(game, c)

        game.board = game.move_player()

        stdscr.clear()

        draw_board(game)

        stdscr.refresh()

    score = len(game.tail_stack)


if __name__ == '__main__':
    score = 0
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.wrapper(main)

    curses.nocbreak()
    stdscr.keypad(False)
    stdscr.nodelay(False)
    curses.echo()

    curses.endwin()

    print('your length: ', score)

