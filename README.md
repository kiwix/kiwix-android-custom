# kiwix-android-custom
Overview
This project contains a python script and various folders containing information needed to create specific custom Kiwix Android apps. _It does *not* create the app_, that's done separately by running the relevant Gradle command to build one or more custom apps.

The script runs with Python 3 and uses a couple of Python packages. You may need to preinstall these before this script will run.

## Installing the prerequisites
The general approach is to use `pip install` for each pre-requisite. If your computer is running MacOS (OSX) then consider using `homebrew`. 

Pillow is a newer, and supported, edition that provides PIL functionality.

### OSX

```
brew install python3
pip3 install Pillow
```

### Some related tickets
- https://github.com/kiwix/kiwix-build/issues/79
- https://github.com/kiwix/kiwix-build/pull/81/files

## Running the script
`python3 gen-custom-android-directory.py *custom_app* --output-dir ...`
The custom_app parameter needs to be one of the listed sub-folders of this project e.g. `phet`
The `output-dir` folder needs to be in your `kiwix-android/app/src/` project folder.

for example if kiwix-android and kiwix-android-custom are peer folders of your home folder `~` then 
`python3 gen-custom-android-directory.py phet --output-dir ../kiwix-android/app/src/phet`

## Building the custom Android app  
The Android's gradle script automatically searches for and adds build targets for that project for each folder it finds that contain the relevant information needed to build a custom app. 

Again, assuming both projects are peers, after running the commands above. Connect an Android device (or create a running Android Emulator)

```
cd ../kiwix-android
./gradlew installPhetDebug
```

Note: the Android build process is currently finiky and could do with being made easier to use. See https://github.com/kiwix/kiwix-android/issues/1360 

## Using a custom app locally
The custom app, as built and installed by the gradle script currently _does not include the ZIM file_ and it does not automatically download or install it yet.

The custom app expects the content to be on the device. Here's an overview of the steps involved. You may need to tweak these for your app, environment and device, etc.

Download the ZIM file to your computer or on your device e.g. for PhET download the ZIM file specified in https://github.com/kiwix/kiwix-android-custom/blob/master/phet/info.json by `"zim_url":`. Get this onto the device in the folder `/sdcard` e.g. using the Android `adb push` command-line utility. Copy this file to the location expected by the app. This is often a deeply nested folder, and with a complex filename that's constructed based on parameters used when creating the custom app. Here's an example of the command I used on a locally connected device that is configured as a developer's device (details of how to do this are beyond the scope of these notes).

```
adb push ~/Downloads/kiwix/phet_mul_2019-06.zim /sdcard/
adb shell
cp /sdcard/phet_mul_2019-06.zim main.4.org.kiwix.kiwixcustomphet.obb
```

## Tips
You can run the script without parameters to see the parameters it expects. If it runs without import errors then your computer probably has the necessary python packages.
