# WSL Kafka and Flink Running Instructions

## Java 11 (WSL)

source ~/.bashrc
echo $JAVA_HOME
    /usr/bin/java

java --version
    openjdk 11.0.22 2024-01-16
    OpenJDK Runtime Environment (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1)
    OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1, mixed mode, sharing)

## Start up Kafka server (WSL)

cd kafka_2.12-3.5.2
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
    Formatting /tmp/kraft-combined-logs with metadata.version 3.5-IV2.
bin/kafka-server-start.sh -daemon config/kraft/server.properties
ps -ef | grep kafka

### Create Rides/Riders/Drivers/Enriched Rides topics

bin/kafka-topics.sh --create --topic rides --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic riders --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic drivers --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic rides_enriched --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092

bin/kafka-topics.sh --bootstrap-server [::1]:9092 --list
bin/kafka-console-consumer.sh --topic rides --bootstrap-server [::1]:9092 --property "print.key=true"

cd kafka_2.12-3.5.2
bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

    { "ride_id":"000001"}@@@{"ride_id": "000001","rider_id": "100001","driver_id": "200001","location_id": "300001","amount": 350,"ride_status": "In Progress","start_lat" : 12.99070744,"start_lng" : 77.57087025,"dest_lat": 12.88772573, "dest_lng": 77.56097347}

## Start up Flink server (WSL)

echo $FLINK_HOME
    /home/christseng/flink/flink-1.17.2

flink --version
    Version: 1.17.2, Commit ID: c0027e5

$FLINK_HOME/bin/start-cluster.sh
    Starting cluster.
    Starting standalonesession daemon on host Chris-SP8.
    Starting taskexecutor daemon on host Chris-SP8.

$FLINK_HOME/bin/sql-client.sh
ps aux | grep flink
    christs+  586603 50.0 23.6 9174280 2900328 ?     Ssl  17:21  15:33 /usr/bin/java --add-opens java.base/java.lang=ALL-UNNAMED -Dfile.encoding=UTF-8 -classpath /mnt/d/development/Real_Time_Analysis/realtime_analysis/target/classes:/

flink run $FLINK_HOME/examples/streaming/WordCount.jar
tail $FLINK_HOME/log/flink-*-taskexecutor-*.out
    (nymph,1)
    (in,3)
    (thy,1)
    (orisons,1)
    (be,4)
    (all,2)
    (my,1)

## MySQL Server (WSL)

sudo mysql
use analytics;

CREATE TABLE Location (
    location_id varchar(255) NOT NULL,
    city varchar(255),
    country varchar(255),
    PRIMARY KEY (location_id)
);

insert into Location (location_id,city,country) values ('300001','Bengaluru','India');
insert into Location (location_id,city,country) values ('300002','Mumbai','India');
insert into Location (location_id,city,country) values ('300003','New Delhi','India');

show tables;
select * from Location;

## Change MySQL Root Password

sudo mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH caching_sha2_password BY 'passWord';
exit;
mysql -u root -p
    passWord

use analytics;
show tables;
select * from Location;
exit;

## Stop Flink and Kafka Server (WSL)

cd flink-1.17.2
./bin/stop-cluster.sh

cd kafka_2.12-3.5.2
bin/kafka-server-stop.sh
