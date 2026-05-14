.PHONY: install lint format test supervisor

install:
	uv sync --all-groups

lint:
	uv run ruff check .

format:
	uv run ruff format .

test:
	uv run pytest

supervisor:
	rm -f /etc/supervisor/conf.d/{{ cookiecutter.project_slug }}.conf
	ln -s `pwd`/supervisor.conf /etc/supervisor/conf.d/{{ cookiecutter.project_slug }}.conf
