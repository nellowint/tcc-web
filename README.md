# tcc-web

Este repositório foi criado para gerenciar o app tcc-web no desenvolvimento do Trabalho de Conclusão de Curso de Tecnologia em Análise e Desenvolvimento de Sistemas.

## tcc

Este app foi desenvolvido em python utilizando o framework django e uso do SGBD MySQL Community Server.

### Pré-requisitos

```
Django~=1.11.0
djangorestframework
mysqlclient
Pillow
```

#### Instalação e Configuração

##### Ambiente Virtual

```
sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
```

##### Instalação pré-requisitos

```
pip install --upgrade pip
pip install -r requirements.txt
```

##### Criação banco de dados

```
CREATE DATABASE tcc CHARACTER SET utf8;
CREATE USER 'tcc'@'localhost' identified by '1234';
GRANT ALL PRIVILEGES ON tcc.* TO 'tcc'@'localhost';
FLUSH PRIVILEGES;
```

#### Migração dos comandos SQL do app

```
python manage.py makemigrations tcc
python manage.py migrate tcc
python manage.py migrate
python manage.py createsuperuser
```

##### Run

```
python manage.py runserver
```

*** 

2018 - @vieirateam