#!/bin/bash

# script that uploades all files in the FILES directory to dropbox
# requires the dropbox_uploader to be configured (run it once to setup)
# inspired by: http://www.codeproject.com/Articles/768623/Raspberry-Pi-HD-surveillance-camera-with-motion-an

FILES=/home/pi/rpi/pictures/*.jpg
UPLOADER=/home/pi/rpi/dropbox_uploader.sh

# comment out if want to show in command line instead of log file
exec &>/tmp/upload_pictures.log

echo "Looking for pictures..."
for f in $FILES
do
        if [ -f $f ];
        then
          echo "Processing picture '$f' ..."
          $UPLOADER upload $f /
          echo "Dropbox upload finished with exit code = $?"
          if [ $? -eq 0 ]
          then
             echo "Upload successful, deleting local copy."
             #rm -f $f
          else
             echo "ERROR: could not upload '$f'"
          fi
        fi
done
echo "All finished."

