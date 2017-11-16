#!/bin/python
import os
import sys
import exifread
import datetime
import re

#try:
from safeutil import move, copyfile
#except ImportError:
#    from shutil import move, copyfile

target_dir="/volume1/photo/photosync"
file=sys.argv[1]

if str(os.path.basename(file)) == '.': 
    sys.exit() 
if str(os.path.basename(file)) == '..': 
    sys.exit()
if os.path.isdir(file):
    sys.exit()
# Open image file for reading (binary mode)
f = open(file, 'rb')
#print os.path.basename(file)
# Return Exif tags
tags = exifread.process_file(f)
try:
    if tags.get('EXIF DateTimeOriginal'):
        #for tag in tags.keys():
        #    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
        #        print "Key: %s, value %s" % (tag, tags[tag])
        print "EXIF"
        date=datetime.datetime.strptime(str(tags['EXIF DateTimeOriginal']), "%Y:%m:%d %H:%M:%S")
        dir="%s/%4d/%02d" % (target_dir, date.year, date.month)
        target="%s/%s" % (str(dir), str(os.path.basename(file).lower()))
    elif re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*", os.path.basename(file), flags=re.I):
        print "NAME"
        parts=re.search(r"IMG_(\d{4})(\d{2})(\d{2}).*", os.path.basename(file), flags=re.I)
        dir="%s/%4d/%02d" % (target_dir, int(parts.group(1)), int(parts.group(2)))
    else:
        print "OHNE"
        dir="%s/0000/00" % (target_dir, int(parts.group(1)), int(parts.group(2)))
        #try:
        #    os.makedirs(dir)
        #except OSError:
        #    pass
    #print file
    target="%s/%s" % (str(dir), str(os.path.basename(file).lower()))
except NameError:
    created=0

created=0
if file and target and dir:
    #print target
    try:
        os.makedirs(dir)
    except OSError:
        created=1
    print 'Move file =>' + move(file,target) 
    #move(file,target)
    if os.path.isfile(file):
        print "Datei ist immernoch vorhanden!"
        exit

