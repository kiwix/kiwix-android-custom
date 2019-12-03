#!/usr/bin/env bash
!/bin/bash

for f in *; do # for all files in current directory
    if [ -d ${f} ]; then # if it is a directory
        if [ -f "$f/info.json" ] && [ -d "$f/res" ]; then #that has a json file and icon set
            mkdir -p "kiwix-android/custom/src/$f/res" #make directory
            cp -v "$f/info.json" "kiwix-android/custom/src/$f/info.json" # copy json over
            cp -vr "$f/res" "kiwix-android/custom/src/$f/res" #copy icons over
        fi
    fi
done
