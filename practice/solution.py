class slice :
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0

    def __init__(self):
        pass

    def add_x(self):
        pass

    def add_y(self):
        pass

    def transpose(self):
        pass


def parse_config(line):
    r, c, l, h = line.split(sep=' ')

    return {
        'rows': int(r),
        'cols': int(c),
        'min_ingridients': int(l),
        'slice_limit': int(h),
    }

def cut_pizza(dateset, config):
    for line in dateset:
        print(line)


if __name__ == "__main__":
    dateset = open('a_example.in', encoding='UTF-8')
    config = parse_config(dateset.readline())
    print(config)
    cut_pizza(dateset, config)

