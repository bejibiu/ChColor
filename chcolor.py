import logging
import os
import sys

from PIL import Image

PATH = './img/'
LEVEL = logging.WARNING
NEXT_COLOR = [255, 255, 255]  # #D41920


def chCollor(PATH, NEXT_COLOR):
    pngs = [f for f in os.listdir(PATH) if f.endswith('png')]
    svgs = [f for f in os.listdir(PATH) if f.endswith('svg')]
    logging.info('Fount %d images' % (len(pngs)+len(svgs)))
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
    logging.info('save {}'.format(png))


def chColorSvg(svg, PATH, NEXT_COLOR):
    logging.debug('Change %s images' % svg)
    with open(os.path.join(PATH, svg), 'r') as img_file:
        img = img_file.read()
    next_color_hex = "".join([f"{i:x}" for i in NEXT_COLOR])
    new_img = img.replace('/>', f' fill="#{next_color_hex}" />')
    with open(os.path.join(PATH, 'out', svg), 'w') as img_save_file:
        img_save_file.write(new_img)
    logging.info('save {}'.format(svg))


def split_list_from_collor(color):
    return list(map(int, color.replace('(', '').replace(')', '').split(',')))


def convert_to_RJB(color):
    if ',' in color:
        return split_list_from_collor()
    else:
        return list(int(color[i:i+2], 16) for i in (0, 2, 4))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if '-nc' in sys.argv:
            try:
                NEXT_COLOR = convert_to_RJB(
                            sys.argv[sys.argv.index('-nc') + 1])
            except IndexError:
                print(
                    'You may have entered a color that starts with #. \r\nOn the command line\
,the comment that follows this character.\r\n\
Re-enter without character #')
                exit(0)
        if '-p' in sys.argv:
            PATH = sys.argv[sys.argv.index('-p') + 1]
        if '-l' in sys.argv:
            LEVEL = int(sys.argv[sys.argv.index('-l') + 1])
    logging.basicConfig(format='%(asctime)s %(message)s', level=LEVEL)
    chCollor(PATH, NEXT_COLOR)
