import org.apache.flink.api.common.functions.CoGroupFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;
import org.apache.flink.streaming.api.functions.ProcessFunction;
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

    if(dataStream == null){
      System.exit(1);
      return;
    }

    OutputTag<String> aWordsTag = new OutputTag<String>("Awords") {};
    DataStream<String> mainDataStream = dataStream.process(new ProcessFunction<String, String>() {
      @Override
      public void processElement(String value, Context ctx, Collector<String> out) throws Exception {
        if (value.startsWith("a")) {
          ctx.output(aWordsTag, value);
        } else {
          out.collect(value);
        }
      }
    });

    // Split the mainDataStream into two streams
    DataStream<String> otherWordsStream = mainDataStream.getSideOutput(aWordsTag);

    // Write to files
    mainDataStream.writeAsText("/Users/swethakolalapudi/flinkJar/Split2.txt", FileSystem.WriteMode.OVERWRITE);
    otherWordsStream.writeAsText("/Users/swethakolalapudi/flinkJar/Split1.txt", FileSystem.WriteMode.OVERWRITE);

    env.execute("Window co-Group Example");
  }
}
