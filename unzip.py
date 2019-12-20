import tarfile  # To decompress .tgz, ,tar files
import os, sys
from configparser import ConfigParser
from setup_tools import debug_log, info_error_log, file_checker
from shutil import move  # To move files over

"""
**** Python 3.2+ required ****
**** Don't change Indentation ****
**** It would be run every 5 minutes ****
**** Overwrite same named file automatically when it extracted ****
"""


# Unzip and move the log files which from file_checker()
# Work from root_path to extraced_path and stat_path

def unzip_move(file_list):

    # If not empty
    if len(file_list) != 0:

        # To count the number of files successfully processed
        global file_num

        for file in file_list:
            # Extract .trz files (landing_path -> extracted_path)
            file_path = os.path.join(root_path, file)

            tar = tarfile.open(file_path)

            try:
                tar.extractall(os.path.join(extracted_path, os.path.dirname(file)))
                debug_log.debug("%s is extracted to %s successfully!", file, extracted_paths)

            except Exception as e:
                info_error_log.exception("Failed to extract %s to %s:\n%s", file, extracted_path, e)
                info_error_log.exception("unzip.py is unsuccessfully terminated:\n")
                sys.exit(2)

            # Extract one more time for stats (landing_path -> stat_path)
            try:
                tar.extractall(os.path.join(stat_path, os.path.dirname(file)))
                debug_log.debug("%s is extracted to %s successfully!", file, stat_path)

            except Exception as e:
                info_error_log.exception( "Failed to extract %s to %s:\n%s", file, stat_path, e)
                info_error_log.exception("unzip.py is unsuccessfully terminated:\n")
                sys.exit(3)

            tar.close()

            # Move .trz files (landing_path -> archive_path)
            # shutil.move() using os.rename() and when the file system is different, does shutil.copy2() and removes sources
            try:
                move(
                    os.path.join(root_path, file),
                    os.path.join(archive_path, file),
                )
                file_num += 1
                debug_log.debug("Moving %s to %s successfully!", file, archive_path)

            except Exception as e:
                info_error_log.exception( "Failed to move %s to %s:\n%s", file, archive_path, e)
                info_error_log.exception("unzip.py is unsuccessfully terminated:\n")
                sys.exit(4)

        # end of for

        info_error_log.info("%d file(s) in %s processed succesfully!", len(file_list), root_path)

    # end of if


# end of unzip_move


def main():

    try:
        info_error_log.info("unzip.py starts...")

        config = ConfigParser()
        config.read(sys.argv[1])

        # Folder paths
        global root_path, extracted_path, stat_path, archive_path, file_num
        root_path = config["paths"]["root_path"]
        extracted_path = config["paths"]["extracted_path"]
        stat_path = config["paths"]["stat_path"]
        archive_path = config["paths"]["archive_path"]

        # removing spaces after the comman (', ') in the list of sub-folders, and split by comma
        folders = config['folders']['sub_folders']
        sub_folders = folders.replace(" ", "").split(',')

        # Number of processed files by this script
        file_num = 0

        # file_checker() returns the list of files to be processed with path (recursively check directories)
        # The list of files pass to unzip_move at root_path
        unzip_move(file_checker(root_path, sub_folders))

        info_error_log.info("unzip.py job is done successfully!")
        sys.exit(0)
        
    except Exception as e:
        info_error_log.exception("unzip.py is unsuccessfully terminated:\n%s", e)
        sys.exit(1)


# end of main

if __name__ == "__main__":
    main()
