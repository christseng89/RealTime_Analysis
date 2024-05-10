package org.example;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

public class TableAPIExample {
  public static void main(String[] args) throws Exception {
    StreamExecutionEnvironment env =
        StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);

    tableEnv.executeSql(
        "CREATE TABLE RideTest (\n"
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

    Table outputTable = tableEnv.sqlQuery("select * from RideTest");
    DataStream<Row> outputStream = tableEnv.toDataStream(outputTable);
    outputStream.print();
    env.execute();
  }
}
