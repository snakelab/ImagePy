#!/usr/bin/env python3
import os
import sys
import exifread
import datetime
import time
import re
import argparse
import shutil
import re

parser = argparse.ArgumentParser(description='Process some images.')
parser.add_argument('-f', '--file', help='Image to work with?', required=True)

typ = ""
process = ""
result = ""
args = parser.parse_args()

# -- Here happens the magic with existing/similar pictures
from safeutil import move, copyfile

# -- should be the dir with the Date-Structure
target_dir = "/Volumes/photo/photosync"

file = args.file
#file = re.escape(args.file)

if str(os.path.basename(file)) == '.':
    sys.exit()
if str(os.path.basename(file)) == '..':
    sys.exit()
if os.path.isdir(file):
    sys.exit()
# Open image file for reading (binary mode)
#f = open(re.escape(file), 'rb')
print("===>%s" % file)
f = open(file, 'rb')

# Return Exif tags
if file.lower().endswith(('.dng')):
    tags = None
else:
    try:
        tags = exifread.process_file(
            f, stop_tag='DateTimeOriginal', details=False, strict=True)
    except ValueError:
        print("==>ExifRead (Tags) Exception!")   
# for tag in tags.keys():
#    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#        print("Key: %s, value %s" % (tag, tags[tag]))
# print(tags)

try:
    if tags is not None and tags.get('EXIF DateTimeOriginal'):
        typ = "EXIF"
        date = datetime.datetime.strptime(
            str(tags['EXIF DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")

        dir = "%s/%4d/%02d" % (target_dir, date.year, date.month)
        target = "%s/%s" % (str(dir), str(os.path.basename(file).lower()))
    elif re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*", os.path.basename(file), flags=re.I):
        typ = "NAME"
        parts = re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*",
                          os.path.basename(file), flags=re.I)

        dir = "%s/%4d/%02d" % (target_dir,
                               int(parts.group(1)), int(parts.group(2)))
    else:
        typ = "OHNE"
        parts = time.gmtime(os.path.getmtime(file))

        dir = "%s/%4d/%02d" % (target_dir,
                               int(parts.tm_year), int(parts.tm_mon))

    filename = str(os.path.basename(file).replace(" ", "-").lower())

    target = "%s/%s" % (str(dir), filename)
except NameError:
    print("==>ExifRead (NameError) Exception!")

existing = 0
do_move = 1
do_del = 0

if file and target and dir:

    try:
        os.makedirs(dir)
    except OSError:
        existing = 1
    # -- be aware of creation date
    #print('Move file =>' + shutil.move(file,target))
    # -- this function checks all and dont override existing files
    # print(target);print(file);print(os.path.isfile(target));
    if os.path.isfile(target):
        process = "- Image existing at target!"

        f_target = open(target, 'rb')
        tags_target = exifread.process_file(
            f_target, stop_tag='DateTimeOriginal', details=False, strict=True)

        # -- if ImageModel, DateTime and Size are similar, we do not copy
        if str(tags['Image Model']) == str(tags_target['Image Model']) and str(os.path.getsize(file)) == str(os.path.getsize(target)) and str(tags['EXIF DateTimeOriginal']) == str(tags_target['EXIF DateTimeOriginal']):
            process = (
                "- Similar File - no copy happens - just remove - %s" % (target))
            do_del = 1
            do_move = 0
        # -- if it is not the same image, but the same name, we change the name
        else:
            print("|%s|%s|" %
                  (tags['Image Model'], tags_target['Image Model']))
            print("|%s|%s|" % (os.path.getsize(file), os.path.getsize(target)))
            print("|%s|%s|" % (
                tags['EXIF DateTimeOriginal'], tags_target['EXIF DateTimeOriginal']))
            i = 0
            n_target = target
            while os.path.isfile(n_target):
                i += 1
                file_comp = os.path.splitext(target)
                n_target = ("%s_%s%s" % (file_comp[0], i, file_comp[1]))
            # print(n_target)
            # print(os.path.splitext(target))
            target = n_target
            process = ("- changed filename ")
            # sys.exit();

    if do_move:
        move(file, target)
        if os.path.isfile(file):
            result = "- ERR->Image is still existing!"
        else:
            result = "- OK->%s" % target
    elif do_del:
        os.remove(file)

    print("%s => %s %s %s" % (file, typ, process, result))
