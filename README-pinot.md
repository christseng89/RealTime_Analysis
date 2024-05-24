# Pinot Courses

## Pinot Overview / Architecture

<https://docs.pinot.apache.org/v/release-1.0.0>
<https://docs.pinot.apache.org/v/release-1.0.0/basics/architecture>

## Pinot Quick Start

<https://docs.pinot.apache.org/v/release-1.0.0/basics/getting-started/running-pinot-locally>

java --version
    openjdk 11.0.22 2024-01-16
    OpenJDK Runtime Environment (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1)
    OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1, mixed mode, sharing)

PINOT_VERSION=1.0.0
wget https://downloads.apache.org/pinot/apache-pinot-$PINOT_VERSION/apache-pinot-$PINOT_VERSION-bin.tar.gz
tar -xvf apache-pinot-$PINOT_VERSION-bin.tar.gz
mv ./apache-pinot-1.0.0-bin ~/pinot

sudo nano ~/.bashrc
    export PINOT_HOME=~/pinot
    export PATH=$PATH:$PINOT_HOME/bin

source ~/.bashrc
echo $PINOT_HOME
mkdir ~/PinotData

### Start Pinot Zookeeper

pinot-admin.sh StartZookeeper -zkPort 2191 -dataDir ~/PinotData/PinotAdmin/zkData> ./zookeeper-console.log 2>&1 &
    [1] 6970

### Start Pinot Controller

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
pinot-admin.sh StartController -zkAddress [::1]:2191 -controllerPort 9000 -dataDir ~/PinotData/data/PinotController > ./controller-console.log 2>&1 &
    [2] 6771

### Start Pinot Broker

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200  -Xloggc:gc-pinot-broker.log"
pinot-admin.sh StartBroker -zkAddress [::1]:2191 > ./broker-console.log 2>&1 &
    [3] 6971

### Start Pinot Server

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
pinot-admin.sh StartServer -zkAddress [::1]:2191 -dataDir ~/PinotData/data/pinotServerData -segmentDir ~/PinotData/data/pinotSegments > ./server-console.log 2>&1 &
    [4] 7136

### Pinot ui

<http://localhost:9000/#/>

## Test Pinot

### Start Kafka Server

KAFKA_CLUSTER_ID="$($KAFKA_HOME/bin/kafka-storage.sh random-uuid)"
kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c $KAFKA_HOME/config/kraft/server.properties

kafka-server-start.sh -daemon $KAFKA_HOME/config/kraft/server.properties

kafka-topics.sh --bootstrap-server [::1]:9092 --list
  rides_enriched
  users
// users and rides_enriched topics will be automatically created by the Pinot Realtime Table

kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic users
kafka-console-producer.sh --bootstrap-server [::1]:9092 --topic users

{"name":"XYZ", "followers": 1, "last_updated_at":"2024-01-13 12:00:00","user_id":"100001"}
{"name":"ZYX", "followers": 2, "last_updated_at":"2024-01-13 12:00:00","user_id":"100002"}
{"name":"YYY", "followers": 3, "last_updated_at":"2024-01-13 14:00:00","user_id":"100003"}
{"name":"ZZZ", "followers": 4, "last_updated_at":"2024-02-14 14:00:00","user_id":"100004"}

### Pinot UI (localhost:9000)

#### Add Schema

Tables => Add Schema

Schema Name: users
Column
    - name / Dimension
    - followers / Metric
    - last_updated_at / DateTime / STRING / SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss
    - user_id / Dimension
=> Save

#### Add Realtime Table

Table Name: users
stream.kafka.broker.list: [::1]:9092
stream.kafka.topic.name: users
=> Save

### Query Console

Tables => users

SELECT sum(followers) FROM users
=> sum(followers) / 10

### Upsert Data

users Schema
{
  ...  
  "primaryKeyColumns": [
    "user_id"
  ]
}

users Table

  ...
  "tenants": {
    "broker": "DefaultTenant",
    "server": "DefaultTenant" //here...
  },
  ...
      "streamConfigs": {
      "streamType": "kafka",
      "stream.kafka.topic.name": "users",
      "stream.kafka.broker.list": "[::1]:9092",
      "stream.kafka.consumer.type": "lowlevel",
      "stream.kafka.consumer.prop.auto.offset.reset": "smallest",
      "stream.kafka.consumer.factory.class.name": "org.apache.pinot.plugin.stream.kafka20.KafkaConsumerFactory",
      "stream.kafka.decoder.class.name": "org.apache.pinot.plugin.stream.kafka.KafkaJSONMessageDecoder",
      "realtime.segment.flush.threshold.rows": "0",
      "realtime.segment.flush.threshold.time": "24h",
      "realtime.segment.flush.threshold.segment.size": "100M",
      "realtime.segment.upsert.enable": "true" // here...
    },  
  ...
  "routing": {
    "segmentPrunerTypes": null,
    "instanceSelectorType": "strictReplicaGroup" // here...
  },
  ...
  "upsertConfig": {
    "mode": "FULL", // here...
    "hashFunction": "NONE",
    "defaultPartialUpsertStrategy": "OVERWRITE",
    "enableSnapshot": false,
    "metadataTTL": 0,
    "enablePreload": false
  },
  ...

### Pinot Swagger REST API

// Schema => Add a new schema => POST => rides_enriched_schema
// Table => Adds a table => POST => rides_enriched_table

### Start Flink Server

start-cluster.sh

### Create Kafka Topics

kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic riders
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic drivers
kafka-topics.sh --create --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 --topic rides_enriched
kafka-topics.sh --bootstrap-server [::1]:9092 --list

### Flink run

cd realtime_analysis/
flink run -c org.example.RideEnrichExample target/realtime-analytics-example-1.0-SNAPSHOT.jar
  ...
  RidesEnriched sink table (upsert) created ...
  RidesEnriched sink table (upsert) inserting ...
  Job has been submitted with JobID 2d68721c81377952394616446ca54d9d
  RidesEnriched sink table (upsert) inserted ...

  Query RidesEnriched sink table ...
  Job has been submitted with JobID 1fc7bb2e4f1f78f3babe1348dd670d6a

kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic drivers
kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic riders
kafka-console-producer.sh --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@" --topic rides

### Stop Pinot <https://docs.pinot.apache.org/operators/cli>

pinot-admin.sh ShowClusterInfo -clusterName PinotCluster -zkAddress localhost:2181
pinot-admin.sh StopProcess -controller -broker -server
