import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;


// use socket with nc signups.txt
public class ex9_windowAll {

  public static void main(String[] args) throws Exception {
    final ParameterTool params = ParameterTool.fromArgs(args);

    // Check if required parameters are provided
    if (!params.has("host") || !params.has("port")) {
      System.out.println("Please provide --host and --port parameters.");
      System.exit(1);
    }

    final String host = params.get("host");
    final int port = params.getInt("port");

    // Check if host and port are available
    if (!isHostPortAvailable(host, port)) {
      System.out.println("Host or port is not available.");
      System.exit(1);
    }

    final StreamExecutionEnvironment env =
        StreamExecutionEnvironment.getExecutionEnvironment();
    env.getConfig().setGlobalJobParameters(params);

    DataStream<String> dataStream = env.socketTextStream(host, port);

    // Start a separate thread to continuously check if the socket is connected
    Thread socketCheckThread = new Thread(() -> {
      try {
        while (true) {
          if (!isHostPortAvailable(host, port)) {
            System.out.println("Socket disconnected. Exiting program.");
            System.exit(0);
          }
          Thread.sleep(1000); // Check every second
        }
      } catch (InterruptedException e) {
        e.printStackTrace();
      }
    });
    socketCheckThread.start();

    DataStream<Tuple2<String, Integer>> parsedStream =
        dataStream.map(new parseRow());

    DataStream<Tuple2<String, Integer>> outStream =
        parsedStream
            .windowAll(TumblingProcessingTimeWindows.of(Time.seconds(10)))
            .sum(1);

    outStream.print();

    env.execute("ex9_windowAll - Tumbling Window");
  }

  public static class parseRow
      implements MapFunction<String, Tuple2<String, Integer>> {

    public Tuple2<String, Integer> map(String input) throws Exception {
      try {
        String[] rowData = input.split(",");
        return new Tuple2<String, Integer>(rowData[1].trim(), 1);
      } catch (Exception ex) {
        System.out.println(ex);
      }
      return null;
    }
  }

  // Method to check if host and port are available
  public static boolean isHostPortAvailable(String host, int port) {
    try (Socket s = new Socket(host, port)) {
      return true;
    } catch (Exception e) {
      return false;
    }
  }
}
