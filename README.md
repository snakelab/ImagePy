# ImagePy
Move your images around

Suppose you have a bunch of images in a directory tree, that you want to order in such a manner:

<target-dir>/YYYY/MM/image.jpg

The script is reading the exif-data and tries to find the creation-date of the image and move this file into the above directories.

If no exif-data is found the script tries to extract the filename in a similar way.

If the filename is allready in the target-dir the script make sure that if the file is not the same, another name is used. If it is the same image nothing happens.

## Used Bibs
 https://github.com/ianare/exif-py

## Install
pip install -r requirements.txt
or
python3 -m pip install exifread argparse

## Usage
1. Change target_dir
2. Run this command (to be ready for filenames with spaces):
IFS='
'&&set -f
for file in $(find ~/Downloads)
do
./imagepy.py -f $file
done

The target-Directory is defined in the script (currently).
