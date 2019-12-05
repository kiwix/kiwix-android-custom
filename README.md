# Kiwix Android custom apps

Kiwix Android custom apps are Android apps running [Kiwix for
Android](https://github.com/kiwix/kiwix-android) ZIM reader against a
pre-configured ZIM file.

Kiwix publishes more than [a dozen of such apps](https://play.google.com/store/apps/collection/cluster?clp=igM6ChkKEzkxMTYyMTU3Njc1NDE4NTc0OTIQCBgDEhsKFW9yZy5raXdpeC5raXdpeG1vYmlsZRABGAMYAQ%3D%3D:S:ANO1ljKl_Lw&gsr=Cj2KAzoKGQoTOTExNjIxNTc2NzU0MTg1NzQ5MhAIGAMSGwoVb3JnLmtpd2l4Lmtpd2l4bW9iaWxlEAEYAxgB:S:ANO1ljLrUVU). [Wikimed - Offline Medical Wikipedia](https://play.google.com/store/apps/details?id=org.kiwix.kiwixcustomwikimed) and [Wikivoyage - Offline Travel Guide](https://play.google.com/store/apps/details?id=org.kiwix.kiwixcustomwikivoyage) being the most famous ones.

This project contains data and scripts needed to create specific
 custom Kiwix Android apps.  _It does *not* create the app_, that's
 done separately by running the relevant Gradle command to build one
 or more custom apps.

## Prerequisites

Python 3 for the scripts in Python. On Debian based GNU/Linux you can
install it with:
```bash
apt-get install python3
```

[Imagemagick](https://imagemagick.org/) is needed by
`gen-std-icon.py`. On Debian based GNU/Linux you can
install it with:
```bash
apt-get install imagemagick
```

Android studio is required to generate icon sets and can be downloaded
from [here](https://developer.android.com/studio/?gclid=Cj0KCQiAiNnuBRD3ARIsAM8KmlvCImKxWu_AGECa8YM5pM7Nr_algyHXSkfbPRTio3WEeKTaEfFiFeIaAs81EALw_wcB).

On macOS, [Homebrew](https://brew.sh) allows to install the packages
`python3` and `imagemagick`.

## Badges

Custom apps use to have icon with two small badges to help user
understanding what the app is about:
* One reprsenting the language of the content
* One representing the stricked WiFi logo to emphasis its offline nature

The script `gen-std-icon.py` allows to add these two badges easily on
a master icon. You can use it that way:
```bash
python3 gen-std-icon.py [custom_app_directory]/icon_master.png [optional language code]
```

The `custom_app_directory` needs to be one of the listed sub-folders
e.g. `phet`. If this is a new custom app, you will have to create it.

The `optional language code` parameter for english would be `en`, if
 you omit this parameter then no language badge is added, this is
 desired in a few cases where the language is already clearly
 indicated by the master icon e.g. `wikimedde`.

## Icon set

The Android custom app needs an _Icon set_ to build properly. This
Icon set is a list of bitmap pictures which are derivatives of the
Icon master from the section above.

To create this Icon set, follow these steps:

1. Create a new empty project with Android Studio (add no activity >
next > finish)
1. In the project view (top left) there should be a dropdown that says
 `Android` select that and choose `Project`, this will make the
 project view display accurately to the file system
1. Delete `MyApplication/app/src/main/res`
1. Right click `MyApplication/app` in android studio, click `New>Image
Asset` to open Asset Studio (if this option is greyed out you will
have to wait for indexing to finish, this shouldn't take longer than 2
minutes)
1. For `foreground layer` `Source Asset > Asset Type` choose `Image`
1. For `path` click the folder icon and browse to the output of
`gen-std-icon.py`
1. For `background layer` `Source Asset > Asset Type` choose `Color`
1. Click on the color box
1. This should present the color chooser, the box in the top right
 with the label `#` should be auto selected.  Type `FFFFFF` to supply
 white as the color, this is typically the color used
1. [Optional] go back to foreground layer and size the icon as
appropriate with the slider
1. Next > Finish will generate a res folder with all the icons needed in
the location where you previously deleted the res folder.
1. Cut and paste the res folder to
`kiwix-android-custom/whatever-directory-this-icon-set-is-for`

These instructions are for a first time setup, you can reuse this
project in the future for icon generation so many steps can be
omitted.

## Version name

The custom app will have a version name displayed on the Google Play
store. This version name has to be a date in the format YYYY-MM (for
example `2018-10`. This version name should be the date of the content
(neither the date of the Software nor the release date).

The app version name is determined in that order:
1. The date can be hardcoded in the json file at the key
`version_name`. Considering that this needs maintenance and that the
publisher can easily create a discrepency with the ZIM content date,
this should probably be avoided in most of the time.
1. If nothing is specified in the json, then it tries to extract it
from the ZIM file name. If the file - specified in `zim_url` - is
`wikipedia_en_all_maxi_2018-10.zim` then it will be `2018-10`.
1. Otherwise the current date will be put (should be avoided).

## Releasing

Simply tag the repo in git with the name of a custom app eg
 `wikimed`. This triggers a Github action that will build an app using
 kiwix-android master branch and the icon set/json defined in this
 repository and then upload it to the Play Console in draft to alpha
 with an expansion file attached.

 This will only work with app updates. To create a new custom app an
 app must be built manually and submit to the Google Play store

## Building Locally

First of all the Kiwix Android needs to be cloned locally:
```bash
git clone https://github.com/kiwix/kiwix-android.git
```

Copy then a custom app directory to `kiwix-android/custom/src`.  If
using Android Studio this will add the build variant and you can
install as you would any app.

Alternatively run `./gradlew
 install[CustomAppNameWithFirstLetterCapitalised]Debug` eg `./gradlew
 installPhetDebug` from the kiwix-android folder

## Testing locally

The custom app, as built and installed by the Gradle script currently
 _does not include the ZIM file_ but it does prompt you to download
 the file if it doesn't find an `.obb` (this is the extension for ZIM
 files in custom app).  So unless you need to test obb file reading
 you can stop here.

To test reading `.obb` files you need the file to be on the device.
 Here's an overview of the steps involved. You may need to tweak these
 for your app, environment and device, etc.

Download the ZIM file to your computer e.g. for PhET download the ZIM
file specified in
https://github.com/kiwix/kiwix-android-custom/blob/master/phet/info.json
by `"zim_url":`.

Get this onto the device in the folder `/sdcard` e.g. using the
Android `adb push` command-line utility or more simply by using Device
File Exlporer in Android Studio. Copy this file to the location
expected by the app.  This is often a deeply nested folder, and with a
complex filename that's constructed based on parameters used when
creating the custom app. Here's an example of the command I used on a
locally connected device that is configured as a developer's device
(details of how to do this are beyond the scope of these notes).
```bash
adb push ~/Downloads/kiwix/phet_mul_2019-06.zim /sdcard/
adb shell
cd /sdcard/Android/obb/
mkdir org.kiwix.kiwixcustomphet
cd org.kiwix.kiwixcustomphet
cp /sdcard/phet_mul_2019-06.zim main.4.org.kiwix.kiwixcustomphet.obb
```
