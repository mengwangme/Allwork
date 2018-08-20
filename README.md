# Allwork


Allwork is a job marketplace. 

Job can be created by project owner and freelancers can apply to the job. 

The idea from [Upwork](https://www.upwork.com/).


## Project setup

```
$ cd allwork
$ sudo pip install docker-compose
$ docker-compose up --build
$ docker-compose exec app python manage.py makemigrations
$ docker-compose exec app python manage.py migrate
```