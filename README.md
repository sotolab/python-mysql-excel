## Install

Install packages with pip: -r requirements.txt

```shell
$ pip install -r requirements.txt
```

### Config

Config.json

```config.json

{
    "productCode": "main-123-110",
    "projectName": "MyProject",
    "version": "230120",
    "hostName": "localhost",
    "hostPort": 3306 ,
    "userName": "youruser",
    "passWord": "yourpw!",
    "databaseName": "your_db"    
}

```
### Create the Database

Run MySQL command line

``` mysql
# mysql >
# mysql > create database your_db character set utf8mb4 collate utf8mb4_general_ci;
# mysql > create user 'youruser'@'localhost' identified by 'yourpw!';
# mysql > GRANT ALL privileges ON your_db.* TO  'youruser'@'localhost' ;
# mysql > flush privileges;
# mysql > exit;

```

### Starting the python

python 

``` shell
$ python main.py
```

