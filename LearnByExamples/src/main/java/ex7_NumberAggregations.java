import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

// use socket
public class ex7_NumberAggregations {

    public static void main(String[] args) throws Exception {
        final ParameterTool params = ParameterTool.fromArgs(args);

        // Check if host and port are available
        String host = params.get("host", "localhost");
        int port = params.getInt("port", 9999);
        if (!isHostPortAvailable(host, port)) {
            System.out.println("Specified host and port are not available.");
            System.exit(1);
        }

        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setGlobalJobParameters(params);

        DataStream<String> dataStream = StreamUtil.getDataStream(env, params);

        if (dataStream == null) {
            System.exit(1);
            return;
        }

        DataStream<Tuple2<String, Double>> minStream = dataStream
          .map(new RowSplitter())
          .keyBy(0)
          .min(1); // min, max, sum etc.

        minStream.print();

        env.execute("ex7_NumberAggregations");
    }

    // Method to check if host and port are available
    private static boolean isHostPortAvailable(String host, int port) {
        try (Socket ignored = new Socket()) {
            ignored.connect(new InetSocketAddress(host, port), 200);
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    // Method to stop the port if it's already in use
    private static void stopPortIfInUse(int port) {
        // Implement stopping logic here, if needed
    }

    public static class RowSplitter implements MapFunction<String, Tuple2<String, Double>> {

        public Tuple2<String, Double> map(String row) throws Exception {
            try {
                String[] fields = row.split(" ");
                if (fields.length == 2) {
                    return new Tuple2<>(
                      fields[0] /* name */,
                      Double.parseDouble(fields[1]) /* running time in minutes */);
                }
            } catch (Exception ex) {
                System.out.println(ex);
            }

            return null;
        }
    }
}
