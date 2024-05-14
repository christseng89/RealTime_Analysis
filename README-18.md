# 18. Using Event Time Temporal Joins and Lookup Joins to Enrich Ride Data: Hands On (2_flink_table_data)

## 1 Start Kafka Server

cd kafka_2.12-3.5.2
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/kraft/server.properties
    Formatting /tmp/kraft-combined-logs with metadata.version 3.5-IV2.
bin/kafka-server-start.sh -daemon config/kraft/server.properties
ps -ef | grep kafka

bin/kafka-topics.sh --create --topic rides --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic riders --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic drivers --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092
bin/kafka-topics.sh --create --topic rides_enriched --partitions 3 --replication-factor 1 --bootstrap-server [::1]:9092 
bin/kafka-topics.sh --bootstrap-server [::1]:9092 --list

### 2 Start Flink Server

cd flink-1.17.2
./bin/start-cluster.sh
    Starting cluster.
    Starting standalonesession daemon on host Chris-SP8.
    Starting taskexecutor daemon on host Chris-SP8.

### 3 Command to Create Group

cd ../kafka_2.12-3.5.2
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides --group rides-flink-consumer

bin/kafka-consumer-groups.sh --bootstrap-server [::1]:9092 --describe --group rides-flink-consumer
    GROUP                TOPIC           PARTITION  CURRENT-OFFSET  LOG-END-OFFSET  LAG             CONSUMER-ID  
    rides-flink-consumer rides           0          0               0               0               -               -
    rides-flink-consumer rides           1          0               0               0               -               -
    rides-flink-consumer rides           2          0               0               0               -               -

### 4 Query Kafka Topics

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides --group rides-flink-consumer

bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

{ "ride_id":"000001"}@@@{"ride_id": "000001","rider_id": "100001","driver_id": "200001","location_id": "300001","amount": 350,"ride_status": "Booked","start_lat" : 12.990707,"start_lng" : 77.570870,"dest_lat": 12.887725, "dest_lng": 77.560973}

### 5 Run the RideEnrichExample in IntelliJ & 6 Query the rides_enriched topic

// Run the RideEnrichExample from the IDE
bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --property print.key=true 
// Not working here ... but works in the IDE

### 6 Input Data for Riders -> Drivers -> Rides

bin/kafka-console-producer.sh --topic riders --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

{"rider_id":"100001"}@@@{"name":"XYZ", "membership_status": "member", "last_updated_at":"2024-01-13 11:00:00","rider_id":"100001"}
{"rider_id":"100002"}@@@{"name":"ZYX", "membership_status": "member", "last_updated_at":"2024-01-13 11:00:00","rider_id":"100002"}
{"rider_id":"100003"}@@@{"name":"YYY", "membership_status": "not a member", "last_updated_at":"2024-01-13 13:00:00","rider_id":"100003"}
{"rider_id":"100004"}@@@{"name":"ZZZ", "membership_status": "not a member", "last_updated_at":"2024-01-13 13:00:00","rider_id":"100004"}

bin/kafka-console-producer.sh --topic drivers --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

{"driver_id":"200001"}@@@{"name":"ABCD", "vehicle_type": "Sedan", "last_updated_at":"2024-01-13 11:00:00","driver_id":"200001"}
{"driver_id":"200002"}@@@{"name":"BCDA", "vehicle_type": "SUV", "last_updated_at":"2024-01-13 11:00:00","driver_id":"200002"}
{"driver_id":"200003"}@@@{"name":"CDDA", "vehicle_type": "Hatchback", "last_updated_at":"2024-01-13 13:00:00","driver_id":"200003"}
{"driver_id":"200004"}@@@{"name":"DCBA", "vehicle_type": "Sedan", "last_updated_at":"2024-01-13 13:00:00","driver_id":"200004"}

bin/kafka-console-producer.sh --topic rides --bootstrap-server [::1]:9092 --property "parse.key=true" --property "key.separator=@@@"

// Run the RideEnrichExample from the IDE AGAIN

### 7 Query the rides_enriched topic again (not working)

bin/kafka-console-consumer.sh --bootstrap-server [::1]:9092 --topic rides_enriched --property print.key=true
