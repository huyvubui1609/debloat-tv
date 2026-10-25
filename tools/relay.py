#!/usr/bin/env python3
"""Forward a local TCP port to a TV port for ADB when the host blocks LAN access.

Run from an ordinary Terminal with access to the local network:
    python3 tools/relay.py <tv-ip> [tv-port] [--listen-port PORT]

Defaults to TV port 5555 and local port 15555. For Android Wireless debugging,
pass the currently advertised pairing or connect port as tv-port. Stop this
process with Ctrl-C before starting a relay for a different TV port.
"""

from __future__ import annotations

import argparse
import socket
import threading


def relay_connection(client: socket.socket, tv_host: str, tv_port: int) -> None:
    try:
        upstream = socket.create_connection((tv_host, tv_port), timeout=10)
    except OSError as exc:
        print(f"TV connection failed: {exc}", flush=True)
        client.close()
        return

    stopped = threading.Event()

    def copy(source: socket.socket, destination: socket.socket) -> None:
        try:
            while not stopped.is_set():
                data = source.recv(65536)
                if not data:
                    break
                destination.sendall(data)
        except OSError:
            pass
        finally:
            stopped.set()
            for peer in (client, upstream):
                try:
                    peer.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass

    forward = threading.Thread(target=copy, args=(client, upstream), daemon=True)
    reverse = threading.Thread(target=copy, args=(upstream, client), daemon=True)
    forward.start()
    reverse.start()
    try:
        stopped.wait()
    finally:
        client.close()
        upstream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tv_ip", help="TV IP address")
    parser.add_argument("tv_port", nargs="?", type=int, default=5555,
                        help="TV TCP port (default: 5555)")
    parser.add_argument("--listen-port", type=int, default=15555,
                        help="Local port ADB will connect to (default: 15555)")
    args = parser.parse_args()

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", args.listen_port))
    listener.listen(8)
    print(f"Relaying 127.0.0.1:{args.listen_port} -> {args.tv_ip}:{args.tv_port}", flush=True)
    try:
        while True:
            client, _ = listener.accept()
            threading.Thread(target=relay_connection,
                             args=(client, args.tv_ip, args.tv_port),
                             daemon=True).start()
    except KeyboardInterrupt:
        pass
    finally:
        listener.close()


if __name__ == "__main__":
    main()
