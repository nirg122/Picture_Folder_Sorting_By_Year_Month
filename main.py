import os
import exiftool

def move_to_dir(date_to_use):
    global files_moved
    try:
        year = date_to_use[0]
        month = date_to_use[1]
        transfer_to_folder = f"{year}/{month}"
        new_path = f'{transfer_to_folder}/{file_name}'
        os.rename(file_name, new_path)
        files_moved += 1
    except FileNotFoundError:
        os.makedirs(transfer_to_folder)
        move_to_dir(date)
        files_moved += 1
    except FileExistsError:
        print(f'This file already exists: {file_name} in {new_path}')
    except Exception as err:
        print(f'The following exception happened for file {file_name}: {err}')
        print(file_data)


# ######### Change Folder Name in Pictures Folder V ####################
folder_name = input('Please enter The folder name: ')
######################################################################


directory = f'%UserProfile%\\Pictures\\{folder_name}'
os.chdir(directory)
files_moved = 0
with exiftool.ExifTool() as et:
    metadata_batch = et.get_metadata_batch('.')

    for file_data in metadata_batch:
        file_name = file_data['File:FileName']
        # For JPG ext:
        ext = file_data['File:FileTypeExtension']
        if ext == 'JPG':
            date = file_data['EXIF:CreateDate'].split(' ')[0].split(':') if 'EXIF:CreateDate' in file_data \
                else file_data['File:FileModifyDate'].split(' ')[0].split(':')
            move_to_dir(date)

        elif ext == 'MOV' or ext == 'MP4':
            date = file_data['QuickTime:CreateDate'].split(' ')[0].split(':')
            move_to_dir(date)

print(f'\nNumber of files moved: {files_moved}')
