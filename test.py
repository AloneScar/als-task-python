import curses
from curses.textpad import Textbox, rectangle

def main(stdscr):
    curses.echo()            # Enable echoing of characters

    # Get a 15-character string, with the cursor on the top line
    s = stdscr.getstr(0,0, 15)
    print(s.decode())
    curses.unecho()

curses.wrapper(main)