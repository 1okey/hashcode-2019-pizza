# built-in modules
from itertools import product
from os import path, listdir
# specific modules
from benchmark import measure_time
from slice import Slice
from pizza import Pizza

def solve_problem(file_name):
    print(f"================= Starting {file_name} dataset =================")
    pizza = Pizza(f_name=file_name)
    pizza.combinations = create_slice_combinations(pizza.max_size)
    slices = pizza.cut_slices()
    save_result(file_name=file_name, slices=slices)
    print(f"================= Finished cutting {file_name} ================\n")

@measure_time
def save_result(file_name, slices):
    result = "\n".join([item.cords for item in slices])
    with open(f"./results/{file_name}.out", mode="w") as file:
        file.write(f"{len(slices)}\n")
        file.write(result)

@measure_time
def create_slice_combinations(max_size):
    data = list()
    for x, y in product(list(range(1, max_size + 1)), repeat=2):
        mul = x * y
        if 1 < mul <= max_size:
            data.append((x, y))
    return sorted(data, key=lambda tup: tup[0] + tup[1])

if __name__ == "__main__":
    for in_file in ["a_example", "b_small","c_medium", "d_big"]:
        solve_problem(in_file.split('.')[0])    

