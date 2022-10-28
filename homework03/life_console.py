import curses
import time
from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border()
        screen.resize(self.life.rows + 2, self.life.cols + 2)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for y in range(self.life.rows):
            for x in range(self.life.cols):
                if self.life.curr_generation[y][x] == 1:
                    screen.addch(y + 1, x + 1, "ඞ") # \u2588
                else:
                    screen.addch(y + 1, x + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        while True:
            self.draw_borders(screen)
            self.draw_grid(screen)
            time.sleep(.3)
            self.life.step()
            screen.refresh()


if __name__ == "__main__":
    console = Console(GameOfLife((15, 40)))
    console.run()
