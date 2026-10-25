#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
ADB=${ADB:-adb}
TV_TARGET=${TV_TARGET:-127.0.0.1:15555}
REMOTE_KEY_SERVICE=com.codex.cleantv/.RemoteSettingsAccessibilityService
ACCESSIBILITY_SERVICES=$("$ADB" -s "$TV_TARGET" shell settings get secure enabled_accessibility_services | tr -d '\r')
if [ "$ACCESSIBILITY_SERVICES" = "null" ]; then ACCESSIBILITY_SERVICES=""; fi
ACCESSIBILITY_ENABLED=$("$ADB" -s "$TV_TARGET" shell settings get secure accessibility_enabled | tr -d '\r')
if [ -z "${JAVA_HOME:-}" ] && [ -x /opt/homebrew/opt/openjdk@21/bin/java ]; then
  JAVA_HOME=/opt/homebrew/opt/openjdk@21
fi
if [ -n "${JAVA_HOME:-}" ]; then export JAVA_HOME PATH="$JAVA_HOME/bin:$PATH"; fi
cd "$ROOT/launcher"
./gradlew --no-daemon assembleDebug
APK="$ROOT/launcher/app/build/outputs/apk/debug/app-debug.apk"
"$ADB" -s "$TV_TARGET" push "$APK" /data/local/tmp/cleantv.apk
"$ADB" -s "$TV_TARGET" shell pm install -r /data/local/tmp/cleantv.apk
if [ -n "$ACCESSIBILITY_SERVICES" ]; then
  "$ADB" -s "$TV_TARGET" shell settings put secure enabled_accessibility_services "$ACCESSIBILITY_SERVICES"
  "$ADB" -s "$TV_TARGET" shell settings put secure accessibility_enabled "$ACCESSIBILITY_ENABLED"
fi
echo "Installed Clean TV. Home selection is intentionally left to the TV/user."
case ":$ACCESSIBILITY_SERVICES:" in
  *":$REMOTE_KEY_SERVICE:"*)
    if [ "$ACCESSIBILITY_ENABLED" = "1" ]; then
      echo "Restored the previously enabled Clean TV remote key service."
    else
      echo "The Clean TV remote key service remains disabled, as it was before the update."
    fi
    ;;
  *) echo "Accessibility preferences were not changed. Enable the Clean TV remote key service manually if desired." ;;
esac
