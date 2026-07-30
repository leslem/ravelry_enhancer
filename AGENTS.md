# Project memory for Ravelry Enhancer

## Project overview
- Name: Ravelry Enhancer
- Type: Django app
- Purpose: Build personalized functionality to enhance how the user interacts with Ravelry data.
- Based on Cookiecutter Django.

## Key project structure
- Main Django project root: `ravelry_enhancer/`
- App(s): `tool_tracker`, `core`
- Configuration: `config/` for the Django settings package
- Local migrations: `ravelry_enhancer/tool_tracker/migrations/`

## Development environment
- Python version: 3.12
- Virtual environment: `.venv`
- Database: PostgreSQL (PostgreSQL 16 in local setup notes)
- Uses `.env` with `DJANGO_READ_DOT_ENV_FILE=True` and `DJANGO_SETTINGS_MODULE=config.settings.local`

## Common commands
- `python manage.py createsuperuser`
- `python manage.py migrate`
- `python manage.py runserver`
- `python manage.py reset_db --noinput` (django-extensions)
- `pytest`
- `coverage run -m pytest`
- `coverage html`
- `mypy ravelry_enhancer`

## Notes / current goals
- Tool tracker for knitting needles, crochet hooks, looms, spindles, etc.
- Possible future integrations:
  - Import tool data from Google Sheets
  - Ravelry connection for projects, stash, queue
  - Project summary builder
  - Custom views and visualizations for stash/project metrics
