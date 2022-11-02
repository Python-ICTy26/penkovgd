import copy
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколени
        self.generations = 1
        # Находится ли игра на паузе
        self.is_on_pause = True

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        np = {
            (row - 1, col),
            (row - 1, col + 1),
            (row, col + 1),
            (row + 1, col + 1),
            (row + 1, col),
            (row + 1, col - 1),
            (row, col - 1),
            (row - 1, col - 1),
        }
        if row == 0:
            np -= {(row - 1, col)}
            np -= {(row - 1, col + 1)}
            np -= {(row - 1, col - 1)}
        if row == self.rows - 1:
            np -= {(row + 1, col)}
            np -= {(row + 1, col + 1)}
            np -= {(row + 1, col - 1)}
        if col == 0:
            np -= {(row, col - 1)}
            np -= {(row + 1, col - 1)}
            np -= {(row - 1, col - 1)}
        if col == self.cols - 1:
            np -= {(row, col + 1)}
            np -= {(row + 1, col + 1)}
            np -= {(row - 1, col + 1)}
        neighbours = [self.curr_generation[i[0]][i[1]] for i in np]
        return neighbours

    def get_next_generation(self) -> Grid:
        next_gen = copy.deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.curr_generation[i][j]
                neighbours = self.get_neighbours((i, j))
                if cell == 1:
                    if not 2 <= neighbours.count(1) <= 3:
                        next_gen[i][j] = 0
                else:
                    if neighbours.count(1) == 3:
                        next_gen[i][j] = 1
        self.generations += 1
        return next_gen

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()

    def pause(self) -> None:
        self.is_on_pause = not self.is_on_pause

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.get_next_generation() != self.curr_generation

    @staticmethod
    def from_file(filename) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        new_grid = []
        with open(filename, mode="r") as f:
            for line in f.readlines():
                new_grid.append([int(cell) for cell in line[:-1]])
        game = GameOfLife((len(new_grid), len(new_grid[0])))
        game.curr_generation = new_grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        str_to_save = ""
        with open(filename, mode="w") as f:
            for row in self.curr_generation:
                for cell in row:
                    str_to_save += str(cell)
                str_to_save += "\n"
            f.write(str_to_save)

    def toggle_cell(self, x, y) -> None:
        cell = self.curr_generation[y][x]
        if cell == 1:
            self.curr_generation[y][x] = 0
        else:
            self.curr_generation[y][x] = 1

    def run_one_step(self):
        if self.is_changing and not self.is_max_generations_exceeded and not self.is_on_pause:
            self.step()


if __name__ == "__main__":
    game = GameOfLife.from_file("grid.txt")
    print(game.curr_generation)
    game.step()
    print(game.curr_generation)
    game.save("save.txt")
