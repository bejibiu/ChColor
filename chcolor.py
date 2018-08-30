from PIL import Image
import logging
import sys
import os

PATH='.'
LEVEL=logging.WARNING
NEXT_COLOR=[255,255,255]


def chCollor(PATH,NEXT_COLOR):
    pngs = [ f  for f in os.listdir(PATH) if f.endswith('png')]
    logging.info('Fount %d images' %len(pngs))
    for png in pngs: 
        logging.debug('Change %s images' %png)
        img = Image.open(png)
        k,j =  img.size
        # img.show()
        for  i in range(k):
            for ii in range(j):
                if not img.getpixel((i,ii))[3] == 0:
                    alpha = img.getpixel((i,ii))[3]
                    img.putpixel((i,ii),(int(NEXT_COLOR[0]),int(NEXT_COLOR[1]),int(NEXT_COLOR[2]),alpha))
        if not os.path.exists(os.path.join(PATH,'out')):
            os.makedirs(os.path.join(PATH, 'out'))
        img.save(os.path.join(PATH, 'out',png))
        logging.info('save {}'.format(png))

if __name__ == "__main__":
    if len(sys.argv)>1:
        if '-nc' in sys.argv:
            NEXT_COLOR = sys.argv[sys.argv.index('-nc') + 1].replace('(','').replace(')','').split(',')
            if len(NEXT_COLOR)<2:
                print('color must be RJB format. For example  "(255,255,255)"')
                exit(0)
        if '-p' in sys.argv:
            PATH = sys.argv[sys.argv.index('-p') + 1]
        if '-l' in sys.argv:
            LEVEL = int(sys.argv[sys.argv.index('-l') + 1])
    logging.basicConfig(format='%(asctime)s %(message)s' , level=LEVEL)
    chCollor(PATH,NEXT_COLOR)
