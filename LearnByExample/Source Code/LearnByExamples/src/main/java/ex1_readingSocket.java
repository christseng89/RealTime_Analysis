import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.utils.ParameterTool;

public class ex1_readingSocket {

  public static void main(String[] args) throws Exception {

    // Obtain the command-line parameters
    final ParameterTool params = ParameterTool.fromArgs(args);

    // Obtain host and port from command-line parameters
    String host = params.get("host", "localhost");
    int port = params.getInt("port", 0); // Default port is 0, adjust as needed

    // Create the execution environment
    final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

    // Ensure that host and port are set externally
    if (host.equals("localhost") && port == 0) {
      throw new IllegalArgumentException("Please provide --host and --port arguments externally.");
    }

    // Create the data source
    env.fromElements("Apache", "Flink", "Example", "Data", "Stream")
      // Map each element to upper case
      .map((MapFunction<String, String>) String::toUpperCase)
      // Print the transformed elements
      .print();

    // Execute the Flink job
    env.execute("Flink Example");
  }
}
