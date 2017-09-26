# django-admin-skeleton

## Installation de l'environnement

1. Installer Python 2.7 [Python](https://www.python.org/downloads/)
2. Installer le gestionnaire de dépendances pip [PIP](https://pip.pypa.io/en/stable/installing/) 
3. Installer mysql [MySQL](http://dev.mysql.com/downloads/mysql/)
4. Installer le connecteur mysql: [mysql connecteur](http://www.codegood.com/download/10/) la version 32b: MySQL-python-1.2.3.win32-py2.7.exe
5. Installer le compiler C++ pour python [c++ compiler](http://aka.ms/vcpython27)
6. Installer Git [Git](https://git-scm.com/) et créer/associer sa clé [ssh](https://help.github.com/articles/generating-ssh-keys/)
7. Pour la traduction des messages [i18n](https://docs.djangoproject.com/fr/1.8/topics/i18n/translation/#gettext-on-windows)



## Installation des dépendances python

Depuis le projet exécuter les commandes suivantes:
Installer les dépendances python

```shell
pip install -r requirements.txt
```


## Configuration
Configurer la base de données (configuré sur mysql dans le projet)

```python
settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_template',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
     },
}
```

Créer la base de données mysql

```shell
$mysql -uroot -p
mysql>create database django_template;
```

## Développement

Pour initialiser la base de données (générer les tables et l'utilisateur admin)

```shell
python manage.py makemigrations
python manage.py migrate
python manage.py syncdb
```


## Exécution 

Pour lancer le serveur de développement

```shell
python manage.py runserver
```


## Pour traduire un message
Par exemple, si votre application Django contient une chaîne à traduire pour le texte "Welcome to my site.", comme ceci :

```python
_("Welcome to my site.")
```
alors **django-admin makemessages** créera un fichier .po contenant l’extrait (message) suivant :

```python
#: path/to/python/module.py:23
msgid "Welcome to my site."
msgstr ""
```

Pour compiler les messages

```python
django-admin compilemessages
```

## Documentation
Le tutoriel pour créer sa première application
https://docs.djangoproject.com/fr/1.8/intro/tutorial01/

Le lien général de la documentation 
https://docs.djangoproject.com/fr/1.8/

Documentation sur la partie administration 
https://docs.djangoproject.com/fr/1.8/#the-admin

Pour les féniants qui comprennent l'anglais
https://www.youtube.com/watch?v=EuOJRop5aBE&feature=youtu.be


### Composants utilisés

[Django salmonella](https://django-salmonella.readthedocs.org/en/latest/) 

[Django autocomplete-light](http://django-autocomplete-light.readthedocs.org/en/master/) 

[Django suit](http://djangosuit.com/)



## Installation Linux

### Installation de Java et apache

```shell
sudo apt-get install openjdk-7-jdk
sudo apt-get install apache2
```

### Installation des dépendances système

```shell
sudo apt-get install python-pip
sudo apt-get build-dep python-mysqldb
sudo apt-get install libmysqlclient-dev
apt-get install libapache2-mod-wsgi
```

### Installation du virtualenv dev
```shell
pip install virtualenvwrapper
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv django-template
workon django-template
pip install -r requirements.txt
```

## Installation du virtualenv prod
```shell
apt-get install python-pip python-virtualenv
cd /var/www/django_template/mysite
virtualenv env_mysite
source env_mysite/bin/activate
env_mysite/bin/pip install -r requirements.txt
(env_mysite) root@vps312524:/var/www/django_template/mysite# python manage.py migrate
(env_mysite) root@vps312524:/var/www/django_template/mysite# python manage.py createsuperuser
```

### Installation apache
```shell
apt-get install apache2
apt-get install libapache2-mod-wsgi
```
Dans /etc/apache2/site-enabled faire le lien sur le fichier de conf apache du projet
```shell
ln -s /var/www/django-template/mysite/mysite.conf mysite.conf
```


### Mise à jour de l'application en production
Sur __un poste de développement à jour__: générer l'archive de mise à jour contenant les sources (.pyc)
```shell
python make_archive.py
```


Sur __la production__ : pour mettre à jour l'application (utilisera le zip avec la date la plus récente)
```shell
python update.py
```


## Multi-tenant
### Principe
Quand l'utilisateur n'est pas connecté, toutes les requêtes sont faites sur le schéma par défaut.

Une table **DomainGroup** contenant username/tenantName est lue lors de la connexion d'un utilisateur (table présente sur le tenant par défaut).

Une fois connecté, toutes les requêtes sont redirigées sur le tenant de l'utilisateur

### Activation mode schéma 
Changer le moteur BDD utilisé dans **dev_settings.py** et/ou **prod_settings.py** pour gérer le swith dynamique des schémas.
```python
#'ENGINE': 'django.db.backends.mysql',
#'NAME': 'django_template',
'ENGINE': 'db_multitenant.db.backends.mysql',
'NAME': 'tenant_devnull',
```

Activer l'application *"tenant"* qui ajoute la table **DomainGroup** et gère les signals pour maintenir sa mise à jour entre tous les tenants
```python
INSTALLED_APPS = (
    ...
    "tenant",
    ...    
)
```

Activer le Middleware dans **settings.py** qui redirigera les requêtes sur le bon tenant
```python
MIDDLEWARE_CLASSES = (
    'db_multitenant.middleware.MultiTenantSchemaMiddleware',
) + MIDDLEWARE_CLASSES
```

Toujours dans **settings.py**: Si nécessaire, vous pouvez modifier le nom de la BDD public par défaut
```python
MULTI_TENANT_MODE = 'SCHEMA'
DEFAULT_TENANT_NAME = 'devnull'
```

En mode multi-tenant, tous les schémas sont préfixés de **tenant_** (y compris le tenant public. cf:*tenant_devnull*) 

### Management commands
Pour utiliser les commandes de management (makemigrations, migrate, createsuperuser ...), il faut définir la variable d'environnement **TENANT_DATABASE_NAME**

Pour Windows:
```shell
set TENANT_DATABASE_NAME=tenant_devnull&& python ./manage.py migrate
```

Pour Linux et Mac:
```shell
TENANT_DATABASE_NAME=tenant_devnull ./manage.py migrate
```

### Mettre en service un nouveau tenant

Créer le nouveau schéma et son admin
```shell
mysql > create database tenant_monclient1;
mysql > use tenant_devnull;
mysql > insert into tenant_domaingroup(username, tenantName) values('admin1','monclient1');
```

```shell
$ TENANT_DATABASE_NAME=tenant_monclient1 ./manage.py migrate
$ TENANT_DATABASE_NAME=tenant_monclient1 ./manage.py createsuperuser --username=admin1
```


### Activation mode database
Il faut définir toutes les databases (1 client par database) dans **dev_settings.py** et/ou **prod_settings.py** pour gérer le swith dynamique des databases.

**Attention: 'default' est la connexion qui contient la liste des tenants DomainGroup**

```python
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'devnull',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
     },
    'client1': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'client1_app',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    },
```

Activer l'application *"tenant"* qui ajoute la table **DomainGroup** et gère les signals pour maintenir sa mise à jour entre tous les tenants
```python
INSTALLED_APPS = (
    ...
    "tenant",
    ...    
)
```

Activer le Middleware dans **settings.py** qui redirigera les requêtes sur le bon tenant
```python
MIDDLEWARE_CLASSES = (
    'db_multitenant.middleware.MultiTenantDatabaseMiddleware',
) + MIDDLEWARE_CLASSES
```

Toujours dans **settings.py**: Définir la BDD public par défaut et sélectionne le mode 'DATABASE' et activer le **DATABASE_ROUTER**
```python
MULTI_TENANT_MODE = 'DATABASE'
DEFAULT_TENANT_NAME = 'default' # Attention: c'est le nom de la base par défaut

DATABASE_ROUTERS = ['db_multitenant.router.DatabaseRouter']
```

Dans ce mode de multi-tenant, on utilise le nom de la connexion plutôt que le nom de schéma 

### Management commands
Dans ce mode, la commande migrate synchronise une seule base à la fois (par défaut: default).
Il faut spécifier la base à synchroniser avec l'option *--database* pour chaque tenant

``` 
$ ./manage.py migrate
$ ./manage.py migrate --database=client1
```

### Limitation
- Le multi-tenant mode schema n'a été mis en place que pour Mysql (il faut créer et adapté un nouveau base.py pour chaque nouvelle BDD supportée)
- Lors de la création d'un utilisateur la table **DomainGroup** du schéma public est mise à jour **avec des queries spécifiques mysql**
- L'ajout d'un nouveau tenant en mode multi-tenant database nécessite un redémarrage de l'application 

### Source   
Le mécanisme mis en place s'inpire du projet ci-contre: 

https://github.com/mik3y/django-db-multitenant

https://fhbash.wordpress.com/2013/08/02/howto-django-one-database-for-auth-and-each-user-connect-to-different-database/

https://docs.djangoproject.com/fr/1.9/topics/db/multi-db/



# Docker déploiement

## 1. build du Dockerfile
  ```shell
docker build -t django-mysite .
  ```

## Importer/exporter une image sur un serveur
  ```shell
  docker save django-mysite > django-mysite.tar
  docker load < django-mysite.tar
```

## 2. création du container de base de données mysql
```shell
# Run Mysql
docker run --name db_mysite --restart=always -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=django_template -v /home/tony/django-template/daily_backup/:/root/backup_mysql -d mysql:5.5.47 --character-set-server=utf8 --collation-server=utf8_unicode_ci

# Run mysite service
docker run -it -d -P --restart=always --name django-mysite -e ADMIN_USER=tony -e ADMIN_PWD=tony --link db_mysite:db_mysite -p 80:80 -v /home/tony/django-template/:/var/www/django-template django-mysite

# Connect to container
docker exec -it django-mysite bash

# See startup logs
docker logs --follow django-mysite
```

# Mise en place du cron de backup journalier du Mysql
Dans /etc/crontab
```
  0  1  *  *  * root docker exec -it db_mysite /root/backup_mysql/backup_mysql.sh
```

# Mettre à jour le service
Déposer le tar dans mysite/
```shell
docker exec -it django-mysite /var/www/mysite/update.py
```

**Configure a custom DNS server to add on each docker container run**

/etc/default/docker

uncomment and and your company DNS:

```shell
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"
```