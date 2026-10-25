# Clean TV

Clean TV is a lightweight Android TV home screen with a D-pad navigable app grid, configurable dock, mini settings panel, and Xiaomi TV integrations.

## Features

- Five configurable dock apps and a Leanback app grid.
- D-pad focus navigation with a visible focus treatment.
- Inputs menu backed by Android TV inputs.
- Wi-Fi settings shortcut and optional SSID label. Android may require location permission to read the connected SSID.
- Mini settings panel with display, accessibility, screensaver, app management, and original-launcher actions.
- Optional remote Settings key accessibility service. It filters remote key events and does not retrieve screen content.
- Material Components for Android with a Material 3 theme.

The launcher targets Android TV API 34 and newer. The app management shortcut uses Xiaomi TV Manager and is available only on compatible Xiaomi TVs. Android 14 limits third-party apps from stopping other apps directly, so this action opens the TV's own memory manager for user confirmation.

## Build

Open `launcher/` in Android Studio or build from that directory with JDK 25 and an Android SDK installed:

```sh
cd launcher
./gradlew assembleDebug
```

The debug APK is written to `launcher/app/build/outputs/apk/debug/app-debug.apk`.

## Install over ADB

The optional helper builds and installs the debug APK using the local ADB endpoint `127.0.0.1:15555` by default:

```sh
./tools/build-and-install.sh
```

Set `TV_TARGET=host:port` to use a different ADB endpoint. For a macOS host that cannot reach the TV directly, `tools/relay.py <tv-ip> <tv-port>` forwards `127.0.0.1:15555` to the TV. Wireless debugging pairing and connection ports are temporary; use the current port shown by the TV. Disable network debugging when it is no longer needed.

The install helper preserves accessibility preferences that were enabled before an app update. On first use, enable the Clean TV remote Settings key service in Android Settings → Accessibility if you want the remote Settings button to open mini settings. The helper does not enable it automatically.

## Customize

- Dock order: edit the package names in `launcher/app/src/main/res/values/config.xml`. Only installed Leanback apps are shown.
- Grid columns: edit the `columns` integer in the same file.
- Wallpaper: add an appropriately licensed image at `launcher/app/src/main/res/drawable-nodpi/home_wallpaper.jpg`. Without that optional file, the launcher uses a black background.
- Strings and colors: edit the resources under `launcher/app/src/main/res/values/` and `values-vi/`.

Outfit is distributed under the SIL Open Font License; its license is included at `launcher/app/src/main/assets/fonts/OFL.txt`.

## Attribution and license

The launcher concept was inspired by [CleanYourTV](https://github.com/Gathin23/cleanyourtv). This project is distributed under the GNU GPL v3; see `LICENSE`.
