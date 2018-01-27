# ImagePy
Move your images around

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
