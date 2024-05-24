# Superset <https://superset.apache.org/docs/installation/pypi/#python-virtual-environment>

## Install superset dependencies <https://superset.apache.org/docs/installation/pypi/>

sudo apt update
sudo apt install build-essential libssl-dev libffi-dev python3-dev python3-pip libsasl2-dev libldap2-dev default-libmysqlclient-dev

sudo nano ~/.bashrc
    export FLASK_APP=superset
    export PATH=$PATH:$FLINK_HOME/bin:$KAFKA_HOME/bin:$PINOT_HOME/bin:$HOME/.local/bin

source ~/.bashrc

sudo apt install python3.10-venv -y

// One time setup with 2 lines
python3 -m venv superset
source superset/bin/activate

    (superset) christseng@Chris-SP8:/mnt/d/development/Real_Time_Analysis$

### Install superset and Pinot connector for superset

echo $FLASK_APP

pip install --upgrade pip
pip install wheel apache-superset

which superset
    /home/christseng/.local/bin/superset
echo $FLASK_APP
    superset

### Superset Secret Key

SUPERSET_KEY="$(openssl rand -base64 42)"
echo "SECRET_KEY='$SUPERSET_KEY'" > superset_config.py
cat superset_config.py
    SECRET_KEY='ZIrQI7eOM8VIRfIBhk6QW4IXNFLlTd4QNvMhdW3+ZUqByhZ1fUbslEhZ'

export SUPERSET_CONFIG_PATH=/mnt/d/development/Real_Time_Analysis/superset_config.py
cat $SUPERSET_CONFIG_PATH
    SECRET_KEY='ZIrQI7eOM8VIRfIBhk6QW4IXNFLlTd4QNvMhdW3+ZUqByhZ1fUbslEhZ'

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

pip install pinotdb
superset db upgrade
superset init

### Start superset

superset run -p 8188 --with-threads --reload --debugger
<http://localhost:8188/superset/welcome/>

### Superset with Pinot <https://superset.apache.org/docs/configuration/databases/>

Superset Console => + => Data => Connect Database => Apache Pinot =>
    SQLALCHEMY URI (pinot://localhost:8099/query?server=http://localhost:9000/) =>
    Test Connection => Connect

Superset Console => Datasets => + DATASET => => DATABASE (Apache Pinot) => TABLE (rides_enriched) =>
CREATE DATASET AND CREATE CHART

Superset Console => Datasets => rides_enriched => SQL => SQL Lab =>
    SELECT * FROM rides_enriched; => RUN
    SELECT count(*) FROM rides_enriched; => RUN

### Superset Dashboards

Superset Console => Datasets => rides_enriched => SQL => SQL Lab =>
    SQL statements below => RUN => Save (name of the Dataset) => SAVE & EXPLORE
S
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

deactivate
stop-cluster.sh
kafka-server-stop.sh
zookeeper-server-stop.sh
