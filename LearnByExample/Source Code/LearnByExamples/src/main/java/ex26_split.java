import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.ProcessFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.util.OutputTag;

public class ex26_split {

  public static void main(String[] args) throws Exception {
    // Checking input parameters
    final ParameterTool params = ParameterTool.fromArgs(args);

    final StreamExecutionEnvironment env =
      StreamExecutionEnvironment.getExecutionEnvironment();

    // make parameters available in the web interface
    env.getConfig().setGlobalJobParameters(params);

    DataStream<String> dataStream = StreamUtil.getDataStream(env, params);

    if (dataStream == null) {
      System.exit(1);
      return;
    }

    // Define the OutputTags for the side outputs
    final OutputTag<String> awordsTag = new OutputTag<String>("Awords") {};
    final OutputTag<String> otherwordsTag = new OutputTag<String>("Others") {};

    // Process the stream and direct elements to side outputs
    SingleOutputStreamOperator<String> mainDataStream = dataStream.process(new rerouteData(awordsTag, otherwordsTag));

    // Extract the side output streams
    DataStream<String> awords = mainDataStream.getSideOutput(awordsTag);
    DataStream<String> otherwords = mainDataStream.getSideOutput(otherwordsTag);

    // Write the streams to separate files
    awords.writeAsText("/Users/swethakolalapudi/flinkJar/Split1.txt", FileSystem.WriteMode.OVERWRITE);
    otherwords.writeAsText("/Users/swethakolalapudi/flinkJar/Split2.txt", FileSystem.WriteMode.OVERWRITE);

    env.execute("Window co-Group Example");
  }

  public static class rerouteData extends ProcessFunction<String, String> {

    private final OutputTag<String> awordsTag;
    private final OutputTag<String> otherwordsTag;

    public rerouteData(OutputTag<String> awordsTag, OutputTag<String> otherwordsTag) {
      this.awordsTag = awordsTag;
      this.otherwordsTag = otherwordsTag;
    }

    @Override
    public void processElement(String value, Context ctx, Collector<String> out) throws Exception {
      if (value.startsWith("a")) {
        ctx.output(awordsTag, value);
      } else {
        ctx.output(otherwordsTag, value);
      }
    }
  }
}
