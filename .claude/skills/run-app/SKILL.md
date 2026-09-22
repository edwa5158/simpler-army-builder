---
name: run-app
description: Launch and drive the simpler-army-builder terminal app (app.py or the preview.py warscroll browser) headlessly, send it keystrokes, and read back exactly what the screen shows, including crashes and what got saved to the JSON data files. Use this whenever you need to run, start, launch, try, smoke-test, reproduce a bug in, or screenshot the app, or to confirm a UI change in ui/*.py actually works. The *_ui.py files are excluded from pytest, so running the app this way is the only real check on them. Use it even if the user just says "does it work now?" after a UI edit.
---

# Running simpler-army-builder

The app is an interactive prompt-toolkit TUI, so you can't just run `python app.py` in Bash: it blocks waiting for keys, and its raw output is escape-code soup. `scripts/drive.py` solves this. It starts the app in a pseudo-terminal, sends your keystrokes one step at a time, and emulates the terminal (with `pyte`) so each snapshot is the plain text a person would see.

It also runs the app against a **throwaway copy of `data_store/`**. The app writes to `army.json` whenever an army is created, and those files are committed, so sandboxing keeps test runs out of `git diff`. At the end it prints a diff of what the run changed in the data files, which is often the simplest way to check a save flow.

## Usage

`pyte` is pulled in on the fly by `--with`, so it never touches `pyproject.toml`. The script finds the repo from its own location, so it works from any directory. Use the absolute path so it doesn't matter where your shell's cwd ends up:

```bash
uv run --with pyte python <repo>/.claude/skills/run-app/scripts/drive.py [options] STEP...
```

Steps are sent in order, and a snapshot is taken after each one:

| Step | Sends |
| --- | --- |
| `up` `down` `left` `right` `enter` `tab` `esc` `space` `backspace` `pageup` `pagedown` `ctrl-c` | that key |
| `down*3` | a key repeated |
| `text:Skaven Test` | literal typed text (quote the whole step in the shell) |
| `wait:1.5` | nothing; just waits, then snapshots |

Options you'll actually use:

- `--target preview` runs `preview.py`, the full-screen master/detail warscroll browser, instead of `app.py`.
- `--final-only` prints just the last snapshot. Use it once you know the path and only care where it ends up.
- `--empty-data` starts with no data files, to test first-run behavior.
- `--rows N` / `--cols N` set the terminal size (default 40×100). Increase rows if a long list or traceback is cut off at the top.
- `--live-data` uses the real `data_store/`. Only use it when the user explicitly wants real data changed.

With no steps, it just shows the startup screen.

## How to work with it

**Explore first, then script.** Menus don't all default to the first option. For example, Manage Armies starts on *Load Army*, so a blind `down enter` can hit *Exit*. Start from a known path below if one fits. Otherwise run a short sequence, read the snapshot to see where the `>` cursor is, then extend it. Each invocation starts fresh from the main menu and replays the whole path, which only takes a few seconds.

Known paths at the time of writing. Menus change, so trust the snapshot over this table:

| Goal | Steps |
| --- | --- |
| Create an army | `enter up enter "text:Name" enter` |
| Load the first saved army | `enter enter enter` |
| Warscroll list | `down enter` |
| Preview browser, move/switch panes | `--target preview` then `down`, `tab` |

**Reading snapshots.** Inline menus stack up on screen, so each snapshot still contains the earlier menus. The current screen is at the bottom, with the `>` marking the highlighted option.

**Read the ending.** The footer says one of three things:
- `still running after last step`: normal. The app was waiting for more input and the driver stopped it.
- `exited with code 0`: the app quit on its own. In `app.py`, choosing *Exit* in any menu ends the whole app, not just that menu.
- `exited with code 1`: a crash. The traceback is in the final snapshot and repeated under "last output before exit", because long tracebacks scroll past the emulated screen.

**Check that the screen is right, not just that it rendered.** A screen that shows up without crashing proves little. Before reporting that a load or view flow "works", read the relevant `data_store/*.json` (the sandbox starts as an exact copy) and compare names, regiments, and points with what the screen shows. For save flows, use the data diff at the end: a flow that should save but shows "(no data files changed)" didn't save.

**Reading the code for a flow.** Navigation lives in `app.py`: `registry()` maps each `ScreenName` to a `Screen`, and whatever a screen's `show()` returns becomes the next screen. To find out what a menu offers, read the `show()` of the screen you're on. `registry()` builds every screen once, at startup, so screens capture `AppState` values from launch and don't see later changes. That's the likely cause when a screen shows stale or placeholder data. For example, an army you create won't show up in *Load Army* later in the same run. That's an app bug worth reporting, not a driver artifact.

## Example

Create a new army and confirm it gets saved:

```bash
uv run --with pyte python <repo>/.claude/skills/run-app/scripts/drive.py --final-only \
  enter up enter "text:Skaven Test" enter
```

The final snapshot shows `Army Name: Skaven Test` above the regiment menu, and the data diff shows a new `"Skaven Test"` entry in `army.json`.

## Reporting back

Tell the user what you ran (the steps) and what happened, quoting the relevant snapshot lines, not every snapshot. If the app crashed, give the exception and the `file:line` from the traceback. If you found the bug through a particular key sequence, include the exact `drive.py` command so it can be rerun after a fix.

If the user wants to try it themselves, they should run `uv run python app.py` (or `uv run python preview.py`) in their own terminal. It needs a real interactive terminal, so a `!` command in this session won't work. That command uses the real `data_store/`.
