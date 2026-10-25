#!/usr/bin/env python3
"""Verify an ADB TCP port is closed; only ECONNREFUSED counts as closed."""
import errno
import socket
import sys

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} TV_IP [PORT ...] (default: 5555)", file=sys.stderr)
    raise SystemExit(2)
host = sys.argv[1]
ports = [int(p) for p in sys.argv[2:]] or [5555]
unknown = False
for port in ports:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((host, port))
    except OSError as e:
        if e.errno == errno.ECONNREFUSED:
            print(f"{host}:{port}: connection refused (closed)")
        else:
            print(f"{host}:{port}: inconclusive: {e}", file=sys.stderr)
            unknown = True
    else:
        print(f"{host}:{port}: OPEN", file=sys.stderr)
        unknown = True
    finally:
        s.close()
raise SystemExit(2 if unknown else 0)
