class Slice :
    _x1 = 0
    _y1 = 0
    _x2 = 0
    _y2 = 0

    def __init__(self):
        pass

    def add_x(self):
        pass

    def add_y(self):
        pass

    def transpose(self):
        pass


class Pizza :
    _start_x = 0
    _start_y = 0
    _height = 0
    _width = 0
    _data = list()
    _slices = list()

    def __init__(self, config):
        self._height = config['rows']
        self._width = config['cols']

    def add_row(self, row):
        self._data.append(row)

    def cut_slices(self):
        pass

    def save_result(self):
        pass


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
        pizza_.add_row(
            list(
                filter(lambda char: not char == '\n', line)
            )
        )


if __name__ == "__main__":
    from benchmark import print_duration

    dataset = open('datasets/d_big.in', encoding='UTF-8')
    pizza = Pizza(config=parse_config(dataset.readline()))

    print_duration(parse_pizza, dataset, pizza)
    print_duration(pizza.cut_slices)
    print_duration(pizza.save_result)

