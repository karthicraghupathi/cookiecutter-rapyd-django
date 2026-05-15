# AGENTS.md

This file orients AI coding agents and human contributors who are new to this repo.

## What this repo is

A Cookiecutter template that scaffolds a Django project. Running
`uvx cookiecutter <this-repo>` produces a fresh project pre-configured with uv, ruff,
pre-commit, Django 4.2 LTS, `environs`-based settings, and the `modernauth` custom
user model (email as username).

## Two-tree layout

- **Root** — the template repo's own dev environment (uv-managed). Run tests from here.
- **`{{ cookiecutter.project_directory }}/`** — the templated tree. Cookiecutter
  substitutes Jinja tokens here at bake time. The literal directory name is the Jinja
  variable.

The two `.pre-commit-config.yaml` files (root + inside the template dir) are
intentionally independent. Don't symlink them.

## Cookiecutter mechanics

- Prompts live in `cookiecutter.json` (lists become choice prompts; first item is the
  default).
- The pre-generation hook is `hooks/pre_gen_project.py` — validates inputs (slug,
  email, unsafe chars) before rendering starts.
- The post-generation hook is `hooks/post_gen_project.py` (cross-platform Python) —
  copies `.env.example` to `.env` with a fresh random `DJANGO_SECRET_KEY`, then runs
  `git init`, `uv sync --all-groups`, pre-commit install, and
  `pre-commit run --all-files`.
- Templated values in hook scripts are rendered via Jinja's `|tojson` filter so quotes
  and backslashes in user input can't break Python parsing of the hook.
- Hooks and the template directory are excluded from the repo-level ruff check because
  they contain unrendered Jinja syntax (`{{ cookiecutter.* }}`) that is invalid Python
  until cookiecutter substitutes it.

## Verification commands

After any change, run from the repo root:

```bash
uv sync                              # ensure deps are current
uv run pytest                        # bakes the template and asserts the output
uv run ruff check .                  # lint
uv run pre-commit run --all-files    # full hook pass
```

If a test fails after editing template files, the bake itself probably broke — check
the test output for the temp directory path and inspect the rendered tree directly.

## Adding a new cookiecutter prompt

1. Add the key to `cookiecutter.json` (use a list for choices).
2. Reference it in template files via `{{ cookiecutter.<key> }}`.
3. If the value needs validation, add a check in `hooks/pre_gen_project.py`.
4. If it affects post-generation setup, update `hooks/post_gen_project.py`.
5. Add a test in `test_cookiecutter.py` that bakes with the new value and asserts the
   rendered output.

## Django-specific notes

- The generated project uses `modernauth.User` as the custom user model. Any new app
  that has a relationship to `User` should import it via `get_user_model()`, never
  directly from `modernauth`.
- Settings live in `{{ cookiecutter.project_slug }}/config/settings.py`. All
  environment reads go through `environs.Env()`. Don't add bare `os.environ` calls.
- Database defaults to SQLite via `DATABASE_URL`. Change the `.env` value for
  PostgreSQL or another backend.
