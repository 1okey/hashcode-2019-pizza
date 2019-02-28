from benchmark import measure_time
from collections import defaultdict


@measure_time
def read_input(file_name):
    with open(f'datasets/{file_name}.txt') as file:
        number_slides = file.readline()
        tags_index = defaultdict(list)
        photos_index = dict()
        for p_index, line in enumerate(file):
            line = line.replace('\n', '')
            orientation, _, *tags = line.split(' ')
            photos_index[p_index] = dict(tags=set(tags), orientation=orientation, index=p_index)
            for tag in tags:
                tags_index[tag].append(dict(orientation=orientation, tags=set(tags), index=p_index, used=False))
        return [number_slides, tags_index, photos_index]


def find_interesting(photos_index, tags_index, cur_photo):
    possible_photos = list()
    best_photo = None
    interesting = None
    if cur_photo is None:
        print('AAAAAAAAAAAAAAAAAAAAAAAaa')

    current_tag_photo = cur_photo['tags']
    for tag in cur_photo['tags']:
        possible_photos.extend(tags_index[tag])

    possible_photos = {photo['index']: photo for photo in possible_photos if not photo['used']}
    possible_photos = possible_photos.values()
    for photo in possible_photos:
        if photo['index'] == cur_photo['index']:
            continue

        if interesting is None:
            best_photo = photo
            interesting = 0
            continue

        possible_tags = photos_index[photo['index']]['tags']
        inter = len(possible_tags.intersection(current_tag_photo))
        if interesting < inter:
            best_photo = photo
            interesting = inter
        if interesting >= len(current_tag_photo) / 2:
            break

    return best_photo


@measure_time
def create_slides(photos_index, tags_index):
    print('Create slides')
    index = 0
    last_photo = photos_index[index]
    photos_index[index]['used'] = True
    slides = list()
    while index <= len(photos_index.keys()):
        if not last_photo:
            break
        if last_photo['orientation'] == 'H':
            new_photo = find_interesting(photos_index, tags_index, last_photo)
            slides.append(str(last_photo['index']))
            last_photo['used'] = True
            last_photo = new_photo
            continue
        if last_photo['orientation'] == 'V':
            first_interesting = find_interesting(photos_index, tags_index, last_photo)
            second_interesting = find_interesting(photos_index, tags_index, first_interesting)
            slides.append('{}, {}'.format(last_photo['index'], first_interesting['index']))
            first_interesting['used'] = True
            last_photo['used'] = True
            last_photo = second_interesting
            continue
        index += 1
    return slides


def save_result(file_name, result):
    print('Save result')
    with open(f"./results/{file_name}.out", mode="w") as file:
        number = len(result)
        file.write(str(number) + '\n')
        data = ' \n'.join(result)
        file.write(data)


def solve_problem(file_name):
    number_slides, tags_index, photos_index = read_input(file_name)
    # pprint(photos_index)
    # pprint(tags_index)
    slides = create_slides(photos_index, tags_index)
    save_result(file_name, slides)


if __name__ == "__main__":
    for in_file in ["b_lovely_landscapes"]:
        solve_problem(in_file)
