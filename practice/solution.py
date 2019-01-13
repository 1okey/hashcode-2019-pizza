from string import Template


class Slice :
    __x1 = 0
    __y1 = 0
    __x2 = 0
    __y2 = 0
    __template = Template("$y1 $x1 $y2 $x2")

    def __init__(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2

    def transpose(self):
        pass

    @property
    def cords(self):
        return self.__template.substitute(self.__y1, self.__x1, self.__y2, self.__x2)


class Pizza :
    __start_x = 0
    __start_y = 0
    __height  = 0
    __width   = 0
    __data    = list()
    __slices  = list()

    def __init__(self, config):
        self._height = config['rows']
        self._width = config['cols']

    def add_row(self, row):
        self.__data.append(row)

    def is_cut(self):
        return self.__start_x + 1 == self._width and \
               self.__start_y + 1 == self._height

    def meets_conditions(self):
        # TODO
        pass

    def cut_slices(self):
        while not self.is_cut():
            end_x, end_y = [0,0]

            while not self.meets_conditions():
                # TODO
                pass

            p_slice = Slice(self.__start_x, self.__start_y, end_x, end_y)
            self.__slices.append(p_slice)

    def save_result(self):
        output = open("output.out", mode='w')
        output.write(str(len(self.__slices)))
        for _slice in self.__slices:
            output.write(_slice.coords)


def parse_config(line):
    r, c, l, h = line.split(sep=' ')

    return {
        'rows': int(r),
        'cols': int(c),
        'min_ingredients': int(l),
        'slice_limit': int(h),
    }


def parse_pizza(dataset_, pizza_):
    for line in dataset_:
        pizza_.add_row(list(filter(lambda char: not char == '\n', line)))


if __name__ == "__main__":
    from benchmark import print_duration

    dataset = open('datasets/d_big.in', encoding='UTF-8')
    pizza = Pizza(config=parse_config(dataset.readline()))

    print_duration(parse_pizza, dataset, pizza)
    print_duration(pizza.cut_slices)
    print_duration(pizza.save_result)

