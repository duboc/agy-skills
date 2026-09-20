"""Bounded, local-only subprocess regressions; no Playwright dependency.

Run: python -m unittest discover -s skills/webapp-testing/tests -v
Fixture servers have an independent lifetime watchdog, including when their
stdout blocks. Cleanup signals only files in this test's temporary directory.
"""
import os
from pathlib import Path
import shlex
import socket
import subprocess
import sys
import tempfile
import time
import unittest


HELPER = Path(__file__).resolve().parents[1] / "scripts" / "with_server.py"
SERVER = r'''
import http.server, os, pathlib, sys, threading, time
port, stop_name, done_name, started_name, mode = sys.argv[1:]
stop, done = pathlib.Path(stop_name), pathlib.Path(done_name)
def watchdog():
    deadline = time.monotonic() + 6
    while time.monotonic() < deadline and not stop.exists():
        time.sleep(.02)
    done.write_text("stopped", encoding="utf-8")
    os._exit(0)
threading.Thread(target=watchdog, daemon=True).start()
pathlib.Path(started_name).write_text("started", encoding="utf-8")
if mode == "verbose":
    sys.stdout.write("x" * (1024 * 1024))
    sys.stdout.flush()
if mode == "never":
    time.sleep(10)
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"owned-fixture")
    def log_message(self, *args):
        pass
with http.server.HTTPServer(("127.0.0.1", int(port)), Handler) as server:
    server.serve_forever(poll_interval=.05)
'''


def shell_command(args):
    return subprocess.list2cmdline(args) if os.name == "nt" else shlex.join(args)


class WithServerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="with-server-tests-")
        self.root = Path(self.temp.name)
        self.fixture = self.root / "fixture_server.py"
        self.fixture.write_text(SERVER, encoding="utf-8")
        self.marker = self.root / "dependent-ran"
        self.fixtures = []

    def tearDown(self):
        # Signal only owned fixtures. Their daemon watchdog exits even if a
        # verbose fixture is blocked in stdout and the helper killed its shell.
        for stop, done, started, launched_at in self.fixtures:
            stop.touch()
        for stop, done, started, launched_at in self.fixtures:
            if started.exists():
                deadline = launched_at + 7
                while not done.exists() and time.monotonic() < deadline:
                    time.sleep(.02)
        self.temp.cleanup()

    def free_port(self):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            return sock.getsockname()[1]

    def server_command(self, port, mode="normal"):
        index = len(self.fixtures)
        stop = self.root / f"stop-{index}"
        done = self.root / f"done-{index}"
        started = self.root / f"started-{index}"
        self.fixtures.append((stop, done, started, time.monotonic()))
        return shell_command([sys.executable, str(self.fixture), str(port),
                              str(stop), str(done), str(started), mode])

    def dependent(self, port=None, exit_code=0):
        code = "from pathlib import Path; import sys; "
        if port is not None:
            code += ("import urllib.request; "
                     f"assert urllib.request.urlopen('http://127.0.0.1:{port}', timeout=2).read() == b'owned-fixture'; ")
        code += f"Path({str(self.marker)!r}).write_text('ran'); sys.exit({exit_code})"
        return [sys.executable, "-c", code]

    def run_helper(self, servers, command=None, timeout=1):
        args = [sys.executable, str(HELPER)]
        for server, port in servers:
            args += ["--server", server, "--port", str(port)]
        args += ["--timeout", str(timeout), "--"] + (command or self.dependent())
        # Logs go to a file so a regressed helper cannot deadlock this harness's
        # stdout pipe or allocate unbounded captured output.
        with tempfile.TemporaryFile() as output:
            process = subprocess.Popen(args, stdout=output, stderr=output)
            try:
                code = process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=2)
                self.fail("helper exceeded 10-second subprocess deadline")
            output.seek(0)
            log = output.read(8192).decode("utf-8", errors="replace")
        return code, log

    def test_occupied_port_rejected_without_running_dependent(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(8)
            port = listener.getsockname()[1]
            fail_server = shell_command([sys.executable, "-c", "raise SystemExit(7)"])
            code, log = self.run_helper([(fail_server, port)])
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                pass  # The helper must leave the unrelated listener alone.
            self.assertNotEqual(code, 0, log)
            self.assertFalse(self.marker.exists(), log)

    def test_early_server_exit_does_not_run_dependent(self):
        fail_server = shell_command([sys.executable, "-c", "raise SystemExit(7)"])
        code, log = self.run_helper([(fail_server, self.free_port())])
        self.assertNotEqual(code, 0, log)
        self.assertFalse(self.marker.exists(), log)

    def test_http_readiness_and_dependent_exit_propagation(self):
        port = self.free_port()
        code, log = self.run_helper([(self.server_command(port), port)],
                                    self.dependent(port, exit_code=23), timeout=3)
        self.assertEqual(code, 23, log)
        self.assertTrue(self.marker.exists(), log)

    def test_startup_timeout_does_not_run_dependent(self):
        port = self.free_port()
        code, log = self.run_helper([(self.server_command(port, "never"), port)])
        self.assertNotEqual(code, 0, log)
        self.assertFalse(self.marker.exists(), log)

    def test_verbose_server_can_reach_readiness(self):
        port = self.free_port()
        code, log = self.run_helper([(self.server_command(port, "verbose"), port)],
                                    self.dependent(port), timeout=3)
        self.assertEqual(code, 0, log)
        self.assertTrue(self.marker.exists(), log)

    def test_all_ports_preflighted_before_first_server_launch(self):
        with socket.socket() as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(8)
            occupied = listener.getsockname()[1]
            first_port = self.free_port()
            first = self.server_command(first_port)
            second = shell_command([sys.executable, "-c", "raise SystemExit(7)"])
            code, log = self.run_helper([(first, first_port), (second, occupied)])
            self.assertFalse(self.fixtures[0][2].exists(),
                             "first server was launched before second port was checked\n" + log)
            self.assertNotEqual(code, 0, log)
            self.assertFalse(self.marker.exists(), log)


if __name__ == "__main__":
    unittest.main()
