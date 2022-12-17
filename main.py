#coding=utf-8
import curses
import operation

conn, cur = operation.connect_database()
tasks = operation.load_tasks(cur)
current_task_index = 0

def show_tasks(stdscr):
    stdscr.clear()
    for idx, task in enumerate(tasks):
        depth = task['depth']
        content = task['content']
        state = task['state']
        x = depth * 4
        y = idx
        if idx == current_task_index:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, "* {} {}".format(state, content))
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, "* {} {}".format(state, content))

    stdscr.refresh()

def add_brother_task(stdscr):
    current_task = tasks[current_task_index]
    task = operation.default_task(content="", depth=current_task['depth'])
    tasks.insert(current_task_index + 1, task)
    show_tasks(stdscr)
    curses.echo()
    content = stdscr.getstr(current_task_index + 1, task['depth'] * 4 + len(task['state']) + 3, 50)
    tasks[current_task_index + 1]['content'] = content.decode().strip()
    curses.noecho()

def main(stdscr):
    global current_task_index
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    show_tasks(stdscr)

    while True:
        key = stdscr.getch()
        stdscr.clear()

        if key in [curses.KEY_UP, 104, 107]:
            current_task_index -= 1
        elif key in [curses.KEY_DOWN, 106, 108]:
            current_task_index += 1
        elif key == 113:
            break
        if current_task_index == -1:
            current_task_index = len(tasks) - 1
        elif current_task_index == len(tasks):
            current_task_index = 0
        if key == curses.KEY_ENTER or key == 10:
            add_brother_task(stdscr)
            current_task_index += 1

        show_tasks(stdscr)

curses.wrapper(main)