#!/bin/bash

for f in *; do # for all files in current directory
    if [ -d ${f} ]; then # if it is a directory
        if [ -f "$f/info.json" ]; then #that has a json file
          if [ -d "kiwix-android/custom/src/$f" ]; then # and there is a matching directory in kiwix-android
            cp -v "$f/info.json" "kiwix-android/custom/src/$f/info.json" # copy it over
          fi
        fi
    fi
done
