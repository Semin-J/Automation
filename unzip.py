import tarfile  # To decompress .tgz, ,tar files
import os  # To check directories
from shutil import move  # To move files over

"""
**** Don't change Indentation ****
**** It would be run every minute ****
1. Overwrite same name file automatically when it extracted
"""


server_list  = ["front_A", "front_B", "app_A", "app_B"]
sub_list = [["inst1", "inst2", "inst3"], ["int1", "int2", "ext1", "ext2", "ext3"]]

root_path = "#"
extracted_path = os.path.join(root_path, "extracted")
stat_path = os.path.join(root_path, "stat")
archive_temp_path = os.path.join(root_path, "archive", "temp")


def change_folder(server, sub, is_mobile):
  
  landing_path = os.path.join(root_path, "landing") if is_mobile == False else os.path.join(root_path, "landing", "mobile")
  paths = {}
  paths['landing_path'] = os.path.join(landing_path, server, sub)
  paths['extratced_path'] = os.path.join(landing_path, server, sub)
  paths['stat_path'] = os.path.join(stat_path, server, sub)
  paths['archive_temp_path'] = os.path.join(archive_temp_path, server, sub)
  return paths


def unzip_move(paths):

  file_list = os.listdir(paths['landing_path'])  # Fix the number of task (To prevent redundant job)

  if len(file_list) != 0:
    
    # Need to sort the list oldest - newest since logs are overwritten
    file_list.sort()

    for file in file_list:
      # Extract .trz files (landing_path -> extracted_path)
      file_path = os.path.join(paths['landing_path'] + file)
      tar = tarfile.open(file_path)
      tar.extractall(paths['extracted_path'])
      # Extract one more time for stats (landing_path -> stat_path)
      tar.extractall(paths['stat_path'])
      tar.close()

      # Move .trz files (landing_path -> archive_path)
      # shutil.move() using os.rename() and when the file system is different, does shutil.copy2() and removes sources
      move(os.path.join(paths['landing_path'], file), os.path.join(paths['archive_temp_path'], file))
    
    # end of for

  # end of if

# end of unzip_move



def main():

  for is_mobile in range(0, 2, 1):

    for server in range(0, 2, 1):
      for sub in range(0, 3, 1):
        unzip_move(change_folder(server_list[server], sub_list[0][sub], is_mobile))

    for server in range(2, 4, 1):
      if is_mobile == False:
        for sub in range(0, 5, 1):
          unzip_move(change_folder(server_list[server], sub_list[1][sub], is_mobile))
      else:
        for sub in range(2, 5, 1):
          unzip_move(change_folder(server_list[server], sub_list[1][sub], is_mobile))

  # end of for

# end of main

if __name__=="__main__":
  main()
