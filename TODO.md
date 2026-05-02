## Assistant

Great plan diagram — I compared it against the current codebase (`main.py`, `army_ui.py`, `regiment_ui.py`, `unit_ui.py`, `warscroll_ui.py`, and model files), and here’s a practical TODO list of what still needs to be built.

## TODOs (what’s still missing)

### 1) App shell & navigation
- [ ] Implement a real top-level `main_menu()` loop with:
  - `Manage armies`
  - `Manage warscrolls`
  - `Exit`
- [ ] Add app state tracking (at minimum: `current_army`, `dirty` flag).
- [ ] Implement exit guard flow:
  - `Unsaved changes?`
  - `Save / Discard / Cancel`
  - Save error handling loop back on failure.

### 2) Startup/config initialization
- [ ] Add startup step to initialize config/data dirs/files (currently paths are simple relative file names).
- [ ] Handle first-run file creation cleanly (`army.json`, `warscroll.json` if missing).

### 3) Army management flow
- [ ] Add `delete_army` flow in `army_selection()`:
  - select army
  - confirm delete
  - delete result handling
- [ ] Add explicit empty state handling when no army files exist.
- [ ] Add army-name validation for `new_army()` (non-empty, collision handling).
- [ ] Keep menu loops/back behavior matching the flowchart (currently mostly single-pass).

### 4) Regiment management flow
- [ ] Expand `regiment_selection_menu()` to support:
  - existing regiment
  - new regiment
  - delete regiment
  - back
- [ ] Implement `Army.remove_regiment(...)` in model layer.
- [ ] Add empty-state + confirm-delete handling.
- [ ] Ensure navigation returns to intended parent menu states.

### 5) Unit management flow
- [ ] Expand `unit_selection_menu()` to support:
  - existing unit
  - new unit
  - delete unit
  - back to regiments / back to main
- [ ] Fix `new_unit()` so it actually creates from selected warscroll and adds to regiment.
- [ ] Remove placeholder behavior (`UnitNumbered(..., 99)`).
- [ ] Add empty-state + confirm-delete handling for units.

### 6) “Create unit from warscroll” branch
- [ ] Make `warscroll_selection()` return a selected warscroll (not just print names).
- [ ] Implement “no warscrolls exist” branch:
  - prompt to create now
  - create + save warscroll
  - continue unit creation
- [ ] Ensure `Unit.from_warscroll(ws)` is used and validated before add.

### 7) Unit editing flow
- [ ] Add `unit_edit_menu(unit)` with:
  - view
  - edit stats/options
  - change warscroll
  - save army
  - back routes
- [ ] Implement `display_unit(unit)`.
- [ ] Implement `edit_unit(unit)` with validation.
- [ ] Implement warscroll swap (`apply_warscroll`-style behavior).
- [ ] Mark army dirty on edits; clear dirty on successful save.

### 8) Warscroll management flow
- [ ] Build `warscroll_menu()` with:
  - view
  - add
  - edit
  - delete
  - back
- [ ] Implement:
  - `select_warscroll()`
  - `create_warscroll()`
  - `edit_warscroll(ws)`
  - `save_warscroll()`
  - `delete_warscroll()`
- [ ] Add validation/error/empty-state handling for every branch.
- [ ] Add confirm-delete flow for warscroll deletion.

### 9) Data/model correctness gaps
- [ ] Fix `Army.from_dict()` to restore `_regiment_number`.
- [ ] Fix `Regiment.from_dict()` to restore `_unit_number`.
- [ ] Replace mutable default arg in `Regiment.__init__(..., units=[])` with `None`.
- [ ] Add robust file I/O error handling around save/load/delete operations.

### 10) Test coverage for planned flow (currently mostly model-only)
- [ ] Add tests for menu/control-flow branches (including back/cancel loops).
- [ ] Add tests for dirty-flag and exit save/discard/cancel logic.
- [ ] Add tests for delete flows (army/regiment/unit/warscroll).
- [ ] Add tests for no-warscroll create-now branch.
- [ ] Add regression tests for restored numbering counters after load.

---

If you want, I can turn this into a **prioritized implementation plan** (Phase 1/2/3) so you can tackle the highest-impact pieces first.
