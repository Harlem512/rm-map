#!/bin/bash

rm -rf ./tiles
export GDAL_ALLOW_LARGE_LIBJPEG_MEM_ALLOC=1
python3 ./gdal2tiles.py -l -p raster -w none ./full_map.png ./tiles
