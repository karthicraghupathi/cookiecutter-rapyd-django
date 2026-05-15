"""Cookiecutter pre-generation hook.

Runs after prompts are answered, before the template tree is rendered.
Validates user-supplied values to fail fast with a clear message instead
of producing a broken project. Templated values are rendered via Jinja's
`|tojson` filter, which makes the hook itself robust to weird input even
before validation runs.

Validations:
- `project_slug` must be a valid ASCII Python identifier (importable as a
  module) and not a Python reserved keyword.
- `project_name`, `author_name`, and `project_description` must not contain
  characters that would surprise downstream consumers (quotes, backslashes,
  control chars).
- `author_email` must match a practical email regex.
"""

from __future__ import annotations

import keyword
import re
import sys

# Templated values are rendered via Jinja's `|tojson` filter so that any
# quote, backslash, or newline in user input is safely escaped before our
# validation logic runs.
PROJECT_SLUG = {{cookiecutter.project_slug | tojson}}
PROJECT_NAME = {{cookiecutter.project_name | tojson}}
AUTHOR_NAME = {{cookiecutter.author_name | tojson}}
AUTHOR_EMAIL = {{cookiecutter.author_email | tojson}}
PROJECT_DESCRIPTION = {{cookiecutter.project_description | tojson}}

# Standard practical email pattern. Disallows quotes, backslashes, and
# whitespace; requires a TLD of 2+ ASCII letters.
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

# Slug becomes a package dir, an importable module, AND the PEP 621
# `name =` field. str.isidentifier() accepts non-ASCII (UAX-31)
# identifiers which break pyproject metadata and uv — gate on ASCII.
SLUG_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

UNSAFE_CHARS = ('"', "\\", "\n", "\r", "\t", "\x00")


def fail(message: str) -> None:
    print(f"\033[31m[pre-gen hook] {message}\033[0m", file=sys.stderr)
    sys.exit(1)


def validate_slug() -> None:
    if not SLUG_RE.match(PROJECT_SLUG):
        fail(
            f"project_slug={PROJECT_SLUG!r} is not a valid ASCII Python "
            "identifier. Use ASCII letters, digits, and underscores; must "
            "start with a letter or underscore. Try setting project_name to "
            "a value that produces a clean slug, or override project_slug "
            "at the prompt."
        )
    if keyword.iskeyword(PROJECT_SLUG):
        fail(
            f"project_slug={PROJECT_SLUG!r} is a Python reserved keyword. "
            "Pick a different project name."
        )


def validate_no_unsafe_chars(field: str, value: str) -> None:
    for ch in UNSAFE_CHARS:
        if ch in value:
            label = {
                "\n": "newline",
                "\r": "carriage return",
                "\t": "tab",
                "\x00": "null byte",
            }.get(ch, repr(ch))
            fail(
                f"{field}={value!r} contains {label}, which produces broken or "
                "confusing output in generated files. Remove the offending character."
            )


def validate_email() -> None:
    if not EMAIL_RE.match(AUTHOR_EMAIL):
        fail(
            f"author_email={AUTHOR_EMAIL!r} doesn't look like an email address "
            "(expected user@host.tld; quotes/backslashes/spaces are not allowed)."
        )


def main() -> None:
    validate_slug()
    validate_no_unsafe_chars("project_name", PROJECT_NAME)
    validate_no_unsafe_chars("author_name", AUTHOR_NAME)
    validate_no_unsafe_chars("project_description", PROJECT_DESCRIPTION)
    validate_email()


if __name__ == "__main__":
    main()
