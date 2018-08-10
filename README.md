## Introduction

dashboard is the Open-Falcon unified default forntend component, including:

- user-defined dashboard and screen.
- configure managent of alerting, hostgroup, template. 
- alerting history managent and display.
- team management.
- combine the multiple alerting.
- user management, such as login, logout, register, ldap_login, etc.


## Clone & Prepare
```
export HOME=/home/work/

mkdir -p $HOME/open-falcon/
cd $HOME/open-falcon && git clone https://github.com/open-falcon/dashboard.git
cd dashboard;

```

## Install dependency

- **CentOS**

```
yum install -y python-virtualenv
yum install -y python-devel
yum install -y openldap-devel
yum install -y mysql-devel
yum groupinstall "Development tools"


cd $HOME/open-falcon/dashboard/
virtualenv ./env

./env/bin/pip install -r pip_requirements.txt
```

- **Ubuntu**

```
apt-get install -y python-virtualenv
apt-get install -y slapd ldap-utils
apt-get install -y libmysqld-dev
apt-get install -y build-essential
apt-get install -y python-dev libldap2-dev libsasl2-dev libssl-dev

cd $HOME/open-falcon/dashboard/
virtualenv ./env

./env/bin/pip install -r pip_requirements.txt
```

## Init database
```
cd /tmp/ && git clone https://github.com/open-falcon/falcon-plus.git 
cd /tmp/falcon-plus/scripts/mysql/db_schema/
mysql -h 127.0.0.1 -u root -p < uic-db-schema.sql
mysql -h 127.0.0.1 -u root -p < portal-db-schema.sql
mysql -h 127.0.0.1 -u root -p < graph-db-schema.sql
mysql -h 127.0.0.1 -u root -p < dashboard-db-schema.sql
mysql -h 127.0.0.1 -u root -p < alarms-db-schema.sql
rm -rf /tmp/falcon-plus/
```


## Configure
    dashboard config file is 'rrd/config.py', change it if necessary.

    ## set API_ADDR to your falcon-plus api modules addr, default value as bellow:
    API_ADDR = "http://127.0.0.1:8080/api/v1" 

    ## set PORTAL_DB_* if necessary, default mysql user is root, default passwd is ""
    ## set ALARM_DB_* if necessary, default mysql user is root, default passwd is ""
    ## if following error msg occurred, please check DB config in rrd/config.py
    
    Error 'NoneType' object has no attribute 'cursor'

## Start in debug mode

    $ ./env/bin/python wsgi.py

    open http://127.0.0.1:8081 in your browser.


## Run with gunicorn in production mode

    $ bash control start

    open http://127.0.0.1:8081 in your browser.


## Stop gunicorn

    $ bash control stop

## Check log

    $ bash control tail
