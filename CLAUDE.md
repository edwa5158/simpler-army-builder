# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A terminal army-list builder for Warhammer Age of Sigmar, built on `prompt-toolkit`. Python 3.12, managed with `uv`.

## Commands

```bash
uv sync                       # install deps (incl. dev group)
uv run python app.py          # run the app (current screen-stack entrypoint)
uv run python preview.py [path/to/warscroll.json]   # launch the warscroll preview UI standalone
uv run pytest                 # full test suite (coverage on core+infrastructure, fails under 70%)
uv run pytest tests/test_army.py::test_name        # single test
uv run pytest --no-cov        # skip coverage when iterating
uv run ruff check . && uv run ruff format .
uv run isort .
uv run ty check               # or: uv run pyrefly check
```

Coverage config lives in `pyproject.toml`; `*_ui.py` files are excluded from both pytest collection and coverage, so UI modules are unverified by the suite — exercise them manually via `app.py`/`preview.py`.

## Architecture

### Layering (enforced by convention — see README.md for the full table)

`main.py -> ui -> infrastructure -> core`, one-way only.

- `config.py` holds data-file paths and may only be imported by the entrypoints; `ui` and `infrastructure` must receive paths as arguments instead. (Note: `main.py` and `app.py` currently violate this by importing `config` — new code should keep paths injected.)
- `core/shared.py` is layout-only text helpers (fixed 75-char rows for regiment headers and unit rows).
- `infrastructure/` holds the domain model plus its JSON persistence.
- `ui/` holds prompt-toolkit screens.

### Two entrypoints, two generations

- `app.py` is the current design: an `App` holds a stack of `ScreenName` enum values, pops one, looks it up in a `registry()` dict of `Screen` instances, calls `show()`, and pushes whatever `ScreenName` that returns. Adding a screen means adding a `ScreenName` member (with its `display_name`), a `Screen` subclass in `ui/`, and a registry entry. Note `registry()` is built once per `run()`, so screens capture `AppState` values at construction time.
- `main.py` is the older controller-style entrypoint (`main_menu_controller`, `*_controller` functions) kept alongside it. It duplicates `AppState`. Prefer `app.py` for new work.

`AppState` tracks `current_army`, `warscrolls`, the two dirty flags and the two file paths. The dirty flags exist but are not yet wired — `save()` writes unconditionally.

### Domain model

`Army -> list[Regiment] -> list[UnitNumbered] -> Unit -> Warscroll`

Every class implements `to_dict()` / `from_dict()` against a matching `TypedDict` (`ArmyDict`, `RegimentDict`, `UnitNumDict`, `UnitDict`, `WarscrollDict`), and that pair is the persistence format — JSON files are dicts keyed by name (`ArmiesDict`, `WarscrollsDict`). `points` is a computed property that rolls up from units. `Army._regiment_number` / `Regiment._unit_number` are monotonic counters for auto-naming and renumbering; `Regiment.from_dict` does not currently restore `_unit_number`.

`UnitNumbered` is a thin positional wrapper around `Unit` that proxies `warscroll`/`wargear`; it is what lives in `Regiment.units`, not bare `Unit`.

`Warscroll.__init__` is overloaded: `(name, points, is_hero)` (the legacy short form used throughout the tests) or the full `(name, type, descr, points, is_hero, ...)`. The positional-int-in-slot-2 check is what disambiguates them.

`Warscrolls` keeps a parallel `catalog` (objects) and `serialized_catalog` (dicts); `append_warscroll` updates both, and `save_warscrolls` writes only `serialized_catalog`. `Warscrolls.load_warscrolls` is a classmethod that returns a raw dict, not a `Warscrolls`.

### Data files

`data_store/army.json`, `data_store/warscroll.json`, and `data_store/test_army.json` are committed and read at runtime via the `config.py` constants. Tests write to `TEST_ARMY_PATH` and clean up with `core.shared.delete_file_if_it_exists`. A stale `infrastructure/army.json` also exists and is unused.

## Git workflow

This is a one-person project: commit and push straight to `main` unless told otherwise. Don't create feature branches or pull requests. CI (`.github/workflows/main.yml`) runs on pushes to `main`.

## Other

- `planned_flow.mmd` is the target navigation flowchart; `TODO.md` is the gap list between it and the code.
- Diagrams belong in `.mmd` files in the project root (see `.github/instructions/mermaid.instructions.md` — its tooling is VS Code/Copilot-specific).
- SonarCloud runs on this repo (`sonar-project.properties`) and consumes `coverage.xml` produced by the pytest run.
