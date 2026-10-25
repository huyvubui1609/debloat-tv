# ADB relay for macOS Local Network restrictions

If ADB cannot reach a TV on the local network but Python in an ordinary
Terminal can, start the TCP relay from the repository root:

```sh
python3 tools/relay.py <tv-ip> [tv-port]
```

The relay listens only on `127.0.0.1:15555` and forwards to the selected TV
port. The default target is port 5555. Wireless debugging uses separate,
temporary ports for pairing and connecting. For those, pass the port currently
shown by the TV, stop the relay with Ctrl-C, then restart it with the next port.

With the relay running, use `127.0.0.1:15555` as the ADB endpoint. For example,
pair through a relay targeting the TV's pairing port, then restart the relay to
target the TV's Wireless debugging connection port and run:

```sh
adb pair 127.0.0.1:15555
adb connect 127.0.0.1:15555
```

The relay does not authenticate ADB or change TV settings; keep Wireless
debugging enabled only while you are actively using it.
