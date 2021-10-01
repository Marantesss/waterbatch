from PIL import Image

WATER_MARGIN = 10

"""
cenas
"""
def get_water_mark_image(filename: str, max_size: int = 128) -> Image:
  size = (max_size, max_size)
  water_mark = Image.open(filename)
  water_mark.thumbnail(size, Image.ANTIALIAS)
  return water_mark

"""
cenas
"""
def print_image(filename: str, water_mark: Image, placement: str = 'top-left') -> Image:
  original_image = Image.open(filename)
  # make a copy as not to change the original image
  modified_image = original_image.copy()
  # third parameter indicates the mask (which the alpha channel will be used)
  paste_coords = get_paste_coordinates(modified_image.size, water_mark.size, placement)
  print(paste_coords)
  modified_image.paste(water_mark, paste_coords, water_mark)

  return modified_image

"""
cenas
"""
def get_paste_coordinates(background_size: tuple[int, int], foreground_size: tuple[int, int], placement: str = 'top-left') -> tuple[int, int]:
  bg_width, bg_height = background_size
  fg_width, fg_height = foreground_size

  size_dictionary = {
    'top-left': (0 + WATER_MARGIN, 0 + WATER_MARGIN ),
    'top-right': (bg_width - fg_width - WATER_MARGIN, 0 + WATER_MARGIN ),
    'bottom-left': (0 + WATER_MARGIN, bg_height - fg_height - WATER_MARGIN ),
    'bottom-right': (bg_width - fg_width - WATER_MARGIN, bg_height - fg_height - WATER_MARGIN ),
  }

  return size_dictionary.get(placement.lower())

def watermark(folder_path: str, image_paths: list[str], water_mark_path: str, position: str, output_folder_path: str) -> bool:
  water_mark = get_water_mark_image(water_mark_path, 128)

  for image_path in image_paths:
    full_path = '%s/%s' % (folder_path, image_path)
    print(full_path)
    image = print_image(full_path, water_mark, position)
    image.save('%s/%s' % (output_folder_path, image_path))

  return True
