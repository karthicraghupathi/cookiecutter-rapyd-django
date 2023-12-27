.PHONY: all supervisor

all: supervisor

supervisor:
	rm -f /etc/supervisor/conf.d/{{ cookiecutter.project_slug }}.conf
	ln -s `pwd`/supervisor.conf /etc/supervisor/conf.d/{{ cookiecutter.project_slug }}.conf
