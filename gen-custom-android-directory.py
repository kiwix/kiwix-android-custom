#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

""" Generate a custom build of Kiwix for Android working with a single content

    The generated App either embed the ZIM file inside (creating large APKs)
    or is prepared to make use of a Play Store companion file.

    APKs uploaded to Play Store are limited to 50MB in size and can have
    up to 2 companion files of 2GB each.
    Note: multiple companion files is not supported currently
        ~~ needs update to the libzim.
    The companion file is stored (by the Play Store) on the SD card.

    Large APKs can be distributed outside the Play Store.
    Note that the larger the APK, the longer it takes to install.
    Also, APKs are downloaded then extracted to the *internal* storage
    of the device unless the user specifically change its settings to
    install to SD card.

    Standard usage is to launch the script with a single JSON file as argument.
    Take a look at JSDATA sample in this script's source code for
    required and optional values to include. """

import argparse
import os, shutil
from PIL import Image

pj = os.path.join

SIZE_MATRIX = {
    'xxxhdpi': 192,
    'xxhdpi': 144,
    'xhdpi': 96,
    'mdpi': 72,
    'hdpi': 72,
}

def generate_icons(source_icon, dest_dir):
    with Image.open(source_icon) as icon:
        for res, pixel in SIZE_MATRIX.items():
            resized_icon = icon.resize((pixel, pixel))
            for type_ in ('drawable', 'mipmap'):
                dir_name = "{}-{}".format(type_, res)
                os.makedirs(pj(dest_dir, dir_name))
                file_name = 'ic_kiwix_widget.png' if type_ == 'drawable' else 'kiwix_icon.png'
                resized_icon.save(pj(dest_dir, dir_name, file_name))

        icon_title = icon.resize((256, 256))
        os.makedirs(pj(dest_dir, 'drawable'))
        icon_title.save(pj(dest_dir, 'drawable', 'kiwix_icon_with_title.png'))

_manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
  xmlns:tools="http://schemas.android.com/tools">
<uses-permission android:name="android.permission.INTERNET" tools:node="remove"/>
</manifest>"""

def generate_manifest(dest_dir):
    with open(pj(dest_dir, 'AndroidManifest.xml'), mode='w') as f:
        f.write(_manifest_content)


def parse_args():
    parser = argparse.ArgumentParser(description="""
This script take a android custom app information directory and generate
a directory suitable for gradle to build a custom app.""")
    parser.add_argument('custom_app',
                        help="The custom app to work on")
    parser.add_argument('--output-dir',
                        help="Where to create the generated custom app information.")
    return parser.parse_args()


if __name__ == "__main__":
    options = parse_args()
    options.output_dir = os.path.abspath(options.output_dir)
    
    os.makedirs(options.output_dir)
    generate_icons(pj(options.custom_app, "icon.png"), pj(options.output_dir, 'res'))
    generate_manifest(options.output_dir)
    shutil.copy(pj(options.custom_app, 'info.json'), pj(options.output_dir, 'info.json'))

