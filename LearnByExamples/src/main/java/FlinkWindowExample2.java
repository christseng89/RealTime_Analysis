import java.net.Socket;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

public class FlinkWindowExample2 {
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

    DataStream<Tuple3<String, String, Integer>> dataStream = rawDataStream
      .map(new MapFunction<String, Tuple3<String, String, Integer>>() {
        @Override
        public Tuple3<String, String, Integer> map(String value) {
          String[] elements = value.split(", ");
          return Tuple3.of(elements[2], elements[0], 1);
        }
      })
      .returns(Types.TUPLE(Types.STRING, Types.STRING, Types.INT));

    dataStream
      .keyBy(value -> value.f0)
      .process(new DeduplicateFunction())
      .print();

    env.execute("FlinkWindowExample2 - sliding window");
  }

  private static boolean isSocketAvailable(String host, int port) {
    try (Socket socket = new Socket(host, port)) {
      return true;
    } catch (Exception e) {
      return false;
    }
  }

  public static class DeduplicateFunction extends KeyedProcessFunction<String, Tuple3<String, String, Integer>, Tuple3<String, String, Integer>> {
    private transient ValueState<Boolean> seen;

    @Override
    public void open(org.apache.flink.configuration.Configuration parameters) throws Exception {
      seen = getRuntimeContext().getState(new ValueStateDescriptor<>("seen", Boolean.class));
    }

    @Override
    public void processElement(Tuple3<String, String, Integer> value, Context ctx, Collector<Tuple3<String, String, Integer>> out) throws Exception {
      Boolean isSeen = seen.value();
      if (isSeen == null) {
        seen.update(true);
        out.collect(value);
      }
    }
  }
}
