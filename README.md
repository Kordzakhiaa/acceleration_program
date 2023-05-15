# "Acceleration Program" API



## Documentation
For the project documentation **[click here!](https://docs.google.com/document/d/1IAGCr9H1FqD7WHoNg15XPgebvGu7l7iuMGI5bzsaZmk/edit)**

## Project requirements

* docker >= 20.10.14
  ```docker --version```
* docker-compose >= 1.27.4
  ```docker-compose --version```
* python >= 3.8
  This is the case when you start the project without docker-compose

## Development Environment Set Up

### Start project directly on your host

#### Virtual Environment Set up

```bash
  python -m venv <path_to_env>
  source <path_to_env>/bin/activate
```

#### Initialize database

```bash
  python manage.py migrate
```

### Start project using docker-compose [This is preferred way]

#### Build and start containers

This will fetch/build images and start containers. Migration command will be run during startup.

```bash
  docker-compose up --build
```

#### Working with running container

* When container is running

```bash
docker-compose exec web_api <your_command>
```

* Without running container

```bash
docker-compose run --rm web_api <your_command>
```

You can run any command you would run on you host machine...
<your_command> examples:

* python manage.py makemigrations
* python manage.py migrate
* python manage.py startapp <app_name>
* python manage.py createsuperuser
