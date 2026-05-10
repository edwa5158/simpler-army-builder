# simpler-army-builder

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_simpler-army-builder&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=edwa5158_simpler-army-builder)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_simpler-army-builder&metric=bugs)](https://sonarcloud.io/summary/new_code?id=edwa5158_simpler-army-builder)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_simpler-army-builder&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=edwa5158_simpler-army-builder)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_simpler-army-builder&metric=coverage)](https://sonarcloud.io/summary/new_code?id=edwa5158_simpler-army-builder)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=edwa5158_simpler-army-builder&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=edwa5158_simpler-army-builder)

## Dependency flow

The codebase is intended to follow a one-way dependency flow so that outer layers depend on inner layers, and not the other way around.

### Allowed imports

- `main.py` is the composition root / entrypoint. It may import from `ui`, `infrastructure`, `core`, and `config.py`.
- `ui` may import from `ui`, `infrastructure`, and `core`.
- `infrastructure` may import from `infrastructure` and `core`.
- `core` may import from `core` only, plus standard-library or third-party dependencies.
- `config.py` may only be imported by `main.py`, and `config.py` should not import from any project package.

### Dependency direction

In simplified form, the allowed project-level dependency direction is:

- `main.py -> ui -> infrastructure -> core`
- `main.py -> infrastructure -> core`
- `main.py -> core`
- `main.py` may depend on `config.py`
- `ui` and `infrastructure` should receive configured values from `main.py` via arguments or other wiring, rather than importing `config.py` directly

### Not allowed

- `core` must not import from `infrastructure`, `ui`, `main.py`, or `config.py`.
- `infrastructure` must not import from `ui`, `main.py`, or `config.py`.
- `ui` must not import from `main.py` or `config.py`.
- No package should import from `main.py`; it is the top-level executable entrypoint.
- Dependency flow must never point back outward. For example, `core <- infrastructure <- ui <- main.py` is allowed, but the reverse direction is not.

These rules are here to keep responsibilities clear and improve testability:

- `main.py` wires the application together and is the only place that should read from `config.py`.
- `ui` handles user interaction.
- `infrastructure` holds app/data structures and persistence-oriented behavior.
- `core` holds shared low-level helpers.
- `config.py` provides configuration constants for `main.py`, so other packages can receive those values explicitly instead of importing constants everywhere.

### Import rules summary table

| Importer (the code doing the import) | Allowed to import from | Not allowed to import from |
| --- | --- | --- |
| `main.py` | `ui`, `infrastructure`, `core`, `config.py` | Nothing in this project should import `main.py` |
| `ui` package | `ui`, `infrastructure`, `core` | `main.py`, `config.py` |
| `infrastructure` package | `infrastructure`, `core` | `ui`, `main.py`, `config.py` |
| `core` package | `core` only | `infrastructure`, `ui`, `main.py`, `config.py` |
| `config.py` | no project packages | `core`, `infrastructure`, `ui`, `main.py` |

This table is intended as a quick reference: read each row as "this code may import these modules, and must not import these others."
