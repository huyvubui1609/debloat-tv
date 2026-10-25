package com.codex.cleantv;

import android.accessibilityservice.AccessibilityService;
import android.accessibilityservice.AccessibilityServiceInfo;
import android.content.Intent;
import android.view.KeyEvent;
import android.view.accessibility.AccessibilityEvent;

/** Filters the Xiaomi remote's global Settings/App Switch key and routes it to Clean TV. */
public final class RemoteSettingsAccessibilityService extends AccessibilityService {
    @Override public void onAccessibilityEvent(AccessibilityEvent event) { }

    @Override public void onInterrupt() { }

    @Override protected void onServiceConnected() {
        super.onServiceConnected();
        AccessibilityServiceInfo info = getServiceInfo();
        if (info != null) {
            info.flags |= AccessibilityServiceInfo.FLAG_REQUEST_FILTER_KEY_EVENTS;
            setServiceInfo(info);
        }
    }

    @Override protected boolean onKeyEvent(KeyEvent event) {
        int code = event.getKeyCode();
        // Xiaomi's physical gear key is mapped as KEYCODE_MENU on this TV.
        // Keep the Android Settings and App Switch variants for other remotes.
        boolean settingsKey = code == KeyEvent.KEYCODE_MENU
                || code == KeyEvent.KEYCODE_APP_SWITCH
                || code == KeyEvent.KEYCODE_SETTINGS;
        if (!settingsKey) return false;
        if (event.getAction() == KeyEvent.ACTION_DOWN && event.getRepeatCount() == 0) {
            Intent open = new Intent(this, MainActivity.class);
            open.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP
                    | Intent.FLAG_ACTIVITY_SINGLE_TOP);
            open.putExtra(MainActivity.EXTRA_OPEN_MINI_SETTINGS, true);
            startActivity(open);
        }
        return true;
    }
}
