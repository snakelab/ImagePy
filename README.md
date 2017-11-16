# ImagePy
Move your images around

Suppose you have a bunch of images in a directory tree, that you want to order in such a manner:

<target-dir>/YYYY/MM/image.jpg

The script is reading the exif-data and tries to find the creation-date of the image and move this file into the above directories.

If no exif-data is found the script tries to extract the filename in a similar way.

## Example ##
./imagepy.py <image>
  
The target-Directory is defined in the script (currently).
