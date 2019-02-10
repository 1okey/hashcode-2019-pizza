from itertools import product
from collections import Counter

from benchmark import measure_time


class Slice:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def transpose(self):
        pass

    @property
    def cords(self):
        return f"{self.y1} {self.x1} {self.y2} {self.x2}"

    def __str__(self):
        return self.cords

    def __repr__(self):
        return self.cords


class Pizza:
    ING_COUNT = 2

    def __init__(self, dataset):
        self.data = list()
        self.slices = list()

        self.height = 0
        self.width = 0
        self.min_ing = 0
        self.max_size = 0

        self.current_x = 0
        self.current_y = 0
        self.load_dataset(dataset)
        self.combinations = self.create_combinations()

    @measure_time
    def load_dataset(self, dataset):
        with open(dataset) as file:
            raw_conf = file.readline()
            self.height, self.width, self.min_ing, self.max_size = [int(i) for i in raw_conf.split()]

            for line in file:
                line = line.strip()
                self.data.append(list(line))

    def create_combinations(self):
        data = list()
        for x, y in product(list(range(1, self.max_size + 1)), repeat=2):
            mul = x * y
            if 1 < mul <= self.max_size:
                data.append((x, y))
        return sorted(data, key=lambda tup: tup[0] + tup[1])

    def is_cut(self):
        return self.current_y >= self.height

    def meets_conditions(self, slice):
        if not slice:
            return False

        ingridients = Counter()
        for row in slice:
            ingridients += Counter(row)

        ing_cond = len(ingridients.keys()) == self.ING_COUNT
        size_cond = sum(ingridients.values()) <= self.max_size
        M_cond = ingridients.get('M', 0) >= self.min_ing
        T_cond = ingridients.get('T', 0) >= self.min_ing

        return all([ing_cond, size_cond, M_cond, T_cond])

    @measure_time
    def cut_slices(self):
        while not self.is_cut():
            is_sliced = False
            for combo_y, combo_x in self.combinations:
                y2 = (self.current_y + combo_y)
                x2 = (self.current_x + combo_x)

                slice_col = slice(self.current_x, x2)
                p_slice = [self.data[y][slice_col] for y in range(self.current_y, y2) if (y + 1) <= self.height]
                if self.meets_conditions(p_slice):
                    self.slices.append(Slice(self.current_x, self.current_y, x2 - 1, y2 - 1))

                    for y in range(self.current_y, y2):
                        if (y + 1) <= self.height:
                            for x in range(self.current_x, x2):
                                self.data[y][x] = '*'

                    self.current_x = x2 % self.width
                    self.current_y = self.current_y if x2 < self.width else y2
                    is_sliced = True
                    break
            if not is_sliced:
                self.current_x += 1
                if self.current_x >= self.width:
                    self.current_x %= self.width
                    self.current_y += 1

    @measure_time
    def save_result(self, f_name):
        result = "\n".join([item.cords for item in self.slices])
        with open(f"{f_name}.out", mode="w") as file:
            file.write(f"{len(self.slices)}\n")
            file.write(result)


if __name__ == "__main__":
    pizza = Pizza(dataset="./datasets/b_small.in")
    # Tests
    pizza.save_result(f_name='b_small')
