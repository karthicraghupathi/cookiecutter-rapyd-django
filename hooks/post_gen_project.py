"""Cookiecutter post-generation hook.

Runs after the template is rendered, in the generated project's directory:
- Creates .env from .env.example with a freshly generated SECRET_KEY.
- Initializes a git repo and bootstraps the uv venv.
- Installs and runs pre-commit (best-effort; non-fatal).
- Makes an initial scaffold commit (identity scoped to that commit only).

Cross-platform: uses subprocess + pathlib instead of bash.
"""

from __future__ import annotations

import os
import secrets
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path.cwd()
PROJECT_SLUG = {{cookiecutter.project_slug | tojson}}
PYTHON_VERSION = {{cookiecutter.python_version | tojson}}


def fail(message: str) -> None:
    print(f"\033[31m[post-gen hook] {message}\033[0m", file=sys.stderr)
    sys.exit(1)


def info(message: str) -> None:
    print(f"[post-gen hook] {message}")


def require_command(cmd: str, install_hint: str) -> None:
    if shutil.which(cmd) is None:
        fail(f"`{cmd}` not found on PATH. Install: {install_hint}")


def create_env_file() -> None:
    """Copy .env.example to .env, replacing the placeholder SECRET_KEY."""
    src = PROJECT_DIR / ".env.example"
    dst = PROJECT_DIR / ".env"
    if not src.exists():
        fail(".env.example not found — template is broken; cannot create .env")
    if dst.exists():
        info(".env already exists — skipping")
        return
    secret_key = secrets.token_urlsafe(50)
    content = src.read_text(encoding="utf-8").replace(
        "DJANGO_SECRET_KEY=changeme",
        f"DJANGO_SECRET_KEY={secret_key}",
    )
    dst.write_text(content, encoding="utf-8")
    info("Created .env with a random DJANGO_SECRET_KEY")


_ENV = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "VIRTUAL_ENV_PROMPT", "UV_PYTHON")}


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    info(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=PROJECT_DIR, env=_ENV, check=check)  # noqa: S603


# Files the scaffold must ship. uv.lock comes from `uv sync`; the
# requirements*.txt files come from the uv-export pre-commit hooks. Those
# steps are individually best-effort, but a committed scaffold missing
# them is broken — so verify before the initial commit.
CRITICAL_GENERATED_FILES = ("uv.lock", "requirements.txt", "requirements-dev.txt")


def verify_critical_files() -> None:
    missing = [
        name
        for name in CRITICAL_GENERATED_FILES
        if not (PROJECT_DIR / name).is_file()
        or (PROJECT_DIR / name).stat().st_size == 0
    ]
    if missing:
        fail(
            "Expected generated file(s) missing or empty after dependency "
            f"resolution: {', '.join(missing)}. The uv sync / uv-export "
            "step likely failed above. Fix the cause and re-generate; the "
            "scaffold was not committed."
        )


def run_pre_commit_with_autofix_handling() -> None:
    """Run `pre-commit run --all-files`, treating auto-fix exits as non-fatal.

    Pre-commit exits non-zero both when a hook auto-fixes files and when a hook
    genuinely fails. A second pass disambiguates: if the second pass is clean,
    the first pass was just auto-fixing. If the second pass also fails, surface
    it as a warning (still non-fatal — the project is usable).
    """
    info("Running pre-commit on all files (best-effort)...")
    first = run(["uv", "run", "pre-commit", "run", "--all-files"], check=False)
    if first.returncode == 0:
        return

    info("First pre-commit pass exited non-zero; checking if it was auto-fix...")
    second = run(["uv", "run", "pre-commit", "run", "--all-files"], check=False)
    if second.returncode == 0:
        info(
            "pre-commit auto-fixed some files on the first pass; second pass "
            "is clean. Review and re-stage before committing."
        )
        return

    print(
        "\033[33m[post-gen hook] pre-commit hooks are still failing after a "
        "second pass. Review hook output above and fix before committing.\033[0m",
        file=sys.stderr,
    )


def main() -> None:
    require_command("git", "https://git-scm.com/downloads")
    require_command("uv", "https://docs.astral.sh/uv/getting-started/installation/")

    create_env_file()

    run(["git", "init", "-b", "main"])
    run(["uv", "sync", "--all-groups", "--python", PYTHON_VERSION])
    run(["git", "add", "."])
    run(["uv", "run", "pre-commit", "install"])
    run_pre_commit_with_autofix_handling()
    verify_critical_files()
    run(["git", "add", "."])
    run(
        [
            "git",
            "-c",
            "user.email=scaffold@localhost",
            "-c",
            "user.name=Cookiecutter Bootstrap",
            "commit",
            "-m",
            "chore: initial project scaffold",
        ]
    )

    info(f"Project ready at {PROJECT_DIR}")


if __name__ == "__main__":
    main()
