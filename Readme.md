
# Coders-HQ Backend

This repository holds the Coders-HQ backend. It is made using [Django](https://www.djangoproject.com/) and [Postgres](https://www.postgresql.org/) as an API backend to the Coders-HQ frontend (based on [React](https://reactjs.org/)) which is hosted on another repository.

## Architecture

The front-end will be located in its own repository which can connect to django's REST framework. The REST framework makes it easy to integrate any frontend to django's API which makes it possible to work on the front and backend separately. The final architecture should look something like this.

```
├──chq_frontend
| ├──public/
| ├──src/
| ├──Dockerfile          
| ├──package.json
| └──package-lock.json
├──chq_backend
| ├──chq_backend/
| ├──media/
| ├──static/
| ├──Dockerfile         
| ├──entrypoint.sh      // bash entrypoint for django to run commands before running the server
| ├──manage.py          
| ├──requirements.txt
| └──settings.ini
└──docker-compose.yaml  //for running multi-conatiner application
```

__Currently the docker-compose.yml is located inside this repository but will eventually be pulled out top integrate the frontend with the backend.__

## Database

Django should be connected to postgres (postgres can be installed locally or using docker) but there is an option to use sqlite for development. Although sqlite should not be used for release. To switch between sqlite or postgres change `DATABASES = ...` in settings.py

Docker makes it easy to set up postgres. The docker-compose.yaml file creates and connects the two containers (django+postgres) together, you can also create postgres by itself and connect to django which you build locally.

## Building

### Pre requisites

1.  python 3
1.  Pip
3.  (optional) pipenv
2.  (Optional) docker

### Building locally

1.  Run `pip install -r requirements.txt`
1.  Make sure you have the correct Database in the settings.py
1.  Run `python manage.py runserver 0.0.0.0:33325`
1.  On a web browser open localhost:33325

### Building on Docker

1.  make sure you have the correct Database in settings.py
3.  Run `docker-compose up` in root dir and it will create the django and postgres apps, it will also run the web app
1.  On a web browser open localhost:33325
