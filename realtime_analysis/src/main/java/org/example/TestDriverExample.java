package org.example;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

public class TestDriverExample {
  public static void main(String[] args) throws Exception {
    final StreamExecutionEnvironment executionEnv =
      StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnv = StreamTableEnvironment.create(executionEnv);

    tableEnv.executeSql(
      "CREATE TABLE DriverTest (\n"
        + "  `driver_id` STRING,\n"
        + "  `name` STRING,\n"
        + "  `vehicle_type` STRING,\n"
        + "  `last_updated_at`  TIMESTAMP(3),\n"
        + "  `request_time` TIMESTAMP(3) METADATA FROM 'timestamp',\n"
        + "  `processing_time` as PROCTIME()\n"
        + ") WITH (\n"
        + "  'connector' = 'kafka',\n"
        + "  'topic' = 'drivers',\n"
        + "  'properties.bootstrap.servers' = '[::1]:9092',\n"
        + "  'properties.group.id' = 'test',\n"
        + "  'scan.startup.mode' = 'latest-offset',\n"
        + "  'format' = 'json'\n"
        + ");");

    System.out.println("DriverTest table created");
    System.out.println("Query DriverTest table...");

    Table table = tableEnv.sqlQuery("select * from DriverTest");
    DataStream<Row> dataStream = tableEnv.toDataStream(table);
    dataStream.print();
    executionEnv.execute();
  }
}
