import argparse
import logging
import os

from PIL import Image


def chCollor(PATH, NEXT_COLOR):
    pngs = [f for f in os.listdir(PATH) if f.endswith('png')]
    svgs = [f for f in os.listdir(PATH) if f.endswith('svg')]
    logging.debug('Fount %d images' % (len(pngs)+len(svgs)))
    if not os.path.exists(os.path.join(PATH, 'out')):
        os.makedirs(os.path.join(PATH, 'out'))
    for png in pngs:
        chColorPng(png, PATH, NEXT_COLOR)
    for svg in svgs:
        chColorSvg(svg, PATH, NEXT_COLOR)


def chColorPng(png, PATH, NEXT_COLOR):
    logging.debug('Change %s images' % png)
    img = Image.open(os.path.join(PATH, png))
    k, j = img.size
    # img.show()
    for i in range(k):
        for ii in range(j):
            if not img.getpixel((i, ii))[3] == 0:
                alpha = img.getpixel((i, ii))[3]
                img.putpixel((i, ii), (NEXT_COLOR[0], NEXT_COLOR[1],
                                       NEXT_COLOR[2], alpha))
    img.save(os.path.join(PATH, 'out', png))
    logging.debug('save {}'.format(png))


def chColorSvg(svg, PATH, NEXT_COLOR):
    logging.debug('Change %s images' % svg)
    with open(os.path.join(PATH, svg), 'r') as img_file:
        img = img_file.read()
    next_color_hex = "".join([f"{i:x}" for i in NEXT_COLOR])
    new_img = img.replace('/>', f' fill="#{next_color_hex}" />')
    with open(os.path.join(PATH, 'out', svg), 'w') as img_save_file:
        img_save_file.write(new_img)
    logging.debug('save {}'.format(svg))


def split_list_from_collor(color):
    return list(map(int, color.replace('(', '').replace(')', '').split(',')))


def convert_to_RJB(color):
    if ',' in color:
        return split_list_from_collor(color)
    color = color[1:] if color.startswith('#') else color
    return list(int(color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Сhanges all colors of all \
        images in the specified folder to the specified one')
    parser.add_argument('-c', '--color', default='D41920',
                        help="color to chage")
    parser.add_argument('-p', '--path', default='./img/',
                        help="set path to picture")
    parser.add_argument('--verbose', '-v', action='store_true', default=0)
    args = parser.parse_args()
    NEXT_COLOR = convert_to_RJB(args.color)
    logging.basicConfig(format='%(asctime)s %(message)s',
                        level=logging.DEBUG if args.verbose else logging.ERROR)
    chCollor(args.path, NEXT_COLOR)
