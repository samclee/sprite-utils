import os

from pathlib import Path
from datetime import datetime
from PIL import Image

########## Utils
def _get_time_string():
  now = datetime.now() 
  mo = now.month
  day = now.day
  hour = now.hour
  min = now.min
  sec = now.second

  return f"{mo:02}{day:02}{hour:02}{min:02}{sec:02}"

########## Split
def split_image_into_tiles(image_name, tile_dimension):
    dest_folder_name = f"split_result_{_get_time_string()}"
    os.mkdir(dest_folder_name)
    dest_folder_path = Path(dest_folder_name)

    with Image.open(image_name) as im:
        width, height = im.size
        width, height = int(width), int(height)

        if (width % tile_dimension != 0) or (height % tile_dimension != 0):
            raise Exception("Source image cannot be split cleanly into tiles")

        num_h_tiles = width // tile_dimension
        num_v_tiles = height // tile_dimension

        print(f"{image_name} is {num_h_tiles} tiles wide")
        print(f"{image_name} is {num_v_tiles} tiles tall")

        for row in range(num_v_tiles):
            for col in range(num_h_tiles):
                left = col * tile_dimension
                upper = row * tile_dimension
                right = left + tile_dimension
                lower = upper + tile_dimension

                new_tile = im.crop((left, upper, right, lower))
                new_filename = f"{row * num_h_tiles + col}.png"
                new_filepath = dest_folder_path / new_filename
                new_tile.save(new_filepath)
                



########## Fuse
def fuse_images_into_one(source_folder):
    total_width = 0
    height = -1
    for root, _, files in os.walk(source_folder, topdown=False):
        for name in files:
            cur_path = Path(os.path.join(root, name))
            if cur_path.suffix == ".png":
                with Image.open(cur_path) as im:
                    total_width += im.width
                    height = max(height, im.height)

    fused = Image.new("RGBA", (total_width, height))
    x_to_paste_at = 0
    for root, _, files in os.walk(source_folder, topdown=False):
        for name in files:
            cur_path = Path(os.path.join(root, name))
            if cur_path.suffix == ".png":
                with Image.open(cur_path) as im:
                    fused.paste(im, (x_to_paste_at, 0))
                    x_to_paste_at += im.width
    
    filename = f"fuse_result_{_get_time_string()}.png"
    fused.save(filename)