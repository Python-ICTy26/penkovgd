import curses
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.resize(self.life.rows + 2, self.life.cols + 2)
        screen.border()

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    screen.addch(y + 1, x + 1, "\u2588")  # \u2588 ඞ
                else:
                    screen.addch(y + 1, x + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.mousemask(1)
        screen.keypad(True)
        self.draw_borders(screen)
        self.draw_grid(screen)
        while True:
            self.life.run_one_step()
            curses.napms(300)
            self.draw_grid(screen)
            screen.nodelay(True)
            event = screen.getch()
            if event == ord(" "):
                self.life.pause()
            elif event == ord("q"):
                break
            elif event == curses.KEY_MOUSE:
                _, mx, my, _, _ = curses.getmouse()
                self.life.toggle_cell(mx - 1, my - 1)
            screen.refresh()


if __name__ == "__main__":
    console = Console(GameOfLife((20, 40)))
    console.run()
