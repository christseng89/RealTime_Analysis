package org.example;

import org.apache.flink.configuration.CheckpointingOptions;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.CheckpointConfig;
import org.apache.flink.streaming.api.environment.ExecutionCheckpointingOptions;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.TableConfig;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

// https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/upsert-kafka/
public class RideEnrichSimple {
  public static void main(String[] args) throws Exception {
    StreamExecutionEnvironment executionEnv =
      StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnv =
      StreamTableEnvironment.create(executionEnv);

    executionEnv.enableCheckpointing(1000);
    executionEnv.getCheckpointConfig().setExternalizedCheckpointCleanup(
      CheckpointConfig.ExternalizedCheckpointCleanup.RETAIN_ON_CANCELLATION);
    Configuration config = new Configuration();
    config.set(
      ExecutionCheckpointingOptions.ENABLE_CHECKPOINTS_AFTER_TASKS_FINISH,
      true);
    config.set(CheckpointingOptions.CHECKPOINT_STORAGE, "filesystem");
    config.set(CheckpointingOptions.CHECKPOINTS_DIRECTORY,
      "file:/home/christseng/FlinkData/Rides");
    executionEnv.configure(config);

    TableConfig tableConfig = tableEnv.getConfig();
    tableConfig.set("table.exec.source.idle-timeout", "1s");
    tableConfig.set("table.local-time-zone", "UTC");

    tableEnv.executeSql("CREATE TABLE Rides (\n"
      + "  `ride_id` STRING,\n"
      + "  `rider_id` STRING,\n"
      + "  `driver_id` STRING,\n"
      + "  `location_id` STRING,\n"
      + "  `amount` FLOAT,\n"
      + "  `ride_status` STRING,\n"
      + "  `start_lat` FLOAT,\n"
      + "  `start_lng` FLOAT,\n"
      + "  `dest_lat` FLOAT,\n"
      + "  `dest_lng` FLOAT,\n"
      + "  `request_time` TIMESTAMP(3) METADATA FROM 'timestamp',\n"
      + "  `processing_time` as PROCTIME()\n"
      + ") WITH (\n"
      + "  'connector' = 'kafka',\n"
      + "  'topic' = 'rides',\n"
      + "  'properties.bootstrap.servers' = '[::1]:9092',\n"
      + "  'properties.group.id' = 'test',\n"
      + "  'scan.startup.mode' = 'latest-offset',\n"
      + "  'format' = 'json'\n"
      + ");");
    System.out.println("\nRides table (kafka) created ...");

    tableEnv.executeSql("CREATE TABLE RidesEnriched (\n"
      + "  `rider_id` STRING,\n"
      // + "  `rider_name` STRING,\n"
      + "  `driver_id` STRING,\n"
      // + "  `driver_name` STRING,\n"
      // + "  `vehicle_type` STRING,\n"
      + "  `ride_id` STRING,\n"
      + "  `amount` FLOAT,\n"
      + "  `request_time`  TIMESTAMP_LTZ(3),\n"
      // + "  `membership_status` STRING,\n"
      + "  `city` STRING,\n"
      + "  `country` STRING,\n"
      + "  `ride_status` STRING,\n"
      + "  `start_lat` FLOAT,\n"
      + "  `start_lng` FLOAT,\n"
      + "  `dest_lat` FLOAT,\n"
      + "  `dest_lng` FLOAT,\n"
      + "  PRIMARY KEY(`ride_id`) NOT ENFORCED\n"
      + "  ) WITH (\n"
      + "  'connector' = 'upsert-kafka',\n"
      + "  'topic' = 'rides_enriched',\n"
      + "  'properties.bootstrap.servers' = '[::1]:9092',\n"
      + "  'properties.group.id' = 'testGroup',\n"
      + "  'value.format' = 'json',\n"
      + "  'key.format' = 'json'\n"
      + ");");
    System.out.println("\nRidesEnriched table (upsert) created ...");

    // Lookup Join with JDBC
    tableEnv.executeSql("CREATE TABLE Location (\n"
      + "  location_id STRING,\n"
      + "  city STRING,\n"
      + "  country STRING,\n"
      + "  PRIMARY KEY (location_id) NOT ENFORCED\n"
      + ") WITH (\n"
      + "   'connector' = 'jdbc',\n"
      + "   'driver' = 'com.mysql.cj.jdbc.Driver',\n"
      +
      "   'url' = 'jdbc:mysql://localhost:3306/analytics',\n"
      + "   'table-name' = 'Location',\n"
      + "   'username' = 'root',\n"
      + "   'password' = 'passWord'\n"
      + ");");
    System.out.println("Location table (jdbc) created ...");

    Thread.sleep(10000);
    System.out.println("\nRidesEnriched table (upsert) inserting ...");
    tableEnv.executeSql("INSERT INTO RidesEnriched\n"
      + "SELECT \n"
      + "ride.rider_id,\n"
      // + "r.name as rider_name,\n"
      + "ride.driver_id,\n"
      // + "d.name as driver_name,\n"
      // + "d.vehicle_type,\n"
      + "ride.ride_id,\n"
      + "ride.amount,\n"
      + "ride.request_time,\n"
      // + "r.membership_status,\n"
      + "l.city,\n"
      + "l.country,\n"
      + "ride.ride_status,\n"
      + "ride.start_lat,\n"
      + "ride.start_lng,\n"
      + "ride.dest_lat,\n"
      + "ride.dest_lng\n"
      + "\n"
      + "FROM Rides ride\n"
      + "\n"
      // + "LEFT JOIN Drivers\n"
      // // Temporal join with Event Time
      // + "FOR SYSTEM_TIME AS OF ride.request_time AS d\n"
      // + "On ride.driver_id = d.driver_id\n"
      // + "\n"
      // + "LEFT JOIN Riders\n"
      // // Temporal join with Event Time
      // + "FOR SYSTEM_TIME AS OF ride.request_time AS r\n"
      // + "On ride.rider_id = r.rider_id\n"
      // + "\n"
      + "LEFT JOIN Location\n"
      // Lookup join with Processing Time
      + "FOR SYSTEM_TIME AS OF ride.processing_time as l\n"
      + "On ride.location_id = l.location_id");
    System.out.println("RidesEnriched table (upsert) inserted ...");

    System.out.println("\nQuery RidesEnriched table ...");

    Table table = tableEnv.sqlQuery("select * from RidesEnriched");
    DataStream<Row> changelogStream = tableEnv.toChangelogStream(table);
    changelogStream.print();

    executionEnv.execute("RideEnrichSimple");
  }
}