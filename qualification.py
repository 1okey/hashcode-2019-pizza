import logging
from collections import defaultdict, namedtuple, Counter
from random import choice

from benchmark import measure_time

# init logger for DEBUG
logger = logging.getLogger('hashcode-2019')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('hashcode-2019.log', 'w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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

        for photo_index, line in enumerate(file):
            line = line.replace('\n', '')
            orientation, number_of_tags, *tags = line.split(' ')
            photos[photo_index] = photo(photo_index, orientation, set(tags), number_of_tags)

            for tag in tags:
                tag_map[tag].append(photo_index)

        return number_slides, photos, tag_map


def get_max_mention(counter, necessary_orientation=None):
    """

    :param Counter counter:
    :param necessary_orientation:
    :return:
    """
    for item in counter.most_common():
        if not necessary_orientation:
            return item[0]
        elif item[1].orientation != necessary_orientation:
            continue
        else:
            return item[1].index

    return None


def get_interesting_photo(last_photo, photos, tag_map, necessary_orientation=None):
    """
    Searches for matching photos by tag intersection and orientation
    :param namedtuple last_photo:
    :param dict photos:
    :param dict tag_map:
    :param str necessary_orientation: 'V'
    :return list:
    """
    possible_photos = []
    for tag in last_photo.tags:
        for photo in tag_map[tag]:
            # the index of the last photo is ignored and
            # it is checked that the photo is in the collection
            if (photo != last_photo.index) and (photo in photos):
                possible_photos.append(photo)

    # intersection of tags was replaced by counting references
    # of photos by tags of the last photo
    number_of_mentions = Counter(possible_photos)
    if number_of_mentions and necessary_orientation:

        for key, value in number_of_mentions.items():
            number_of_mentions[key] = photos[key]

        return get_max_mention(number_of_mentions, necessary_orientation)
    elif number_of_mentions:
        return get_max_mention(number_of_mentions, necessary_orientation)

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
            second_photo_index = get_interesting_photo(first_photo, photos, tag_map, necessary_orientation='V')
            if second_photo_index:
                slide.append(second_photo_index)

    return slide


def save_result(file_name, result):
    print('Save result')
    with open(f"./results/{file_name}.out", mode="w") as file:
        file.write(str(len(result)) + '\n')
        data = '\n'.join(result)
        file.write(data)


@measure_time
def solution_one(file_name):
    slides = []
    used_photos_numb = 0  # for statistics
    number_slides, photos, tag_map = read_input(file_name)

    # take the first photo to start
    last_photo = photos[0]
    used_photos_numb += 1
    slides.append(str(last_photo.index))
    del photos[0]

    while photos:
        photos_found = create_slide(last_photo, photos, tag_map)
        if photos_found:
            last_photo = photos[photos_found[-1]]
            used_photos_numb += len(photos_found)
            slides.append(' '.join([str(item) for item in photos_found]))

            # delete photo from collection
            for key in photos_found:
                if key in photos:
                    del photos[key]
        else:
            # if no suitable photos are found - randomly choose from available ones
            random_index = choice(list(photos.keys()))
            logger.debug(f'Choose random photo index: {random_index}')
            last_photo = photos[random_index]
            used_photos_numb += 1
            slides.append(str(random_index))
            del photos[random_index]

    print(f'All photo: {number_slides}, used photos: {used_photos_numb}, unused photo: {number_slides - used_photos_numb}')
    save_result(file_name, slides)


if __name__ == "__main__":
    datasets = [
        'a_example',
        'b_lovely_landscapes',
        'c_memorable_moments',
        # 'd_pet_pictures',
        # 'e_shiny_selfies',
    ]
    for in_file in datasets:
        solution_one(in_file)
