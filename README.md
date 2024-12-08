# Slippy Map Tilenames for Rusted Moss

<a href="https://www.rustedmossgame.com/">Rusted Moss</a>'s map, rendered and sliced into <a href="https://en.wikipedia.org/wiki/Tiled_web_map">tiles</a> for your enjoyment.

Uses a <a href="https://github.com/commenthol/gdal2tiles-leaflet">fork</a> of `gdal2tiles.py` to generate the tiles.

## To Use

Simply use this endpoint to fetch tiles:

`https://raw.githubusercontent.com/Harlem512/rm-map/refs/heads/main/tiles/{z}/{x}/{y}.png`

Tile size is 256 pixels. The map is 45,840 by 27,600 pixels, so tiles beyond those borders will throw 404 errors (use `bounds` for leaflet). There are 8 native zoom levels, where 0 fits the entire map in one tile, and 8 is a 1:1 view.

```js
// Leaflet example
L.tileLayer(
  'https://raw.githubusercontent.com/Harlem512/rm-map/refs/heads/main/tiles/{z}/{x}/{y}.png',
  {
    attribution:
      "<a href='https://www.rustedmossgame.com/' target='_blank'>Rusted Moss</a> interactive map, a <a href='/' target='_blank'>Harlem512 Production</a>",
    minZoom: 0,
    maxNativeZoom: 8,
    // these are lat-lng values for the corners of the map
    bounds: [
      [85.0511287798066, 71.80664062500001],
      [27.293689224852407, -180],
    ],
  }
).addTo(map)
```

Alternatively, just go <a href="https://harlem512.github.io/rm-map.html">here</a> and see it in action or copy my source code.

## To Build

You'll need python, gdal, and a Linux distribution to build. The linux is optional, you could run the python directly.

Download `gdal2tiles.py` from <a href="https://github.com/commenthol/gdal2tiles-leaflet">here</a> and place it in the root directory, then run `./createtiles.sh`.

Modifying `full_map.png` will change the resulting tiles. If you modify the size of the map, your bounds will change.

## How we got here

1. Get a dump of all rooms
   - The Bus, RMML mod
   - Early processing (remove objects, add more rendering, etc)
2. Build rooms into delta json
   - custom python script
   - Aligns rooms to grid, fast placement
3. Render room json into massive .png
   - custom python script
4. Add post-processing
   - paint.net
   - Massive (45k by 27k) file
   - Room connections, background colors
5. Export to png
   - paint.net
   - Layers flattened, ready for final processing
6. Post-post processing
   - paint.net
   - Add 256px border, remove background
7. Build tiled web map
   - gdal2tiles-leaflet
   - ./createtiles.sh with data/big_map.png
   - Generates 8 zoom layers
