import os
from tqdm import tqdm
from PIL import Image

for zoom in os.listdir('./tiles'):
    if os.path.isdir(f'./tiles/{zoom}/'):
        for x in tqdm(os.listdir(f'./tiles/{zoom}/')):
            for y in os.listdir(f'./tiles/{zoom}/{x}'):
                with Image.open(f'./tiles/{zoom}/{x}/{y}') as tile:
                    tl = tile.getpixel((0,0))
                    good = True
                    for ix in range(0, tile.width, 8):
                        for iy in range(0, tile.height, 8):
                            if tile.getpixel((ix, iy)) != tl:
                                good = False
                                break
                        if not good:
                            break

                    if good:
                        # make smaller
                        newer = Image.new('RGBA', (1,1), color=tl)
                        newer.save(f'./tiles/{zoom}/{x}/{y}')