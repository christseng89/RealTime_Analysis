import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

import java.io.IOException;
import java.net.Socket;

// use socket
public class ex2_filter {

    public static void main(String[] args) throws Exception {

        // Checking input parameters
        final ParameterTool params = ParameterTool.fromArgs(args);

        // Host and port parameters
        String host = params.get("host");
        int port = params.getInt("port");

        // Check if the host and port are available
        if (!isHostPortAvailable(host, port)) {
            System.err.println("Host " + host + " and port " + port + " are not available.");
            System.exit(1);
        }

        final StreamExecutionEnvironment env =
          StreamExecutionEnvironment.getExecutionEnvironment();

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);

        DataStream<String> dataStream = StreamUtil.getDataStream(env, params);

        if(dataStream==null){
            System.exit(1);
            return;
        }

        DataStream<String> outStream = dataStream.filter(new Filter());

        outStream.print();

        env.execute("ex2_filter");
    }

    // Method to check if host and port are available
    private static boolean isHostPortAvailable(String host, int port) {
        try (Socket socket = new Socket(host, port)) {
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public static class Filter implements FilterFunction<String> {

        public boolean filter(String input) throws Exception {
            try {
                Double.parseDouble(input.trim());
                return false;
            } catch (Exception ex) {
            }

            return input.length() > 3;
        }

    }
}
