<!-- OBG_DRAW: MODIFY ANYTHING THAT CHANGES cy -->

This is a Rusted moss mod designed to rip images of every room and build metadata for rendering the map, included for safekeeping. Hacked together and barely works. If you want to use this, you'll need RMML (available on my githup page). This version doesn't take images, you'll need to set `dump` to true and uncomment/recomment some stuff to get images to work.

# controller

## create

```sp
global.thebus = {}
global.thebus.surf_x = 448
global.thebus.surf_y = 252
global.thebus.screenshot = false
global.thebus.screenshot_index = 0

global.thebus.driver = {}
global.thebus.driver.index = 0
global.thebus.driver.cooldown = 0
global.thebus.driver.state = 0

global.thebus.camera = {}
global.thebus.camera.x = 0
global.thebus.camera.y = 0
global.thebus.camera.delta = []

global.thebus.stop = {}
global.thebus.stop.i = 0
global.thebus.stop.scale = 1
global.thebus.stops = undefined

global.thebus.prev = {}
global.thebus.prev.camera_scale = global.camera_scale
global.thebus.prev.game_width = global.game_width
global.thebus.prev.game_height = global.game_height

global.thebus.parallax = {}
global.thebus.parallax.layers = []
global.thebus.parallax.mod_index = 0
global.thebus.parallax.dx = []
global.thebus.parallax.dy = []

global.thebus.data = {}

global.thebus.analysis = true
global.thebus.dump = false
global.thebus.replace_parallax = false
global.thebus.quickboot = false

global.max_w = 0
global.max_h = 0

self.depth = -99999

surface_resize(application_surface_get(), global.game_width * 4, global.game_height * 4)
```

## room_start

```sp
self.depth = -99999
global.speedrun_mode_ = true
global.debug_ui_ = true
global.debug_cursor_ = true

-- start the bus
if global.thebus.quickboot {
  with omenu_new {
    global.difficulty = 1
    global.speedrun_mode_ = 1
    global.maya_mode = false
    self.state = 8
    global.current_file = 9
    -- self.menu_select = 0
    self.start_timer = 100
  }
}

instance_create_depth(0, 0, 99999, omod_instance)
-- bg renderer
instance_create_depth(0, 0, 4999, omod_instance)
instance_create_depth(0, 0, 5000, omod_instance)
instance_create_depth(0, 0, 5001, omod_instance)
```

## step_begin

```sp
if instance_number(omenu_new) != 0 {
  return
}

if global.thebus.replace_parallax {
  with obg_draw {
    instance_destroy(self)
  }
  with oparalax_handler_new {
    instance_destroy(self)
  }
}
-- kill death pits
-- with opit_generator {
--   instance_destroy(self)
-- }
-- kill enemies
with par_enemy {
  -- self.destroy_index = 10
  self.do_destroy = false
  instance_destroy(self)
}
-- kill pickups
-- with par_pickup {
--   instance_destroy(self)
-- }
-- kill munny
with omunny {
  instance_destroy(self)
}

if global.thebus.stops == undefined {
  let stop_set = {}

  global.thebus.stops = []
  -- navs
  -- global.rmml.log(json_stringify(global.map_data_))
  -- global.rmml.log(json_stringify(global.map_colors_))
  -- global.rmml.throw("aa")

  let x = 0
  while x < array_length(global.map_data_) {
    if global.map_data_[x][0] == -1 {
      x += 1
      continue
    }
    let y = 0
    while y < array_length(global.map_data_[x]) {
      let d = global.map_data_[x][y]
      let xx = d.xx
      let yy = d.yy

      let d_id = ds_grid_get(global.map_grid_, xx, yy)

      if !stop_set[d_id] {
        stop_set[d_id] = true
        array_push(global.thebus.stops, [xx, yy, d_id, room_get_name(d_id)])
      }

      y += 1
    }
    x += 1
  }
  -- global.rmml.log(global.thebus.stops)

  let actual_stops = [
    rm_test,
    rm_moss_8,
    rm_pipe_6,
    rm_seer_teleport,
    rm_catacombs_to_hell_4,
    rm_forest_branch_0_2,
  ]

  global.thebus.stops2 = []
  let i = 0
  while i < array_length(actual_stops) {
    let stop_id = actual_stops[i]
    let j = 0
    while j < array_length(global.thebus.stops) {
      let stop = global.thebus.stops[j]
      if stop[2] == stop_id {
        array_push(global.thebus.stops2, stop)
        break
      }
      j += 1
    }

    i += 1
  }
  -- global.thebus.stops = global.thebus.stops2
}

if global.thebus.driver.cooldown > 0 {
  if global.thebus.driver.state == 3 and global.thebus.driver.cooldown == 1 {
    -- replace pickups with sprites
    with par_pickup {
      let new_pickup = instance_create_depth(self.x, self.y, self.depth, omod_instance)
      new_pickup.index = self.index
      new_pickup.type = self.object_index
      new_pickup.is_pickup = true

      if self.object_index == opickup_trinket {
        new_pickup.image_index = self.index
        new_pickup.sprite_index = strinkets
      } else if self.object_index == opickup_event and room_get() == rm_snow_intro_1 {
        new_pickup.sprite_index = splayer_grenade_upgrade
      } else {
        new_pickup.sprite_index = self.sprite_index
      }

      instance_destroy()
    }
  }

  global.thebus.driver.cooldown -= 1
  return
}

match global.thebus.driver.state {
  -- tp to room
  case 0 {
    global.thebus.camera.dx = 0
    global.thebus.camera.dy = 0

    if global.thebus.stop.i >= array_length(global.thebus.stops) {
      global.rmml.log(json_stringify(global.thebus.data))
    }

    let d = global.thebus.stops[global.thebus.stop.i]
    --maxw
    -- 3944x268
    -- let d = [97,43]
    --maxh
    -- 555x1660
    -- let d = [56,63]
    -- let r = ds_grid_get(global.map_grid_, d[0], d[1])
    room_goto(d[2])
    global.input_skip_ = 10
    global.player_map_x_ = d[0]
    global.player_map_y_ = d[1]
    global.map_draw_offset_x_ = 0
    global.map_draw_offset_y_ = 0

    global.thebus.stop.i += 1
    -- screenshot
    if global.thebus.dump {
      global.thebus.driver.state = 4
    } else {
      global.thebus.driver.state = 2
    }
    -- global.rmml.log(["goto", d[2], d[3]])

    global.camera_scale = global.thebus.prev.camera_scale
    global.game_width = global.thebus.prev.game_width
    global.game_height = global.thebus.prev.game_height

    -- teleporter
    global.warp_unlock_ = d[2] != rm_pipe_6
  }
  -- adjust background
  case 1 {
    global.camera_scale = global.thebus.prev.camera_scale
    global.game_width = global.thebus.prev.game_width
    global.game_height = global.thebus.prev.game_height
    -- screenshot
    if keyboard_check_pressed('Z') {
      global.thebus.driver.state = 4
    }
    -- advance
    if keyboard_check_pressed('X') {
      global.thebus.driver.state = 0
    }
  }
  -- init room
  case 2 {
    global.thebus.driver.state = 1

    if global.thebus.analysis {
      global.thebus.driver.cooldown = 3
      global.thebus.driver.state = 5
    }

    if !global.thebus.replace_parallax {
      return
    }

    -------------------------------------
    -- init parallax
    -------------------------------------
    let sprite_index = sbg
    match global.current_biome_ {
      case 1 {
        sprite_index = sbg_blue
      }
      case 2 {
        sprite_index = sbg_blue
      }
      case 16 {
        sprite_index = sbg_elfheim
      }
      case 9 {
        sprite_index = sbg_forest_new
      }
      case 4 {
        sprite_index = sbg_stone
      }
      case 11 {
        sprite_index = sbg_pink
      }
      case 14 {
        sprite_index = sbg_labs
      }
      case 15 {
        sprite_index = sbg_editor
      }
    }

    if global.current_biome_ == 7 {
      -- chimney
      global.thebus.parallax.layers = [
        []
      ]
    } else if global.current_biome_ == 1 or global.current_biome_ == 6 {
      sprite_index = sbg_blue
      let current_time = current_time_get()
      -- mountain side (1) || rain
      global.thebus.parallax.layers = [
        [0, sprite_index, 0],
        [0, sprite_index, 1],
        [0, sprite_index, 2],
        [0, sbg_blue_mid_0, current_time // 130],
        [0, sprite_index, 3],
        [0, sbg_blue_mid_1, current_time // 130],
        [0, sprite_index, 4],
        [0, sprite_index, 5],
        [0, sbg_blue_mid_2, current_time // 130],
        [0, sprite_index, 6],
        [0, sprite_index, 7],
        [1, 1644566],
      ]
    } else if global.current_biome_ == 2 {
      -- lake

    } else if global.current_biome_ == 9 {
      -- forest

    } else if global.current_biome_ == 16 {
      -- depths
    } else if global.current_biome_ == 4 {
      -- hell

    } else if global.current_biome_ == 11 {
      -- mountain side (2)
    } else if global.current_biome_ == 15 {
      -- level editor
    } else if global.current_biome_ == 14 {
      -- lab
    } else {
      global.thebus.parallax.layers = []
    }
    global.thebus.parallax.dx = []
    global.thebus.parallax.dy = []
    let i = 0
    while i < array_length(global.thebus.parallax.layers) {
      array_push(global.thebus.parallax.dx, 0)
      array_push(global.thebus.parallax.dy, i * 250)
      i += 1
    }
  }
  -- screenshot
  case 3 {

  }
  -- screenshot start
  case 4 {
    let room_w = ceil(room_width_get() / 16) * 16
    let room_h = ceil(room_height_get() / 16) * 16

    -- scale adjustments
    let scalex = ceil(room_w / global.thebus.surf_x)
    let scaley = ceil(room_h / global.thebus.surf_y)
    global.thebus.stop.scale = max(scalex, scaley)

    -- game stuff
    global.camera_scale = global.thebus.stop.scale
    global.game_width = global.thebus.stop.scale * global.thebus.surf_x
    global.game_height = global.thebus.stop.scale * global.thebus.surf_y

    -- expand room
    room_set_width(room_get(), room_w)
    room_set_height(room_get(), room_h)
    -- surface_resize(application_surface_get(), global.game_width, global.game_height)
    -- window_set_size(global.game_width, global.game_height)
    room_goto(room_get())

    let has_chest = false
    let has_pickup = false
    let has_lore = false

    with ochest {
      has_chest = true
    }
    with par_pickup {
      -- rm_test_5
      has_pickup = true
    }
    with olore_boxes {
      has_lore = true
    }

    global.thebus.driver.state = 3
    global.thebus.driver.cooldown = 5

    with owind_flag {
      global.thebus.driver.cooldown = 20
    }
  }
  -- raw analysis
  case 5 {
    global.thebus.driver.state = 0

    -- perform analysis
    let rm = room_get()

    let addBBox = fun (data, field) {
      if data[field] == undefined {
        data[field] = []
      }
      array_push(data[field], {
        left: self.bbox_left,
        right: self.bbox_right,
        top: self.bbox_top,
        bottom: self.bbox_bottom,
      })
    }

    let addXY = fun (data, field, other) {
      if data[field] == undefined {
        data[field] = []
      }
      let added = {
        x: self.x,
        y: self.y,
      }
      array_push(data[field], added)
      return added
    }

    -- room data
    let data = {
      id: rm,
      room_width: room_width_get(),
      room_height: room_height_get(),
      biome_id: global.current_biome_,
      biome_name: global.biome_get_name(global.current_biome_),
      map_x: global.player_map_x_,
      map_y: global.player_map_y_,
      color_id: global.map_data_[room_get()][0].color
    }

    -- arenas
    with oarena_test {
      addBBox(data, "arena")
    }

    -- pits
    with opit_generator {
      addBBox(data, "pit")
    }

    -- transition
    with oroom_transition {
      addBBox(data, "transition")
    }

    -- pickups
    with par_pickup {
      let add = addXY(data, "pickup")
      add.type = object_get_name(self.object_index)
      add.index = self.index
    }

    -- guns/upgrades
    with opickup_gun { addXY(data, "gun").index = self.index }
    with ohook_upgrade_statue { addXY(data, "upgrade").type="huldur" }
    with opickup_event { addXY(data, "upgrade").type="grenade" }
    with onpc_nimue { addXY(data, "upgrade").type="nimue" }
    with oseer { addXY(data,"upgrade").type="seer" }

    -- chests
    with ochest {
      addXY(data, "chest")
    }

    -- lore
    with olore_boxes {
      addXY(data, "lore")
    }

    -- teleporter
    with oteleport_point {
      addXY(data, "warp")
    }

    -- save point
    with osave_point {
      addXY(data, "save")
    }

    -- other
    with par_shop {
      let add = addXY(data, "other")
      add.type = "shop"
      add.index = self.object_index
    }
    with oshop_blacksmith { addXY(data, "other").type="blacksmith" }
    with obell_handler {
      self.x = room_width_get() / 2
      self.y = room_height_get() / 2
      addXY(data, "other").type="bell"
    }
    with otitania_head { addXY(data, "other").type="head" }
    if room_get() == rm_tea_party {
      with par_pickup {
        self.x = room_width_get() / 2
        self.y = room_height_get() / 2
        addXY(data, "other").type = "tea"
      }
    }

    global.thebus.data[room_get_name(rm)] = data
  }
}
```

## step_end

```sp
with ocamera {
  self.clamp_pos = false
  if global.thebus.driver.state == 1 {
    if keyboard_check('W') {
      self.ypos -= 5
    }
    if keyboard_check('A') {
      self.xpos -= 5
    }
    if keyboard_check('S') {
      self.ypos += 5
    }
    if keyboard_check('D') {
      self.xpos += 5
    }
  } else {
    -- self.xpos = 0
    -- self.ypos = 0
    self.xpos = -8
    self.ypos = -8
  }
}
```

## draw_begin

```sp
with ogame {
  self.draw_catacombs_light = false
  self.black_screen = false
}
```

## draw

```sp
global.flash_ = 0
with olightning_draw {
  instance_destroy(self)
}
```

# instance

## draw

```sp
if self.is_pickup {
  if self.type == opickup_flag {
    -- draw_pickup_alt
    self.image_alpha = 1
    self.image_blend = c_gray
    draw_self()
    self.image_blend = c_white
    -- draw_pickup
    self.image_alpha = 0.9
    gpu_set_blendmode(bm_add)
    draw_self()
    gpu_set_blendmode(bm_normal)
  } else {
    -- draw_pickup
    -- opickup_tp, opickup_hp, opickup_trinket
    self.image_alpha = 0.9
    gpu_set_blendmode(bm_add)
    draw_self()
    gpu_set_blendmode(bm_normal)
  }
}

--
if self.depth == 5001 {
  with ocamera {
    self.xpos = 0
    self.ypos = 0
  }
  global.thebus.__normal_scale = global.camera_scale
  global.camera_scale = 1
} else if self.depth == 4999 {
  global.camera_scale = global.thebus.__normal_scale
}

-- replicate bg_draw
if self.depth != 5000 or !global.thebus.replace_parallax {
  return
}

-- draw layers
let i = 0
while i < array_length(global.thebus.parallax.layers) {
  let layer = global.thebus.parallax.layers[i]
  let dx = global.thebus.parallax.dx[i]
  let dy = global.thebus.parallax.dy[i]
  match layer[0] {
    case 0 {
      let rep = 0
      while rep < 8 {
        draw_sprite(layer[1], layer[2], dx + rep * 444, dy)
        rep += 1
      }
    }
    case 1 {
      -- draw_rectangle_ca(0, dy, global.game_width, global.game_height, layer[1], 1)
    }
  }
  i += 1
}
```

## draw_gui

```sp
if self.depth == 99999 {
  if global.thebus.driver.state == 3 and global.thebus.driver.cooldown <= 0 {
    if global.thebus.dump {
      global.thebus.driver.state = 0
    } else {
      global.thebus.driver.state = 1
    }

    -- let surf = surface_create(1000, 1000)
    -- let surf = surface_create(room_width_get() + 16, room_height_get() + 16)
    let surf = surface_create(room_width_get(), room_height_get())
    surface_set_target(surf)
    draw_clear_alpha(c_black, 1)

    with ogame {
      shader_replace_simple_set_hook(self.shader)
      texture_set_stage(self.lut_pointer, sprite_get_texture(global.lutmap, 0))
      let uvs_ = sprite_get_uvs(global.lutmap, 0)
      shader_set_uniform_f_array(self.uvs_pointer, [uvs_[0], uvs_[1], (uvs_[2] - uvs_[0]), (uvs_[3] - uvs_[1])])
      if (self.downsample_pointer != -1) {
        shader_set_uniform_f(self.downsample_pointer, self.downsample_rate)
      }

      -- draw_surface(application_surface_get(), 8, 8)
      draw_surface(application_surface_get(), 0, 0)

      shader_replace_simple_reset_hook()
    }

    surface_save(surf, "screenshot/" + room_get_name(room_get()) + ".png")
    -- global.rmml.log(room_get_name(room_get()))
    -- global.rmml.log(global.current_biome_)
    global.rmml.log(global.thebus.stop.i / array_length(global.thebus.stops))
    surface_reset_target()
    surface_free(surf)
  }
}
```
