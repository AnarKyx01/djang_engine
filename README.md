# djang_engine

This is a quiz/ctf engine to support continuous training, very early stages of development

```bash
### Django Requirements
sudo su
apt-get update
apt-get install python3-pip python3-dev libpq-dev
pip3 install --upgrade pip
pip3 install django

### Postgresql Requirements
sudo su
apt-get install postgresql postgresql-contrib
pip3 install psycopg2
```

Dependencies: 
  - django (https://docs.djangoproject.com/en/1.10/intro/install/)

Notes:
  Currently configured with sqlite with default information; recommend using postgresql over sqlite

TODO: create readme
