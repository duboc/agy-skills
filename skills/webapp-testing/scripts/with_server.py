#!/usr/bin/env python3
"""
Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
    python scripts/with_server.py --server "npm start" --port 3000 -- python test.py

    # Multiple servers
    python scripts/with_server.py \\
      --server "cd backend && python server.py" --port 3000 \\
      --server "cd frontend && npm run dev" --port 5173 \\
      -- python test.py
"""

import subprocess
import socket
import time
import sys
import argparse
import os
import signal
import shlex


def parse_server_cmd(raw_cmd):
    """Parse server command into (argv, cwd) without invoking a shell."""
    stripped = raw_cmd.strip()
    cwd = None
    if stripped.startswith("cd ") and "&&" in stripped:
        cd_part, rest = stripped.split("&&", 1)
        tokens = shlex.split(cd_part, posix=(os.name != "nt"))
        if len(tokens) == 2 and tokens[0] == "cd":
            cwd = os.path.abspath(tokens[1])
            stripped = rest.strip()
    argv = shlex.split(stripped, posix=(os.name != "nt"))
    if not argv:
        raise ValueError(f"Empty server command: {raw_cmd!r}")
    return argv, cwd


def port_open(port):
    """TCP availability only; callers must also verify application readiness."""
    try:
        with socket.create_connection(('127.0.0.1', port), timeout=0.2):
            return True
    except OSError:
        return False


def is_server_ready(port, process, timeout=30):
    """Wait for a live launched process and a listening TCP port."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Server exited with status {process.returncode} before readiness")
        if port_open(port):
            return process.poll() is None
        time.sleep(0.1)
    return False


def stop_server(process):
    """Stop only the process tree/group started by this helper."""
    if os.name == 'nt':
        # A shell may own a Node/Python child. Do not kill by port or image name.
        if process.poll() is None:
            subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           check=False)
    else:
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=5)
        except ProcessLookupError:
            pass
        except subprocess.TimeoutExpired:
            pass
        finally:
            # The shell can exit before a stubborn child; kill the remaining group.
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def main():
    parser = argparse.ArgumentParser(description='Run command with one or more servers')
    parser.add_argument('--server', action='append', dest='servers', required=True,
                        help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True,
                        help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=30,
                        help='Timeout in seconds per server (default: 30)')
    parser.add_argument('command', nargs=argparse.REMAINDER,
                        help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    # Parse server configurations
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)
    if args.timeout <= 0 or any(not 1 <= port <= 65535 for port in args.ports):
        parser.error('Timeout must be positive and ports must be between 1 and 65535')
    if len(set(args.ports)) != len(args.ports):
        parser.error('Each server requires a distinct port')
    occupied = [port for port in args.ports if port_open(port)]
    if occupied:
        parser.error(f'Ports already in use: {occupied}; inspect/reuse existing servers separately')

    servers = []
    for cmd, port in zip(args.servers, args.ports):
        servers.append({'cmd': cmd, 'port': port})

    server_processes = []

    try:
        # Start all servers
        for i, server in enumerate(servers):
            if port_open(server['port']):
                raise RuntimeError(f"Port {server['port']} became occupied before launch")
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}")

            argv, cwd = parse_server_cmd(server['cmd'])
            process = subprocess.Popen(
                argv,
                cwd=cwd,
                shell=False,
                # Inherit streams: unread PIPEs can deadlock verbose dev servers.
                start_new_session=(os.name != 'nt'),
                creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.CREATE_NO_WINDOW)
                if os.name == 'nt' else 0,
            )
            server_processes.append(process)

            # Wait for this server to be ready
            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], process, timeout=args.timeout):
                raise RuntimeError(
                    f"Server failed to start on port {server['port']} within {args.timeout}s"
                )

            print(f"Server TCP port ready on {server['port']}; verify app readiness in the test")

        print(f"\nAll {len(servers)} server(s) ready")

        # Run the command
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all servers
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            stop_server(process)
            print(f"Server {i+1} stopped")
        print("All servers stopped")


if __name__ == '__main__':
    main()
