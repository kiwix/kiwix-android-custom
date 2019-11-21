# kiwix-android-custom
Overview
This project contains a python script and various folders containing information needed to create specific custom Kiwix Android apps.
 _It does *not* create the app_, that's done separately by running the relevant Gradle command to build one or more custom apps.

The script runs with Python 3. It also requires imagemagick be installed.

## Installing the prerequisites
Android studio is required to generate icon sets and can be downloaded from [here](https://developer.android.com/studio/?gclid=Cj0KCQiAiNnuBRD3ARIsAM8KmlvCImKxWu_AGECa8YM5pM7Nr_algyHXSkfbPRTio3WEeKTaEfFiFeIaAs81EALw_wcB)

The general approach is to use `apt-get install` for the dependencies, Linux or Linux Subsystem recommended.
 If your computer is running MacOS (OSX) then consider using `homebrew`. 

```
apt-get install python3
apt-get install imagemagick
```

### OSX

```
brew install python3
brew install imagemagick
```

## Running the script
The script adds "badges" to a master icon, these badges are "offline" and "language"

`python3 gen-std-icon.py [custom_app_directory]/icon_master.png [optional language code]`

The `custom_app_directory` needs to be one of the listed sub-folders of this project e.g. `phet`

The `optional language code` parameter for english would be `en`,
 if you omit this parameter then no language badge is added, 
 this is desired in a few cases where the language is already clearly indicated by the master icon eg `wikimedde`

## Generating an icon set
1. Create a new empty project with Android Studio (add no activity>next>finish)
1. In the project view (top left) there should be a dropdown that says `Android`
 select that and choose `Project`, this will make the project view display accurately to the file system
1. Delete `MyApplication/app/src/main/res`
1. Right click `MyApplication/app` in android studio, click `New>Image Asset` 
to open Asset Studio (if this option is greyed out you will have to wait for indexing to finish, this shouldn't take longer than 2 minutes)
1. For `foreground layer` `Source Asset>Asset Type` choose `Image`
1. For `path` click the folder icon and browse to the output of `gen-std-icon.py`
1. For `background layer` `Source Asset>Asset Type` choose `Color`
1. Click on the color box
1. This should present the color chooser, the box in the top right with the label `#` should be auto selected.
 Type `FFFFFF` to supply white as the color, this is typically the color used
1. [Optional] go back to foreground layer and size the icon as appropriate with the slider
1. Next>Finish will generate a res folder with all the icons needed in the location where you previously deleted the res folder.
1. Cut and paste the res folder to `kiwix-android-custom/whatever-directory-this-icon-set-is-for`

These instructions are for a first time setup, you can reuse this project 
in the future for icon generation so many steps can be omitted.

## Building the custom Android app  
Copy a custom app directory to `kiwix-android/custom/src`. 
If using Android Studio this will add the build variant and you can install as you would any app.

Alternatively run `./gradlew install[CustomAppNameWithFirstLetterCapitalised]Debug`
 eg `./gradlew installPhetDebug` from the kiwix-android folder

## Using a custom app locally
The custom app, as built and installed by the gradle script currently _does not
 include the ZIM file_ but it does prompt you to download the file if it doesn't find an `.obb`.
  So unless you need to test obb file reading you can stop here.

To test reading obb files you need the content to be on the device.
 Here's an overview of the steps involved. You may need to tweak these for your app, environment and device, etc.

Download the ZIM file to your computer or on your device e.g. for PhET download 
the ZIM file specified in https://github.com/kiwix/kiwix-android-custom/blob/master/phet/info.json by `"zim_url":`.
 Get this onto the device in the folder `/sdcard` e.g. using the Android `adb push` command-line utility or more
  simply by using Device File Exlporer in Android Studio. Copy this file to the location expected by the app. 
  This is often a deeply nested folder, and with a complex filename that's constructed based on parameters
   used when creating the custom app. Here's an example of the command I used on a locally connected device
    that is configured as a developer's device (details of how to do this are beyond the scope of these notes).

```
adb push ~/Downloads/kiwix/phet_mul_2019-06.zim /sdcard/
adb shell
cd /sdcard/Android/obb/                                                                                                                                        
mkdir org.kiwix.kiwixcustomphet
cd  org.kiwix.kiwixcustomphet
cp /sdcard/phet_mul_2019-06.zim main.4.org.kiwix.kiwixcustomphet.obb
```

## Releasing an App
Simply tag the repo in git with the name of a custom app eg `wikimed`.
 This triggers a github action that will build an app using kiwix-android master branch
 and the icon set/json defined in this repository and then upload it to the Play Console in draft to alpha with an expansion file attached.
 
 This will only work with app updates. To create a new custom app an app must be built manually and submitted to the play store
