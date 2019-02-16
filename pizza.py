from collections import Counter
from benchmark import measure_time
from slice import Slice

class Pizza:
    ING_COUNT = 2

    def __init__(self, f_name):
        self.data = list()
        self.combinations = list()

        self.height = 0
        self.width = 0
        self.min_ingridients = 0
        self.max_size = 0
        self.x1 = 0
        self.y1 = 0
        
        self.load_dataset(f"./datasets/{f_name}.in")

    @measure_time
    def load_dataset(self, dataset):
        with open(dataset) as file:
            raw_conf = file.readline()
            self.height, self.width, self.min_ingridients, self.max_size = [int(i) for i in raw_conf.split()]

            for line in file:
                line = line.strip()
                self.data.append(list(line))


    def meets_conditions(self, slice):
        if not slice:
            return False

        ingridients = Counter()
        for row in slice:
            ingridients += Counter(row)

        ing_cond = len(ingridients.keys()) == self.ING_COUNT
        size_cond = sum(ingridients.values()) <= self.max_size
        M_cond = ingridients.get('M', 0) >= self.min_ingridients
        T_cond = ingridients.get('T', 0) >= self.min_ingridients

        return all([ing_cond, size_cond, M_cond, T_cond])

    @measure_time
    def cut_slices(self):
        slices = list()
        while self.y1 < self.height:
            if self.x1 < self.width and self.y1 < self.height and self.data[self.y1][self.x1] == '*':
                self.y1 += self.x1 // self.width
                self.x1 = self.x1 % self.width + 1
                continue

            for combo_y, combo_x in self.combinations:
                y2 = (self.y1 + combo_y)
                x2 = (self.x1 + combo_x)

                slice_col = slice(self.x1, x2)
                p_slice = [self.data[y][slice_col] for y in range(self.y1, y2) if (y + 1) <= self.height]
                if self.meets_conditions(p_slice):
                    slices.append(Slice(self.x1, self.y1, x2 - 1, y2 - 1))

                    for y in range(self.y1, y2):
                        if (y + 1) <= self.height:
                            for x in range(self.x1, x2):
                                self.data[y][x] = '*'
                    break

            self.y1 += self.x1 // self.width
            self.x1 = self.x1 % self.width + 1
        return slices