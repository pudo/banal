# banal

Python micro-utilities library for buffering type uncertainties. Pure standard library — no external dependencies allowed.

## Development

```bash
# Install with dev deps
pip install -e ".[dev]"

# Type checking (strict)
make typecheck    # or: mypy --strict banal

# Build distribution
make build        # or: python3 -m build
```

## PERFORMANCE IS CRITICAL

This library is called in tight inner loops across many downstream projects. Every unnecessary branch, type check, or import adds real cost. When making changes:

- Minimize the number of `isinstance` checks and conditional branches.
- Don't add a guard for a case that existing checks already exclude.
- Prefer the cheapest check that covers the needed cases.
- Benchmark before and after if you're unsure.

## Key constraints

- **No external dependencies.** Only Python standard library imports.
- **Strict mypy typing.** All code must pass `mypy --strict`.
- **Python 3.10+** compatibility required.

## Release

Uses `bumpversion` for versioning. Publishing to PyPI is automatic on tagged pushes via GitHub Actions.

## Modules

- `lists.py` — sequence utilities (`ensure_list`, `unique_list`, `chunked_iter`, etc.)
- `dicts.py` — mapping utilities (`ensure_dict`, `clean_dict`, `keys_values`)
- `cache.py` — hashing (`hash_data`, `bytes_iter`)
- `bools.py` — boolean coercion (`as_bool`)
- `filesystem.py` — path decoding (`decode_path`)
