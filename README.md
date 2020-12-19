
# Coders HQ Backend

![Django Test](https://github.com/ralsuwaidi/CHQ_Backend/workflows/Django%20Test/badge.svg)


This repository holds the Coders-HQ backend. It is made using [Django](https://www.djangoproject.com/) and [Postgres](https://www.postgresql.org/) as an API backend to the Coders-HQ frontend (based on [React](https://reactjs.org/)) which is hosted [in this repo](https://github.com/Coders-HQ/CHQ_Frontend). The main Coders-HQ website is hosted at [codershq.ae](https://codershq.ae).

Table of Contents
=================

<!--ts-->
   * [Coders HQ Backend](#coders-hq-backend)
   * [Table of Contents](#table-of-contents)
      * [Installation](#installation)
         * [Pre requisites](#pre-requisites)
         * [Building locally](#building-locally)
         * [Building on Docker](#building-on-docker)
      * [API](#api)
      * [Architecture](#architecture)
      * [Database](#database)

<!-- Added by: runner, at: Fri Dec 18 18:29:20 UTC 2020 -->

<!--te-->

## Installation

### Pre requisites

1.  python 3
1.  Pip
2.  (Optional) [docker](https://docs.docker.com/get-docker/)
2.  (Optional) httpie

### Building locally

1.  run `pip install -r requirements.txt` in root dir 
1.  run `python manage.py migrate`
1.  run `python manage.py createsuperuser`
1.  run `python manage.py runserver 0.0.0.0:33325`
1.  On a web browser open [localhost:33325](http://localhost33325)

### Building on Docker

3.  Run `docker-compose up` in __root dir__ and it will create the django and postgres apps, it will also run the web app
1.  On a web browser open [localhost:33325](http://localhost33325)

## API

All information related to the API, and how to use it, can be found [here](https://documenter.getpostman.com/view/13659675/TVmJjeuV).

## Architecture

The front-end will be located [in its own repository](https://github.com/Coders-HQ/CHQ_Frontend) which can connect to django's REST framework. The REST framework makes it easy to integrate any frontend to django's API which makes it possible to work on the front and backend separately. The final architecture should look something like this.

```
├──chq_frontend
| ├──public/
| ├──src/
| ├──Dockerfile          
| ├──package.json
| └──package-lock.json
├──CHQ_Backend
| ├──chq_backend/
| ├──users/             // main django app
| ├──Dockerfile         
| ├──entrypoint.sh      // bash entrypoint for django to run commands before running the server
| ├──manage.py          
| ├──requirements.txt
| └──settings.ini
└──docker-compose.yaml  // for running multi-conatiner application
```

__Currently the docker-compose.yml is located inside this repository but will eventually be pulled out top integrate the frontend with the backend.__

## Database

Django should be connected to postgres (postgres can be installed locally or using docker) but there is an option to use sqlite for development. __Sqlite should not be used for release.__ To switch between sqlite or postgres use the [migrate function](https://docs.djangoproject.com/en/3.1/topics/db/multi-db/#synchronizing-your-databases) like so:

```
$ ./manage.py migrate                           // for sqlite
$ ./manage.py migrate --database=postgres       // for postgres (must have an instance of postgres running)
```

Docker makes it easy to set up postgres. The docker-compose.yaml file creates and connects the two containers (django+postgres) together, you can also create postgres by itself and connect to django which you build locally.

