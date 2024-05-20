import java.net.Socket;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

// use socket
// Filter, Map, and Chaining
public class ex3_Map {

  public static void main(String[] args) throws Exception {
    // Checking input parameters
    final ParameterTool params = ParameterTool.fromArgs(args);

    String host = params.get("host");
    int port = params.getInt("port");

    // Check if the host and port are available
    if (!isHostPortAvailable(host, port)) {
      System.out.println("Host or port not available. Exiting program.");
      System.exit(1);
      return;
    }

    final StreamExecutionEnvironment env =
        StreamExecutionEnvironment.getExecutionEnvironment();

    // make parameters available in the web interface
    env.getConfig().setGlobalJobParameters(params);

    DataStream<String> dataStream = StreamUtil.getDataStream(env, params);

    if (dataStream == null) {
      System.exit(1);
      return;
    }

    DataStream<String> outStream =
        dataStream.filter(new Filter()).map(new CleanString());

    outStream.print();

    env.execute("ex3_Map");
  }

  public static boolean isHostPortAvailable(String host, int port) {
    try (Socket socket = new Socket(host, port)) {
      return true;
    } catch (Exception e) {
      return false;
    }
  }

  public static class Filter implements FilterFunction<String> {
    public boolean filter(String input) throws Exception {
      try {
        Double.parseDouble(input.trim());
        return false;
      } catch (Exception ex) {
        // Do nothing
      }
      return input.length() > 3;
    }
  }

  public static class CleanString implements MapFunction<String, String> {
    public String map(String input) throws Exception {
      return input.trim().toLowerCase();
    }
  }
}
