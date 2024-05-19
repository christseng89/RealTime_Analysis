import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.streaming.api.functions.source.SourceFunction.SourceContext;

import java.io.File;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Scanner;
import java.io.IOException;

public class ex1_readingData {

    public static void main(String[] args) throws Exception {
        // Checking input parameters
        final ParameterTool params = ParameterTool.fromArgs(args);

        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        DataStream<String> dataStream = null;

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);
        String sourceType = "Text File";

        if (params.has("input")) {
            String inputFilePath = params.get("input");
            if (!new File(inputFilePath).exists()) {
                System.err.println("Error: The specified input file does not exist.");
                System.exit(1);
                return;
            }
            dataStream = env.readTextFile(inputFilePath);
        } else if (params.has("host") && params.has("port")) {
            sourceType = "Socket";
            String host = params.get("host");
            int port = Integer.parseInt(params.get("port"));
            if (!isPortAvailable(host, port)) {
                System.err.println("Error: Unable to connect to the specified host and port.");
                System.exit(1);
                return;
            }

            dataStream = env.addSource(new SocketSourceFunction(host, port));
        } else {
            System.out.println("Use --host and --port to specify socket");
            System.out.println("Use --input to specify file input");
            System.exit(1);
            return;
        }

        if (dataStream == null) {
            System.exit(1);
            return;
        }

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

        tupleStream.print();
        tupleStream.writeAsCsv(params.get("output"), FileSystem.WriteMode.OVERWRITE, "\n", ",");

        env.execute("Read and Write from " + sourceType);
    }

    private static boolean isPortAvailable(String host, int port) {
        try (Socket socket = new Socket(host, port)) {
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    private static class SocketSourceFunction implements SourceFunction<String> {
        private final String host;
        private final int port;
        private volatile boolean isRunning = true;

        public SocketSourceFunction(String host, int port) {
            this.host = host;
            this.port = port;
        }

        @Override
        public void run(SourceContext<String> ctx) throws Exception {
            try (ServerSocket serverSocket = new ServerSocket(port);
                 Socket socket = serverSocket.accept();
                 Scanner scanner = new Scanner(socket.getInputStream())) {
                while (isRunning && scanner.hasNextLine()) {
                    String line = scanner.nextLine();
                    if ("STOP".equals(line.trim())) {
                        isRunning = false;
                    } else {
                        ctx.collect(line);
                    }
                }
            }
        }

        @Override
        public void cancel() {
            isRunning = false;
        }
    }
}
