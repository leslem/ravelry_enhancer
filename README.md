# Ravelry Enhancer

A Django app to build personalized functionality to enhance the way I use Ravelry

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy ravelry_enhancer

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.


## TODO

- [ ] tool tracker (knitting needles, crochet hooks, looms, spindles, etc.)
    - characteristics from the GSheet, but also notes, maybe to-do's
    - management command to import data from the GSheet
- [ ] rav connection
    - pull projects
    - pull stash
    - pull queue
- [ ] project summary builder (with fields from my template .md)
- [ ] Custom views
    - Queue
        - Sort by age of stash
        - Sort by yardage of stash
        - Sort by age of pattern
    - Stash by storage location
    - Stash by color family
- [ ] visualizations
    - Yardage over time
    - Projects over time
    - Stash over time (in and out)
    - Stash by color family
    - Time from yarn purchase to cast on
