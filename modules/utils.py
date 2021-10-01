import os
from zipfile import ZipFile
from io import BytesIO

def create_folder(folder_path: str) -> bool:
  # don't do anything if folder already exists
  if os.path.exists(folder_path):
    return False
    
  os.mkdir(folder_path)
  return True

def remove_folder(folder_path: str) -> bool:
  # don't do anything if folder does not exist
  if not os.path.exists(folder_path):
    return False

  for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    os.remove(file_path)
  os.rmdir(folder_path)
  return True

def zip_content_in_folder(folder_path: str) -> bool:
  # don't do anything if folder does not exist
  if not os.path.exists(folder_path):
    return False

  # zipping files
  data = BytesIO()
  with ZipFile(data, mode='w') as z:
    for file_name in os.listdir(folder_path):
      file_path = os.path.join(folder_path, file_name)
      # write(<file in directory tree>, <file in zip>)
      z.write(file_path, file_name)
  # make data start back at the beggining
  data.seek(0)

  return data
