import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;

import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class ex11_countWindow {

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

        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
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

        DataStream<courseCount> outStream = dataStream
          .map(new parseRow())
          .keyBy(value -> value.course)
          .window(SlidingProcessingTimeWindows.of(Time.seconds(30), Time.seconds(10)))
          .sum("count");

        outStream.print();

        env.execute("ex11_countWindow - SlidingProcessingTimeWindows");
    }

    public static class parseRow implements MapFunction<String, courseCount> {
        @Override
        public courseCount map(String input) throws Exception {
            try {
                String[] rowData = input.split(",");
                if (rowData.length == 3) {
                    return new courseCount(rowData[1].trim(), 1); // Use the country as the key and initialize count as 1
                } else {
                    throw new IllegalArgumentException("Invalid input format: " + input);
                }
            } catch (Exception ex) {
                System.out.println(ex);
                return null;
            }
        }
    }

    // Class to hold the course count
    public static class courseCount {
        public String course;
        public Integer count;

        public courseCount() {
        }

        public courseCount(String course, Integer count) {
            this.course = course;
            this.count = count;
        }

        public String getCourse() {
            return course;
        }

        public void setCourse(String course) {
            this.course = course;
        }

        public Integer getCount() {
            return count;
        }

        public void setCount(Integer count) {
            this.count = count;
        }

        @Override
        public String toString() {
            return course + ": " + count;
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
