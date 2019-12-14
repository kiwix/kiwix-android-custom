This files gives guidelines for developers wanting to further develop
Kiwix custom apps.

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

## Building Locally

First of all the Kiwix Android needs to be cloned locally:
```bash
git clone https://github.com/kiwix/kiwix-android.git
```

Copy then a custom app directory to `kiwix-android/custom/src`.  If
using Android Studio this will add the build variant and you can
install as you would any app.

Alternatively - if you are more export - you can run `./gradlew
 install[CustomAppNameWithFirstLetterCapitalised]Debug` eg `./gradlew
 installPhetDebug` from the kiwix-android folder

## Testing locally

The custom app, as built and installed by the Gradle script currently
 _does not include the ZIM file_ but it does prompt you to download
 the file if it doesn't find an `.obb` (this is the extension for ZIM
 files in custom app).  So unless you need to test obb file reading
 you can stop here.

To test reading an `.obb` file you need the file to be on the device.
 Here's an overview of the steps involved. You may need to tweak these
 for your app, environment and device, etc.

Download first the ZIM file to your computer e.g. for PhET download
the ZIM file specified in
https://github.com/kiwix/kiwix-android-custom/blob/master/phet/info.json
by the json key `zim_url`.

The Android obb dedicated directory is not always at the exact same
place on the Android device, usually it can be found at
`/sdcard/Android/obb/`. One time you will have found it, you will have
to create a directory for your custom app based on its Android id, for
example `org.kiwix.kiwixcustomphet` (`org.kiwix.kiwixcustom` + name of
the app directory).

You have then to get the ZIM file onto the device custom app obb
folder using the Android `adb push` command-line utility or more
simply by using Device File Exlporer in Android Studio. The obb
filename should be `main.4.` + app id + `.obb`. Here's an example:
```bash
adb push ~/Downloads/kiwix/phet_mul_2019-06.zim /sdcard/
adb shell
cd /sdcard/Android/obb/
mkdir org.kiwix.kiwixcustomphet
cd org.kiwix.kiwixcustomphet
mv /sdcard/phet_mul_2019-06.zim main.4.org.kiwix.kiwixcustomphet.obb
```
