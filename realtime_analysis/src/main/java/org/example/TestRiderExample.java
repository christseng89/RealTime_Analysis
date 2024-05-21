package org.example;

import org.apache.flink.api.common.JobExecutionResult;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

import java.util.concurrent.CancellationException;

public class TestRiderExample {
  public static void main(String[] args) throws Exception {
    final StreamExecutionEnvironment executionEnv =
      StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnv = StreamTableEnvironment.create(executionEnv);

    tableEnv.executeSql(
      "CREATE TABLE RiderTest (\n"
        + "  `rider_id` STRING,\n"
        + "  `name` STRING,\n"
        + "  `membership_status` STRING,\n"
        + "  `last_updated_at`  TIMESTAMP(3),\n"
        + "  `request_time` TIMESTAMP(3) METADATA FROM 'timestamp',\n"
        + "  `processing_time` as PROCTIME()\n"
        + ") WITH (\n"
        + "  'connector' = 'kafka',\n"
        + "  'topic' = 'riders',\n"
        + "  'properties.bootstrap.servers' = 'localhost:9092',\n"  // Updated here
        + "  'properties.group.id' = 'test',\n"
        + "  'scan.startup.mode' = 'latest-offset',\n"
        + "  'format' = 'json'\n"
        + ");");

    System.out.println("RiderTest table created");
    System.out.println("Query RiderTest table...");

    Table table = tableEnv.sqlQuery("SELECT * FROM RiderTest");
    DataStream<Row> dataStream = tableEnv.toDataStream(table);
    dataStream.print();

    // Submit the job and obtain a JobClient for control
    JobClient jobClient = executionEnv.executeAsync("TestRiderExample");

    // Add a shutdown hook to gracefully shut down the job
    Runtime.getRuntime().addShutdownHook(new Thread(() -> {
      try {
        System.out.println("Shutdown hook triggered, waiting for the job to complete...");
        jobClient.cancel().get();
      } catch (CancellationException ce) {
        System.out.println("Job canceled, waiting for completion...");
      } catch (Exception e) {
        e.printStackTrace();
      }
    }));

    // Wait for the job to finish
    JobExecutionResult result = jobClient.getJobExecutionResult().get();
    System.out.println("Execution result: " + result);
  }
}

