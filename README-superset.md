# Superset <https://superset.apache.org/docs/installation/pypi/#python-virtual-environment>

## Install superset dependencies <https://superset.apache.org/docs/installation/pypi/>

sudo apt update
sudo apt install build-essential libssl-dev libffi-dev python3-dev python3-pip libsasl2-dev libldap2-dev default-libmysqlclient-dev

sudo nano ~/.bashrc
    export FLASK_APP=superset
    export PATH=$PATH:$FLINK_HOME/bin:$KAFKA_HOME/bin:$PINOT_HOME/bin:$HOME/.local/bin

source ~/.bashrc

## Start Pinot

### Start Pinot Zookeeper / Controller / Broker / Server

echo $PINOT_HOME
    /home/christseng/pinot

pinot-admin.sh StartZookeeper -zkPort 2191 -dataDir ~/PinotData/PinotAdmin/zkData> ./zookeeper-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
pinot-admin.sh StartController -zkAddress [::1]:2191 -controllerPort 9000 -dataDir ~/PinotData/data/PinotController > ./controller-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200  -Xloggc:gc-pinot-broker.log"
pinot-admin.sh StartBroker -zkAddress [::1]:2191 > ./broker-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
pinot-admin.sh StartServer -zkAddress [::1]:2191 -dataDir ~/PinotData/data/pinotServerData -segmentDir ~/PinotData/data/pinotSegments > ./server-console.log 2>&1 &

### Pinot ui

<http://localhost:9000/#/>

### Install Python virtual environment

sudo apt install python3.10-venv -y

// Create superset virtual environment
python3 -m venv superset
ls superset -l

/// Activate superset virtual environment
source superset/bin/activate

    (superset) christseng@Chris-SP8:/mnt/d/development/Real_Time_Analysis$

### Install MySQL client connector

sudo apt install mysql-client mysql-client-core-8.0 -y
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential -y

mysql --version
export MYSQLCLIENT_CFLAGS=`mysql_config --cflags`
export MYSQLCLIENT_LDFLAGS=`mysql_config --libs`

echo $MYSQLCLIENT_CFLAGS
    -I/usr/include/mysql

echo $MYSQLCLIENT_LDFLAGS
    -L/usr/lib/x86_64-linux-gnu -lmysqlclient -lzstd -lssl -lcrypto -lresolv -lm

pip install mysqlclient

// Connect to MySQL String
mysql://root:passWord@localhost:3306/analytics

### Install superset and Pinot connector for superset

echo $FLASK_APP
    superset

pip install --upgrade pip
pip install Pillow
pip install wheel apache-superset

### Superset Secret Key

SUPERSET_KEY="$(openssl rand -base64 42)"
echo "SECRET_KEY='$SUPERSET_KEY'" > superset_config.py
cat superset_config.py
    SECRET_KEY='ZIrQI7eOM8VIRfIBhk6QW4IXNFLlTd4QNvMhdW3+ZUqByhZ1fUbslEhZ'

export SUPERSET_CONFIG_PATH=/mnt/d/development/Real_Time_Analysis/superset_config.py
cat $SUPERSET_CONFIG_PATH
    SECRET_KEY='ZIrQI7eOM8VIRfIBhk6QW4IXNFLlTd4QNvMhdW3+ZUqByhZ1fUbslEhZ'

### Superset Pinot

pip install pinotdb
superset db upgrade

### Initialize Superset

superset fab create-admin
    Username [admin]: admin
    User first name [admin]: Chris
    User last name [user]: Tseng
    Email [admin@fab.org]: xxxx@gmail.com
    Password:
    Repeat for confirmation:

    Recognized Database Authentications.
    Admin User admin created.

ls ~/.superset
    superset.db

superset load_examples
superset init

### Start superset

superset run -p 8188 --with-threads --reload --debugger
<http://localhost:8188/superset/welcome/>

### Superset with Pinot

<https://superset.apache.org/docs/configuration/databases/>
Superset Console => Settings => Database Connections => +DATABASE => Connect Database => Apache Pinot =>
    SQLALCHEMY URI (pinot://localhost:8099/query?server=http://localhost:9000/) =>
    Test Connection => Connect

Superset Console => SQL => SQL Lab => DATABASE (Apache Pinot) => SCHEME (default) => TABLE (rides_enriched) => SELECT * from rides_enriched => RUN

Superset Console => Datasets => +DATASET => DATABASE (Apache Pinot) => SCHEMA (default) => TABLE (rides_enriched) => CREATE DATASET AND CREATE CHART

Superset Console => Datasets => +DATASET => rides_enriched => SQL => SQL Lab =>
    SELECT * FROM rides_enriched; => RUN
    SELECT count(*) FROM rides_enriched; => RUN

### Superset with MySQL

<https://superset.apache.org/docs/configuration/databases/>
Superset Console => Settings => Database Connections => +DATABASE => Database Connection => +DATABASE => MySQL =>
    SQLALCHEMY URI (mysql://root:passWord@localhost:3306/analytics) => CONNECT

Superset Console => SQL => SQL Lab => DATABASE (MySQL) => SCHEME (analytics) => TABLE (Location) => SELECT * from Location => RUN

Superset Console => Datasets => +DATASET => DATABASE (MySQL) => SCHEMA (analytics) => TABLE (Location) => CREATE DATASET AND CREATE CHART

### Superset Dashboards

Superset Console => Datasets => rides_enriched => SQL => SQL Lab =>
    SQL statements below => RUN => Save (name of the Dataset) => SAVE & EXPLORE

// Find a breakdown at City level for total Rides
select count(1),city from rides_enriched where ride_status!='Cancelled' group by city

// Find a breakdown of ride status
select count(1),ride_status from rides_enriched group by ride_status

// Find a breakdown of vehicle type
select count(1),vehicle_type from rides_enriched group by vehicle_type

// Find a breakdown of rides taken based on membership
select count(1),membership_status from rides_enriched ride_status!='Cancelled' group by membership_status

// Find the Total revenue in last 1 hour
select sum(amount) from rides_enriched ride_status!='Cancelled'

// Find average revenue per user in last 1 hour
select avg(amount) from rides_enriched ride_status!='Cancelled'

### Restart Superset after Installation

source ~/.bashrc
// Start Kafka
KAFKA_CLUSTER_ID="$($KAFKA_HOME/bin/kafka-storage.sh random-uuid)"
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c $KAFKA_HOME/config/kraft/server.properties

kafka-server-start.sh -daemon $KAFKA_HOME/config/kraft/server.properties

kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic riders
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic drivers
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides_enriched
kafka-topics.sh --bootstrap-server [::1]:9092 --list

// Start Flink
start-cluster.sh
<http://localhost:8081>

// Start Pinot Zookeeper / Controller / Broker / Server
pinot-admin.sh StartZookeeper -zkPort 2191 -dataDir ~/PinotData/PinotAdmin/zkData> ./zookeeper-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
pinot-admin.sh StartController -zkAddress [::1]:2191 -controllerPort 9000 -dataDir ~/PinotData/data/PinotController > ./controller-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200  -Xloggc:gc-pinot-broker.log"
pinot-admin.sh StartBroker -zkAddress [::1]:2191 > ./broker-console.log 2>&1 &

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
pinot-admin.sh StartServer -zkAddress [::1]:2191 -dataDir ~/PinotData/data/pinotServerData -segmentDir ~/PinotData/data/pinotSegments > ./server-console.log 2>&1 &
  
<http://localhost:9000/#/>

// Start Superset Virtual Environment
source superset/bin/activate

echo $FLASK_APP
    superset

which superset
    /mnt/d/development/Real_Time_Analysis/superset/bin/superset

export SUPERSET_CONFIG_PATH=/mnt/d/development/Real_Time_Analysis/superset_config.py
superset run -p 8188 --with-threads --reload --debugger
<http://localhost:8188/superset/welcome/>

### Stop Superset, Pinot, Flink, Kafka

deactivate
stop-cluster.sh
pinot-admin.sh StopProcess -controller -broker -server
kafka-server-stop.sh
zookeeper-server-stop.sh

### Updating Superset Manually

pip install apache-superset --upgrade
superset db upgrade
superset init

<https://www.tutorialspoint.com/>

### Superset Windows 11

mkdir D:\superset
cd /d D:\superset

// Check Versions
python --version
pip --version
systeminfo | findstr /C:"OS"

    OS Name:                       Microsoft Windows 11 Pro
    OS Version:                    10.0.26120 N/A Build 26120
    OS Manufacturer:               Microsoft Corporation
    OS Configuration:              Standalone Workstation
    OS Build Type:                 Multiprocessor Free
    BIOS Version:                  Microsoft Corporation 25.100.143, 12/7/2023

// Upgrade Setuptools & PIP
pip install --upgrade setuptools pip

// Create Virtual Environment named venv & Activate Virtual Environment
python -m venv venv
venv\Scripts\activate

// Install Superset
pip install setuptools
pip install apache-superset

// Install DB Drivers - Postgres & MS SQL
pip install psycopg2
pip install pymssql

:: Open Scripts folder to do superset related stuff
cd venv\Scripts

:: Create application database
python superset db upgrade

:: Create admin user
set FLASK_APP=superset
flask fab create-admin

:: Load some data to play with (optional)
python superset load_examples

:: Create default roles and permissions
python superset init

:: Start web server on port 8088
python superset run -p 8088 --with-threads --reload --debugger

https://www.tutorialspoint.com/
