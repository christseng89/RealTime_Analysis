import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;
import org.apache.flink.streaming.api.functions.sink.RichSinkFunction;

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
      }
      dataStream = env.readTextFile(inputFilePath);
    } else if (params.has("host") && params.has("port")) {
      sourceType = "Socket";
      String host = params.get("host");
      int port = Integer.parseInt(params.get("port"));

      if (!isHostReachable(host, port)) {
        System.err.println("Error: The specified host and port are not reachable.");
        System.exit(1);
      }

      dataStream = env.addSource(new SocketSourceFunction(host, port));
    } else {
      System.out.println("Use --host and --port to specify socket");
      System.out.println("Use --input to specify file input");
      System.exit(1);
    }

    if (dataStream == null) {
      System.exit(1);
    }

    if (!params.has("output")) {
      System.out.println("Use --output to specify the output file path");
      System.exit(1);
    }

    // Convert each string to a tuple (for demonstration, we'll split by space and use the first part as key)
    System.out.println("Reading from " + sourceType);
    DataStream<Tuple2<String, String>> tupleStream = dataStream.map(new MapFunction<String, Tuple2<String, String>>() {
      @Override
      public Tuple2<String, String> map(String value) throws Exception {
        // Split the string on the first space, use as (key, value) pair
        String[] parts = value.split(" ", 2);
        return parts.length == 2 ? new Tuple2<>(parts[0], parts[1]) : new Tuple2<>(parts[0], "");
      }
    });

    tupleStream.print();

    // Add a custom sink to write the accumulated data to CSV
    tupleStream.addSink(new CsvSinkFunction(params.get("output")));

    // Execute the job
    System.out.println("Writing to CSV file: " + params.get("output"));
    env.execute("Read and Write from " + sourceType);
  }

  private static class SocketSourceFunction implements SourceFunction<String> {
    private final String host;
    private final int port;
    private volatile boolean isRunning = true;
    private final List<String> accumulatedData = new ArrayList<>();

    public SocketSourceFunction(String host, int port) {
      this.host = host;
      this.port = port;
    }

    @Override
    public void run(SourceContext<String> ctx) throws Exception {
      try (Socket socket = new Socket(host, port); Scanner scanner = new Scanner(socket.getInputStream())) {
        while (isRunning && scanner.hasNextLine()) {
          String line = scanner.nextLine();
          accumulatedData.add(line);
          ctx.collect(line);
        }
      } catch (IOException e) {
        System.err.println("Error reading from socket: " + e.getMessage());
        isRunning = false;  // Stop the source if there is an error
      }
    }

    @Override
    public void cancel() {
      isRunning = false;
    }

    public List<String> getAccumulatedData() {
      return accumulatedData;
    }
  }

  private static class CsvSinkFunction extends RichSinkFunction<Tuple2<String, String>> {
    private final String outputPath;

    public CsvSinkFunction(String outputPath) {
      this.outputPath = outputPath;
    }

    @Override
    public void open(Configuration parameters) throws Exception {
      super.open(parameters);
      File outputFile = new File(outputPath);
      File parentDir = outputFile.getParentFile();
      if (parentDir != null && !parentDir.exists()) {
        if (!parentDir.mkdirs()) {
          throw new IOException("Failed to create directories for output path: " + outputPath);
        }
      }
      if (outputFile.exists()) {
        if (!outputFile.delete()) {
//          throw new IOException("Failed to delete existing output file: " + outputPath);
        }
      }
    }

    @Override
    public void invoke(Tuple2<String, String> value, Context context) throws Exception {
      // Writing the accumulated data to the CSV file
      try (PrintWriter writer = new PrintWriter(new java.io.FileWriter(outputPath, true))) {
        writer.println(value.f0 + value.f1);
      } catch (IOException e) {
        System.err.println("Error writing to CSV file: " + e.getMessage());
      }
    }
  }

  private static boolean isHostReachable(String host, int port) {
    try (Socket s = new Socket()) {
      s.connect(new InetSocketAddress(host, port), 1000);
      return true;
    } catch (IOException e) {
      return false;
    }
  }
}
