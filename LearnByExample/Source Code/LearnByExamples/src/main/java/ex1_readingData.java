import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.io.IOException;
import java.net.Socket;

public class ex1_readingData {

    public static void main(String[] args) throws Exception {
        // Checking input parameters
        final ParameterTool params = ParameterTool.fromArgs(args);

        final StreamExecutionEnvironment env =
          StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<String> dataStream = null;

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);

        try {
            // Validate and initialize data stream
            if (params.has("input")) {
                dataStream = env.readTextFile(params.get("input"));
            } else if (params.has("host") && params.has("port")) {
                // Check socket connectivity
                String host = params.get("host");
                int port = Integer.parseInt(params.get("port"));
                if (!isPortAvailable(host, port)) {
                    System.err.println("Error: Unable to connect to the specified host and port.");
                    System.exit(1);
                    return;
                }
                dataStream = env.socketTextStream(host, port);
            } else {
                System.out.println("Use --host and --port to specify socket");
                System.out.println("Use --input to specify file input");
                System.exit(1);
                return;
            }
        } catch (Exception e) {
            System.err.println("Error: Unable to initialize data stream.");
            e.printStackTrace();
            System.exit(1);
            return;
        }

        // Validate output parameter
        if (!params.has("output")) {
            System.out.println("Use --output to specify the output file path");
            System.exit(1);
            return;
        }

        // Convert each string to a tuple (for demonstration, we'll split by space and use the first part as key)
        DataStream<Tuple2<String, String>> tupleStream = dataStream.map(new MapFunction<String, Tuple2<String, String>>() {
            @Override
            public Tuple2<String, String> map(String value) throws Exception {
                // Split the string on the first space, use as (key, value) pair
                String[] parts = value.split(" ", 2);
                return parts.length == 2 ? new Tuple2<>(parts[0], parts[1]) : new Tuple2<>(parts[0], "");
            }
        });

        // Print the tuples and write to CSV
        tupleStream.print();
        tupleStream.writeAsCsv(params.get("output"), FileSystem.WriteMode.OVERWRITE, "\n", ",");

        // Execute the Flink job
        env.execute("Read and Write");
    }

    private static boolean isPortAvailable(String host, int port) {
        try (Socket socket = new Socket(host, port)) {
            return true;
        } catch (IOException e) {
            return false;
        }
    }
}
