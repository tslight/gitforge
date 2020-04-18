"""
Simple ncurses pad scrolling.
"""

import cgitb
import curses
import curses.ascii
import os
import re
from .culor import addstr

os.environ.setdefault("ESCDELAY", "12")  # otherwise it takes an age!
# better curses debugging
cgitb.enable(format="text")


def event_loop(stdscr, lines):
    lines = re.split(f"{os.linesep}|\\n|\\r|\\x1b\\[0K", lines)
    # lines = [line for line in lines if line]
    maxy, maxx = stdscr.getmaxyx()
    longest = len(max(lines, key=len))
    pad = curses.newpad(len(lines), longest + 1)
    pad.keypad(True)  # use function keys
    curses.curs_set(0)  # hide the cursor
    curses.start_color()
    pminrow = 0  # pad row to start displaying contents at
    pmincol = 0  # pad column to start displaying contents at
    while True:
        # draw lines
        for idx, line in enumerate(lines):
            # pad.addstr(idx, 0, line)
            addstr(pad, idx, 0, line)

        # refresh components
        stdscr.noutrefresh()
        pad.noutrefresh(pminrow, pmincol, 0, 0, maxy - 1, maxx - 1)
        curses.doupdate()

        # react to input
        key = stdscr.getch()

        if key == ord("q") or key == curses.ascii.ESC:
            break

        if key == ord("k") or key == curses.KEY_UP:
            if pminrow > 0:
                pminrow -= 1
        elif key == ord("j") or key == curses.KEY_DOWN:
            if pminrow < len(lines) - maxy:
                pminrow += 1
        elif key == ord("h") or key == curses.KEY_LEFT:
            if pmincol > 0:
                pmincol -= 1
        elif key == ord("l") or key == curses.KEY_RIGHT:
            if pmincol < longest - maxx:
                pmincol += 1
        elif key == ord("f") or key == curses.KEY_NPAGE:
            if pminrow < len(lines) - maxy:
                pminrow += maxy
            if pminrow > len(lines) - maxy:
                pminrow = len(lines) - maxy
        elif key == ord("b") or key == curses.KEY_PPAGE:
            if pminrow > 0:
                pminrow -= maxy
        elif key == ord("g") or key == curses.KEY_HOME:
            pminrow = 0
        elif key == ord("G") or key == curses.KEY_END:
            pminrow = len(lines) - maxy
        elif key == curses.KEY_RESIZE:
            stdscr.erase()
            pad.erase()
            maxy, maxx = stdscr.getmaxyx()


def pager(lines):
    curses.wrapper(event_loop, lines)
