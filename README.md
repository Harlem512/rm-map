# Slippy Map Tilenames for Rusted Moss

<a href="https://www.rustedmossgame.com/">Rusted Moss</a>'s map, rendered and sliced into <a href="https://en.wikipedia.org/wiki/Tiled_web_map">tiles</a> for your enjoyment.

Uses a <a href="https://github.com/commenthol/gdal2tiles-leaflet">fork</a> of `gdal2tiles.py` to generate the tiles.

## To Use

Simply use this endpoint to fetch tiles:

`https://raw.githubusercontent.com/Harlem512/rm-map/refs/heads/main/tiles/{z}/{x}/{y}.png`

Tile size is **_512_** pixels. The map is 74_632 by 67_632 pixels, so tiles beyond those borders will throw 404 errors (use `bounds` for leaflet). There are 9 native zoom levels, where 0 fits the entire map in one tile, and 9 is a 1:1 view. Some tiles are not actually 512x512 to save bandwidth.

```js
// build map
const map = L.map('map', {
  // IMPORTANT: prevents latlng weirdness
  crs: L.CRS.Simple,
})

// how big the 0 tile is, scaled to the tile width
const BASE_SIZE = 262_144 // (1 << 9) * 512
// widths in screen-space
const WIDTH = (74_632 / BASE_SIZE) * TILE_SIZE
const HEIGHT = (-67_632 / BASE_SIZE) * TILE_SIZE

// add tiles
L.tileLayer(
  'https://raw.githubusercontent.com/Harlem512/rm-map/refs/heads/main/tiles/{z}/{x}/{y}.png',
  {
    attribution:
      "<a href='https://www.rustedmossgame.com/' target='_blank'>Rusted Moss</a> interactive map, a <a href='/' target='_blank'>Harlem512 Production</a>",
    minZoom: 0,
    maxNativeZoom: 9,
    // these are lat-lng values for the corners of the map
    bounds: [
      [0, WIDTH],
      [HEIGHT, 0],
    ],
  }
).addTo(map)

// add a marker. y values must be first, and negative
// both points need to be divided by 256 (idk why)
// these are relative to the original image
L.marker([
   -123 / 256, // Y
   700 / 256   // X
])
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
   - gimp
   - add logo, convert solid color tiles to 1x1px
7. Build tiled web map
   - gdal2tiles-leaflet
   - `./createtiles.sh` with data/full_map.png
   - `python compressor.py` to compress to 1x1 pixel tiles
   - `optimize-images ./tiles` to optimize tiles tiles
   - Generates 9 zoom layers
