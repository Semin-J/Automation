import os, logging
from shutil import move, make_archive, rmtree
from datetime import date, timedelta
from zipfile import ZipFile, ZIP_DEFLATED
from fnmatch import fnmatch

"""
**** This one runs once a day, to move, zip and delete old logs ****
1. This script need to create New Date Folder in Archive
2. Create dated folders, copying extracted daily logs (Don't copy over empty folders)
3. Don't move extracted folder itself - If the batch failed, there is no location for extracted files
4. Logging, .exit() return should be implemented
"""

server_list  = ["front_A", "front_B", "app_A", "app_B"]
sub_list = [["inst1", "inst2", "inst3"], ["int1", "int2", "ext1", "ext2", "ext3"]]

root_path = "#"
extracted_path = os.path.join(root_path, "extracted")
stat_path = os.path.join(root_path, "stat")
archive_temp_path = os.path.join(root_path, "archive", "temp")
archive_path = os.path.join(root_path, "archive")
access_right = 0o755


# Date folder in archive path (Archving yesterday logs)
yesterday = date.today() - timedelta(1)
yesterday_path = os.path.join(archive_path, yesterday.strftime("%d-%b-%Y"))


# Create whole folder structure (extracted -> archive /date/)
def create_folders(target_path, access_right):

  target = ''

  try:
    for server in range(0, 2, 1):
      for sub in range(0, 3, 1):
        os.makedirs(os.path.join(target_path, server_list[server], sub_list[0][sub]), access_right, exist_ok = True)
    
    for server in range(2, 4, 1):
      for sub in range(0, 5, 1):
        os.makedirs(os.path.join(target_path, server_list[server], sub_list[1][sub]), access_right, exist_ok = True)
    logging.debug('All directories are created successfully in %s', target_path)

  except Exception as e:
    logging.exception('Failed to create directory %s:\n%s', target, e)

# end of create_folders



# If the origin sub folder is not empty, move over
# If the origin sub folder is empty, delete target sub folders
def move_old_logs(origin_path, target_path):

  origin_file_path = ''
  target_file_path = ''

  try:
    for server in range(0, 2, 1):
      for sub in range(0, 3, 1):
        origin_file_path = os.path.join(origin_path, server_list[server], sub_list[0][sub])
        target_file_path = os.path.join(target_path, server_list[server], sub_list[0][sub])
        origin_file_list = os.listdir(origin_file_path)
        target_file_list = os.listdir(target_file_path)
        
        if len(origin_file_list) != 0:
          for file in origin_file_list:
            move(os.path.join(origin_path, server_list[server], sub_list[0][sub] + file), os.path.join(target_path, server_list[server], sub_list[0][sub], file))
        
        elif (len(origin_file_list) == 0 and len(target_file_list) == 0):
          os.rmdir(os.path.join(target_path, server_list[server], sub_list[0][sub]))
        
        elif (len(origin_file_list) == 0 and len(target_file_list) != 0):
          pass
    
    for server in range(2, 4, 1):
      for sub in range(0, 5, 1):
        origin_file_path = os.path.join(origin_path, server_list[server], sub_list[1][sub])
        target_file_path = os.path.join(target_path, server_list[server], sub_list[1][sub])
        origin_file_list = os.listdir(origin_file_path)
        target_file_list = os.listdir(target_file_path)
        
        if len(origin_file_list) != 0:
          for file in origin_file_list:
            move(os.path.join(origin_path, server_list[server], sub_list[1][sub], file), os.path.join(target_path, server_list[server], sub_list[1][sub], file))
        
        elif (len(origin_file_list) == 0 and len(target_file_list) == 0):
          os.rmdir(os.path.join(target_path, server_list[server], sub_list[1][sub]))
        
        elif (len(origin_file_list) == 0 and len(target_file_list) != 0):
          pass
      logging.debug('All old logs are moved succesfully!')
    
  except Exception as e:
    logging.exception('Failed to move old log from %s to %s:\n%s', origin_file_path, target_file_path, e)



# Clean up (delete) 'files only' recursively in targeted path
def clean_up_folders(target_path):

  try:
    if target_path == archive_temp_path:  # Get rid of only 2-day-old .trz files
      old_2days = date.today() - timedelta(2)
      old_2days_pattern = old_2days.strftime("*-%Y%m%d.*")
      for folder in os.walk(target_path):  # sets of tuples (o: folder, 1: [subfolders], 2: [files])
        for file in folder[2]:
          if fnmatch(file, old_2days_pattern):
            os.remove(os.path.join(folder[0], file))

    else:  # Get rid of contents in any folder and its subfolders
      for folder in os.walk(target_path):
        for file in folder[2]:
          os.remove(os.path.join(folder[0], file))
    logging.debug('All folders are cleaned up successfully!')

  except Exception as e:
    logging.exception('Failed to clean up folder:\n%s', e)

# end of clean_up_folders



# Zip (3)-day-old log folder
def zip_Ndays_old_logs(N = 3):

  old_Ndays = date.today() - timedelta(N)
  old_Ndays_str = old_Ndays.strftime("%d-%b-%Y")
  old_Ndays_path = os.path.join(archive_path, old_Ndays_str)

  try:
    if os.path.exists(old_Ndays_path):
      make_archive(old_Ndays_path, 'zip', old_Ndays_path)

      if os.path.exists(old_Ndays_path + '.zip'):
        rmtree(old_Ndays_path)
    logging.debug('Zipped %s folder successfully!', old_Ndays_str)

  except Exception as e:
    logging.exception('Failed to zip %s:\n%s', old_Ndays_str, e)
# end of zip_Ndays_old_logs



# Delete One old logs (By date, 95-day-old)
# File creation time check is posible for Windows, but *nix
def delete_oldest_log(N = 95):

  # Based on Date on folder name
  old_Ndays = date.today() - timedelta(N)
  old_Ndays_str = old_Ndays.strftime("%d-%b-%Y.zip")
  old_Ndays_path = os.path.join(archive_path, old_Ndays_str)

  try:
    if os.path.exists(old_Ndays_path):
      os.remove(old_Ndays_path)
      logging.debug('Deleted %s log successfully', old_Ndays_str)

  except Exception as e:
    logging.exception('Failed to delete %s log:\n%s', old_Ndays_str, e)

# end of delete_oldest_log



def main():

  # Create log file (Once created, append)
  batch_log_path = '#'
  today_pattern = date.today().strftime("%Y%m%d")
  today_log_path = os.path.join(batch_log_path, (today_pattern + '_Debug_Error.log'))

  logging.basicConfig(level = logging.DEBUG,
                      filename = today_log_path,
                      format = '%(asctime)s.%(msecs)03d|%(levelname)s|%(module)s|%(message)s',
                      datefmt = '%Y-%m-%d@%H:%M:%S')

  try:
    # Check yesterday folder already exist or not, and create
    if not os.path.exists(yesterday_path):
      os.mkdir(yesterday_path, access_right)

    create_folders(yesterday_path, access_right)

    move_old_logs(extracted_path, yesterday_path)

    clean_up_folders(stat_path)
    clean_up_folders(archive_temp_path)
    zip_Ndays_old_logs(3)
    delete_oldest_log(95)
    logging.debug('old_log_manager.py job is done successfully!')

  except Exception as e:
    logging.exception('old_log_manager.py unsuccessfully terminated:\n%s', e)

# end of main


if __name__=="__main__":
  main()