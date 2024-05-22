package org.example;

import org.apache.flink.api.common.JobExecutionResult;
import org.apache.flink.core.execution.JobClient;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.Table;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;
import org.apache.flink.types.Row;

import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;

public class TestLocationExample {
  public static void main(String[] args) throws Exception {
    final StreamExecutionEnvironment executionEnv =
      StreamExecutionEnvironment.getExecutionEnvironment();
    StreamTableEnvironment tableEnv = StreamTableEnvironment.create(executionEnv);

    // Lookup Join with JDBC
    tableEnv.executeSql("CREATE TABLE Location (\n"
      + "  location_id STRING,\n"
      + "  city STRING,\n"
      + "  country STRING,\n"
      + "  PRIMARY KEY (location_id) NOT ENFORCED\n"
      + ") WITH (\n"
      + "   'connector' = 'jdbc',\n"
      + "   'driver' = 'com.mysql.cj.jdbc.Driver',\n"
      + "   'url' = 'jdbc:mysql://localhost:3306/analytics',\n"
      + "   'table-name' = 'Location',\n"
      + "   'username' = 'root',\n"
      + "   'password' = 'passWord'\n"
      + ");");

    System.out.println("Location table created");
    System.out.println("Query Location table...");

    Table table = tableEnv.sqlQuery("select * from Location");
    DataStream<Row> dataStream = tableEnv.toDataStream(table);
    dataStream.print();

    // Submit the job and obtain a JobClient for control
    JobClient jobClient = executionEnv.executeAsync("TestLocationExample");

    // Wait for the job to reach the RUNNING state
    jobClient.getJobExecutionResult().get();
    JobExecutionResult result = jobClient.getJobExecutionResult().get();
    System.out.println("Execution result: " + result);
    System.exit(0);
  }
}
