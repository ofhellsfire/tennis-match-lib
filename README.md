# Tennis Match Lib

Provides functions and classes to parse and to work with tennis match scores.

## Dev Notes

Formatting

```
poetry run black --line-length 98 --target-version py39 --skip-string-normalization --color tennis_match_lib/
```

Linting / Static Analysis

```
poetry run pylint tennis_match_lib
```

Unit tests execution

```
poetry run pytest -vvs --cov=tennis_match_lib --cov-report term-missing
```
