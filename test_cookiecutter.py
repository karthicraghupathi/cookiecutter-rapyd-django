def test_bake_project(cookies):
    result = cookies.bake(
        extra_context={
            "project_name": "Django Boilerplate",
            "project_slug": "django_boilerplate",
            "project_directory": "django_boilerplate_project",
            "project_description": "Django Boilerplate contains all the\
                 boilerplate you need to create a Django application.",
        }
    )

    assert result.exit_code == 0
    assert result.exception is None

    assert result.project_path.name == "django_boilerplate_project"
    assert result.project_path.is_dir()
