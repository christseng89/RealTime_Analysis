import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;

import java.net.Socket;

public class FlinkWindowExample {
  public static void main(String[] args) throws Exception {
    final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

    String host = "localhost";
    int port = 9000;

    // Check if the socket is available before starting the job
    if (!isSocketAvailable(host, port)) {
      System.out.println("Socket at " + host + ":" + port + " is not available. Exiting program.");
      System.exit(1);
    }

    DataStream<String> rawDataStream = env.socketTextStream(host, port);

    DataStream<Tuple2<String, Integer>> dataStream = rawDataStream
      .map(new MapFunction<String, Tuple2<String, Integer>>() {
        @Override
        public Tuple2<String, Integer> map(String value) {
          return Tuple2.of(value, 1);
        }
      })
      .returns(Types.TUPLE(Types.STRING, Types.INT));

    dataStream
      .keyBy(value -> value.f0)
      .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
      .sum(1)
      .print();

    // Register a shutdown hook to handle job cancellation
    Runtime.getRuntime().addShutdownHook(new Thread(() -> {
      System.out.println("Job has been cancelled. Exiting program.");
      System.exit(0);
    }));

    env.execute("FlinkWindowExample");
  }

  private static boolean isSocketAvailable(String host, int port) {
    try (Socket socket = new Socket(host, port)) {
      return true;
    } catch (Exception e) {
      return false;
    }
  }
}
