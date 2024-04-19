# Project initialization

Record of how I set up the project on my Mac for local development.

## Set up the project template via `cookiecutter`

```
sudo port install py311-cookiecutter py312-cookiecutter
which cookiecutter-3.12

cd ~/devel
cookiecutter-3.12 https://github.com/cookiecutter/cookiecutter-django
#   [1/27] project_name (My Awesome Project): Ravelry Enhancer
#   [2/27] project_slug (ravelry_enhancer):
#   [3/27] description (Behold My Awesome Project!): A Django app to build personalized functionality to enhance the way I use Ravelry
#   [4/27] author_name (Daniel Roy Greenfeld): Leslie Emery
#   [5/27] domain_name (example.com):
#   [6/27] email (leslie-emery@example.com): leslie.s.emery@gmail.com
#   [7/27] version (0.1.0):
#   [8/27] Select open_source_license
#     1 - MIT
#     2 - BSD
#     3 - GPLv3
#     4 - Apache Software License 2.0
#     5 - Not open source
#     Choose from [1/2/3/4/5] (1): 1
#   [9/27] Select username_type
#     1 - username
#     2 - email
#     Choose from [1/2] (1): 2
#   [10/27] timezone (UTC): America/Los_Angeles
#   [11/27] windows (n): n
#   [12/27] Select editor
#     1 - None
#     2 - PyCharm
#     3 - VS Code
#     Choose from [1/2/3] (1): 3
#   [13/27] use_docker (n): n
#   [14/27] Select postgresql_version
#     1 - 16
#     2 - 15
#     3 - 14
#     4 - 13
#     5 - 12
#     Choose from [1/2/3/4/5] (1): 1
#   [15/27] Select cloud_provider
#     1 - AWS
#     2 - GCP
#     3 - Azure
#     4 - None
#     Choose from [1/2/3/4] (1): 4
#   [16/27] Select mail_service
#     1 - Mailgun
#     2 - Amazon SES
#     3 - Mailjet
#     4 - Mandrill
#     5 - Postmark
#     6 - Sendgrid
#     7 - SendinBlue
#     8 - SparkPost
#     9 - Other SMTP
#     Choose from [1/2/3/4/5/6/7/8/9] (1): 1
#   [17/27] use_async (n): n
#   [18/27] use_drf (n): n
#   [19/27] Select frontend_pipeline
#     1 - None
#     2 - Django Compressor
#     3 - Gulp
#     4 - Webpack
#     Choose from [1/2/3/4] (1): 1
#   [20/27] use_celery (n): n
#   [21/27] use_mailpit (n): n
#   [22/27] use_sentry (n): n
#   [23/27] use_whitenoise (n): y
#   [24/27] use_heroku (n): n
#   [25/27] Select ci_tool
#     1 - None
#     2 - Travis
#     3 - Gitlab
#     4 - Github
#     5 - Drone
#     Choose from [1/2/3/4/5] (1): 4
#   [26/27] keep_local_envs_in_vcs (y):
#   [27/27] debug (n):
#  [INFO]: .env(s) are only utilized when Docker Compose and/or Heroku support is enabled so keeping them does not make sense given your current setup.
#  [WARNING]: You chose to not use any cloud providers nor Docker, media files won't be served in production.
#  [SUCCESS]: Project initialized, keep up the good work!
```

## Set up Postgres server

- Make sure to click "allow" on the Settings popup that asks if it's ok for Terminal to control your computer. This is needed to create the postgres user properly.
    - The first time I tried to use the Postgres server, it didn't work, and I think it was because I'd missed this prompt while running my `macports_install.sh` script.
- The `postgresql16` port installs all of the necessary code, but the `postgresql16-server` portfile is just very short script that creates the postgres user and the `launchd` script that will be run by `port load`
- [PostgreSQL 16 port](https://ports.macports.org/port/postgresql16-server/details/)
- [MacPorts postgres server set up gist](https://gist.github.com/DrTom/4f2edcac26a0eae82360dbc9b18dd82c)

```
sudo port select postgresql postgresql16
sudo mkdir -p /opt/local/var/db/postgresql16/defaultdb
sudo chown postgres:postgres /opt/local/var/db/postgresql16/defaultdb
sudo -u postgres /bin/sh -c 'cd /opt/local/var/db/postgresql16 &&
/opt/local/lib/postgresql16/bin/initdb -D /opt/local/var/db/postgresql16/defaultdb'

sudo port load postgresql16-server
```

## Set up the app database in Postgres

```
# Log into the server as admin
createdb --username=postgres ravelry_enhancer
# psql --username=postgres
# create user leslie
CREATE USER leslie WITH PASSWORD '<the usual>' CREATEDB;
GRANT CREATE ON DATABASE ravelry_enhancer TO leslie;

CREATE USER ravelry_enhancer WITH PASSWORD '<password>' CREATEDB;
ALTER ROLE ravelry_enhancer SET client_encoding TO 'utf8';
ALTER ROLE ravelry_enhancer SET default_transaction_isolation TO 'read committed';
ALTER ROLE ravelry_enhancer SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ravelry_enhancer TO ravelry_enhancer;

# These additional steps required for postgres15 and up: https://stackoverflow.com/a/75876944
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ravelry_enhancer;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ravelry_enhancer;
GRANT ALL ON SCHEMA public TO ravelry_enhancer;
# This additional step required on top of that: https://stackoverflow.com/a/77289725
ALTER DATABASE ravelry_enhancer OWNER TO ravelry_enhancer;
```

## Set up the venv

```
python3.12 -m venv .venv
.venv/bin/pip install -r requirements/local.txt
echo "export DJANGO_READ_DOT_ENV_FILE=True" >> .venv/bin/activate
echo "export DJANGO_SETTINGS_MODULE=local" >> .venv/bin/activate
source .venv/bin/activate
```

## Check Django set up

```
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```


## Set up the git repo and push to GitHub
```
pre-commit install
git commit -m "Initial project set up from cookiecutter"
git branch -M main
git remote add origin git@github.com:leslem/ravelry_enhancer.git
git push -u origin main
```
