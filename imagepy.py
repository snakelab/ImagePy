#!/usr/bin/env python3
import os
import sys
import exifread
import datetime
import time
import re
import argparse
import shutil

parser = argparse.ArgumentParser(description='Process some images.')
parser.add_argument('-f','--file', help='Image to work with?', required=True)

args = parser.parse_args()
#print(args)

#-- Here happens the magic with existing/similar pictures
from safeutil import move, copyfile

#-- should be the dir with the Date-Structure
target_dir="/Volumes/photo/photosync"

file=args.file

if str(os.path.basename(file)) == '.':
    sys.exit()
if str(os.path.basename(file)) == '..':
    sys.exit()
if os.path.isdir(file):
    sys.exit()
# Open image file for reading (binary mode)
f = open(file, 'rb')

# Return Exif tags
if file.lower().endswith(('.dng')):
    tags = None
else:
    tags = exifread.process_file(f,stop_tag='DateTimeOriginal',details=False,strict=True)
#for tag in tags.keys():
#    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#        print("Key: %s, value %s" % (tag, tags[tag]))
#print(tags)

try:
    if tags is not None and tags.get('EXIF DateTimeOriginal'):
        print("EXIF")
        date=datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")

        dir="%s/%4d/%02d" % (target_dir, date.year, date.month)
        target="%s/%s" % (str(dir), str(os.path.basename(file).lower()))
    elif re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*", os.path.basename(file), flags=re.I):
        print("NAME")
        parts=re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*", os.path.basename(file), flags=re.I)

        dir="%s/%4d/%02d" % (target_dir, int(parts.group(1)), int(parts.group(2)))
    else:
        print("OHNE")
        parts=time.gmtime(os.path.getmtime(file))

        dir="%s/%4d/%02d" % (target_dir, int(parts.tm_year), int(parts.tm_mon))

    target="%s/%s" % (str(dir), str(os.path.basename(file).replace(" ", "-").lower()))
except NameError:
    print("==>ExifRead Exception!")

existing=0
if file and target and dir:
    try:
        os.makedirs(dir)
    except OSError:
        existing=1
    #-- be aware of creation date
    #print('Move file =>' + shutil.move(file,target))
    #-- this function checks all and dont override existing files
    move(file,target)
    if os.path.isfile(file):
        print("Image is still existing!")
        exit
