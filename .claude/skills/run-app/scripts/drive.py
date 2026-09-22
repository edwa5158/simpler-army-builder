"""Drive the simpler-army-builder TUI headlessly and print what the screen shows.

Spawns the app in a pseudo-terminal, feeds it keystrokes one step at a time, and
renders the terminal with pyte so each snapshot is the text a human would see.
The app runs against a throwaway copy of data_store/, so nothing real is touched.

Run from the repo root (pyte is pulled in ephemerally, not added to the project):

    uv run --with pyte python .claude/skills/run-app/scripts/drive.py [options] STEP...

Steps: up down left right enter tab esc space backspace ctrl-c pageup pagedown,
optionally repeated as `down*3`; `text:Some words` types literal text;
`wait:1.5` sleeps without sending anything.
"""

from __future__ import annotations

import argparse
import difflib
import os
import pty
import re
import select
import shutil
import signal
import struct
import sys
import tempfile
import termios
import time
from fcntl import ioctl
from pathlib import Path

import pyte

ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b[@-_]|\r")

REPO = Path(__file__).resolve().parents[4]

KEYS = {
    "up": "\x1b[A",
    "down": "\x1b[B",
    "right": "\x1b[C",
    "left": "\x1b[D",
    "enter": "\r",
    "tab": "\t",
    "esc": "\x1b",
    "space": " ",
    "backspace": "\x7f",
    "ctrl-c": "\x03",
    "pageup": "\x1b[5~",
    "pagedown": "\x1b[6~",
}

APP_LAUNCHER = """
import sys
from app import App, AppState
from ui.screen import ScreenName
App(ScreenName.MAIN_MENU, AppState(sys.argv[1], sys.argv[2])).run()
"""


def parse_step(step: str) -> tuple[str, str | float]:
    if step.startswith("text:"):
        return step, step[len("text:") :]
    if step.startswith("wait:"):
        return step, float(step[len("wait:") :])
    name, _, count = step.partition("*")
    if name not in KEYS:
        sys.exit(f"Unknown step {step!r}. Keys: {', '.join(KEYS)}; or text:..., wait:N")
    return step, KEYS[name] * int(count or 1)


def read_until_quiet(fd: int, stream: pyte.ByteStream, quiet: float, timeout: float, log: bytearray) -> bool:
    """Feed pty output to the emulator until it has been silent for `quiet` seconds.

    Returns False once the child has closed the pty (exited).
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        ready, _, _ = select.select([fd], [], [], quiet)
        if not ready:
            return True
        try:
            data = os.read(fd, 65536)
        except OSError:
            return False
        if not data:
            return False
        log.extend(data)
        stream.feed(data)
    return True


def snapshot(screen: pyte.Screen) -> str:
    lines = [line.rstrip() for line in screen.display]
    while lines and not lines[-1]:
        lines.pop()
    cursor = f"(cursor row {screen.cursor.y}, col {screen.cursor.x})"
    return "\n".join(lines) + f"\n{cursor}"


def diff_data(original: Path, sandbox: Path) -> str:
    out: list[str] = []
    for path in sorted(sandbox.glob("*.json")):
        before_path = original / path.name
        before = before_path.read_text().splitlines() if before_path.exists() else []
        after = path.read_text().splitlines()
        label = path.name if before_path.exists() else f"{path.name} (new file)"
        out.extend(difflib.unified_diff(before, after, f"data_store/{label}", f"sandbox/{label}", lineterm=""))
    return "\n".join(out) or "(no data files changed)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("steps", nargs="*", help="keystroke steps to send, in order")
    parser.add_argument("--target", choices=["app", "preview"], default="app")
    parser.add_argument("--cols", type=int, default=100)
    parser.add_argument("--rows", type=int, default=40)
    parser.add_argument("--quiet", type=float, default=0.5, help="seconds of silence that count as 'settled'")
    parser.add_argument("--startup-timeout", type=float, default=20.0)
    parser.add_argument("--empty-data", action="store_true", help="start with no data files (first-run behaviour)")
    parser.add_argument("--live-data", action="store_true", help="use the real data_store/ instead of a sandbox copy")
    parser.add_argument("--final-only", action="store_true", help="print only the last snapshot")
    args = parser.parse_args()
    steps = [parse_step(s) for s in args.steps]

    data_src = REPO / "data_store"
    if args.live_data:
        data_dir = data_src
    else:
        data_dir = Path(tempfile.mkdtemp(prefix="army-builder-data-"))
        if not args.empty_data:
            for f in data_src.glob("*.json"):
                shutil.copy2(f, data_dir)
    army, warscroll = str(data_dir / "army.json"), str(data_dir / "warscroll.json")

    if args.target == "app":
        cmd = ["uv", "run", "python", "-c", APP_LAUNCHER, army, warscroll]
    else:
        cmd = ["uv", "run", "python", "preview.py", warscroll]

    screen = pyte.Screen(args.cols, args.rows)
    stream = pyte.ByteStream(screen)

    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(REPO)
        os.environ.pop("VIRTUAL_ENV", None)  # set by `uv run --with`; would confuse the inner `uv run`
        # pyte never answers cursor-position requests; tell prompt_toolkit not to ask.
        os.environ.update(
            TERM="xterm-256color", COLUMNS=str(args.cols), LINES=str(args.rows), PROMPT_TOOLKIT_NO_CPR="1"
        )
        os.execvp(cmd[0], cmd)
    ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", args.rows, args.cols, 0, 0))

    print(f"$ {' '.join(cmd[:3])} ...  (data: {data_dir})\n")
    log = bytearray()
    alive = read_until_quiet(fd, stream, max(args.quiet, 1.5), args.startup_timeout, log)
    shots = [("startup", snapshot(screen))]

    for label, payload in steps:
        if not alive:
            shots.append((f"{label} (skipped: app already exited)", ""))
            continue
        if isinstance(payload, float):
            time.sleep(payload)
        else:
            for ch in payload:  # one key at a time so prompt_toolkit sees discrete presses
                os.write(fd, ch.encode())
                time.sleep(0.05)
        alive = read_until_quiet(fd, stream, args.quiet, 10.0, log)
        shots.append((label, snapshot(screen)))

    if alive:
        os.kill(pid, signal.SIGTERM)
        time.sleep(0.3)
    else:
        read_until_quiet(fd, stream, 0.2, 2.0, log)  # drain whatever the child wrote on the way out
    _, status = os.waitpid(pid, 0)
    exit_code = os.waitstatus_to_exitcode(status)

    for label, text in shots[-1:] if args.final_only else shots:
        print(f"===== after: {label} =====")
        if text:
            print(text)
        print()

    ended = f"exited with code {exit_code}" if not alive else "still running after last step (terminated by driver)"
    print(f"===== app {ended} =====\n")
    if not alive and exit_code != 0:
        # Tracebacks often scroll past the emulated screen, so show the raw tail too.
        tail = ANSI.sub("", log.decode(errors="replace")).splitlines()[-40:]
        print("===== last output before exit (raw, ANSI stripped) =====")
        print("\n".join(tail) + "\n")
    print("===== data changes vs data_store/ =====")
    print(diff_data(data_src, data_dir) if not args.live_data else "(live data mode: compare with git diff data_store/)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
