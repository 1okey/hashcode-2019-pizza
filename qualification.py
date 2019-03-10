import logging
from collections import defaultdict, namedtuple, Counter
from random import choice

from benchmark import measure_time

# init logger for DEBUG
logger = logging.getLogger('hashcode-2019')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('hashcode-2019.log', 'w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

photo = namedtuple('Photo', 'index orientation tags number_tags')


@measure_time
def read_input(file_name):
    """
    Read dataset
    :param str file_name:
    :return int, dict, dict:
    """
    with open(f'datasets/{file_name}.txt') as file:
        number_slides = int(file.readline().replace('\n', ''))
        tag_map = defaultdict(list)
        photos = dict()
        tag_map['V'] = set()
        tag_map['H'] = set()

        for photo_index, line in enumerate(file):
            line = line.replace('\n', '')
            orientation, number_of_tags, *tags = line.split(' ')
            photos[photo_index] = photo(photo_index, orientation, set(tags), int(number_of_tags))

            if orientation == 'V':
                tag_map['V'].add(photo_index)
            else:
                tag_map['H'].add(photo_index)

            for tag in tags:
                tag_map[tag].append(photo_index)

        return number_slides, photos, tag_map


def get_interesting_photo(last_photo, photos, tag_map):
    """
    Searches for matching photos by tag intersection and orientation
    :param namedtuple last_photo:
    :param dict photos:
    :param dict tag_map:
    :return list:
    """
    if last_photo.number_tags == 1:
        optimal_intersection = 1
    else:
        optimal_intersection = last_photo.number_tags // 2
    counter = Counter()
    for tag in last_photo.tags:
        for photo in tag_map[tag]:
            # the index of the last photo is ignored and
            # it is checked that the photo is in the collection
            if (photo != last_photo.index) and (photo in photos):
                counter[photo] += 1

            # do lazy processing if it possible
            if counter[photo] >= optimal_intersection:
                logger.debug(f'Optimal intersection: {photo}')
                return photo

    if counter:
        return counter.most_common()[0][0]
    return None


def create_slide(last_photo, photos, tag_map):
    """
    Creates a slide. May consist of one horizontal photo or two vertical
    :param namedtuple last_photo:
    :param dict tag_map:
    :param dict photos:
    :return list:
    """
    slide = []
    first_photo_index = get_interesting_photo(last_photo, photos, tag_map)
    if first_photo_index:
        slide.append(first_photo_index)
        first_photo = photos[first_photo_index]

        if first_photo.orientation == 'V':
            random_v_photo = get_random_oriented_photo(photos, tag_map, 'V', exclude=[first_photo_index])
            slide.append(random_v_photo)

        if first_photo.orientation == 'V' and len(slide) < 2:
            logger.debug(f'Saved one vertical photo: {first_photo_index}')

    return slide


def save_result(file_name, result):
    with open(f"./results/{file_name}.out", mode="w") as file:
        file.write(str(len(result)) + '\n')
        data = '\n'.join(result)
        file.write(data)


def get_random_oriented_photo(photos, tag_map, orient, exclude=None):
    """
    Get a random photo according to orientation
    :param dict photos:
    :param dict tag_map:
    :param str orient: 'H' or 'V'
    :param exclude:
    :return:
    """
    if exclude is None:
        exclude = []

    existing_photo = set(photos.keys())
    existing_orient_photo = existing_photo.intersection(tag_map[orient])
    for item in exclude:
        existing_orient_photo.remove(item)
    random_index = choice(list(existing_orient_photo))

    existing_orient_photo.remove(random_index)
    tag_map[orient] = existing_orient_photo
    return random_index


@measure_time
def solution_one(file_name):
    slides = []
    randomly_selected_photos = 0  # for statistics
    number_slides, photos, tag_map = read_input(file_name)

    # take a first horizontal photo to start
    for key, value in photos.items():
        if value.orientation == 'H':
            last_photo = value
            slides.append(str(last_photo.index))

            del photos[last_photo.index]
            break

    while photos:
        print(len(photos))
        photos_found = create_slide(last_photo, photos, tag_map)
        if photos_found:
            last_photo = photos[photos_found[-1]]
            slides.append(' '.join([str(item) for item in photos_found]))

            # delete photo from collection
            for key in photos_found:
                if key in photos:
                    del photos[key]
        else:
            # if no suitable photos are found - randomly choose from available ones
            random_index = get_random_oriented_photo(photos, tag_map, 'H')

            last_photo = photos[random_index]
            randomly_selected_photos += 1
            slides.append(str(random_index))
            del photos[random_index]

    print(f'All photo: {number_slides}, randomly selected photos: {randomly_selected_photos}')
    save_result(file_name, slides)


if __name__ == "__main__":
    datasets = [
        # 'a_example',
        # 'b_lovely_landscapes',
        # 'c_memorable_moments',
        'd_pet_pictures',
        # 'e_shiny_selfies',
    ]
    for in_file in datasets:
        solution_one(in_file)
        print()
