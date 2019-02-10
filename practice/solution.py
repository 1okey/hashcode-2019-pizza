from pprint import pprint
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


class Pizza:
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

    @measure_time
    def load_dataset(self, dataset):
        with open(dataset) as file:
            raw_conf = file.readline()
            self.height, self.width, self.min_ing, self.max_size = [int(i) for i in raw_conf.split()]

            for line in file:
                line = line.strip()
                self.data.append(line)

    def is_cut(self):
        return self.current_x + 1 == self.width and self.current_y + 1 == self.height

    def meets_conditions(self, slice):
        ingridients = Counter()
        for row in slice:
            ingridients += Counter(row)
        return (len(slice[0]) * len(slice) <= self.max_size
                and len(ingridients.keys()) == 2
                and )

    @measure_time
    def cut_slices(self):
        while not self.is_cut():
            end_x, end_y = [self.current_x, self.current_y]
            y = self.current_y
            p_slice = list()
            while not self.meets_conditions(p_slice):

                while not y <= end_y:
                    p_slice.append(self.data[y][self.current_x:end_x])
                    y += 1

                end_x += 1

            p_slice = Slice(self.current_x, self.current_y, end_x, end_y)
            self.slices.append(p_slice)

    @measure_time
    def save_result(self):
        result = "\n".join([item.cords for item in self.slices])
        with open("output.out", mode="w") as file:
            file.write(f"{len(self.slices)}\n")
            file.write(result)


if __name__ == "__main__":
    pizza = Pizza(dataset="./datasets/b_small.in")
    # Tests
    pprint(pizza.data)
    test = [Slice(i, i, i, i) for i in range(5)]
    pizza.slices = test
    pizza.save_result()
