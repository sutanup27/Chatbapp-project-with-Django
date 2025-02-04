# Django_project

## Django Environment set-up
* Install Python version 3.7.0 or more
* pip should be installed
* install virtual environment 
    ```pip install virtualenvwrapper-win```
* create an virtual environment
    ```mkvirtualenv django_env```
* activate that environment
    ```source django_test/bin/activate ```
* install Django 2.2 or more
    ```pip install django ```
* install django rest-api-framework
    ```pip install djangorestframework```
* install 

## Django channels Environment set-up
* install radis-server to work with django-channels
```sudo apt-get install redis-server```
* install django-channels
```python -m pip install -U channels```
* install channels-redis
```python -m pip install -U channels-redis```

## Installing Mongodb
*install mongodb
```https://docs.mongodb.com/v3.6/installation/```
*check ```mongo``` command on terminal working or not
*check ``` show dbs``` command and how many databases are showing

## start the we server
* Run ```mongod``` command to start mongodb server (if it is ont started yet).
* Run ```service redis-server restart``` to start radis-server (```redis-cli ping``` to check radis working properly or not)
* go to project's ```chatter``` directory where ```manage.py``` resides.
* Run ```python manage.py runserver <hostname>:<portname>``` to run the webserver.( If there is some error you might have missed some installation please complete those and debug the error then proceed)
* In browser type ``` <hostname>:<portname>``` to check the server is working properly or not.
