import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;

import java.io.File;

public class ex5_keys {

    public static void main(String[] args) throws Exception {

        final ParameterTool params = ParameterTool.fromArgs(args);
        String inputFilePath = params.get("input");

        // Check if the input file exists
        if (!isFileExists(inputFilePath)) {
            System.out.println("Input file does not exist. Exiting program.");
            System.exit(1);
            return;
        }

        final StreamExecutionEnvironment env =
          StreamExecutionEnvironment.getExecutionEnvironment();

        env.getConfig().setGlobalJobParameters(params);

        DataStream<String> dataStream = StreamUtil.getDataStream(env, params);
        if (dataStream == null) {
            System.exit(1);
            return;
        }

        DataStream<Tuple2<String, Integer>> outStream = dataStream
          .map(new ExtractSpecialties())
          .flatMap(new SplitSpecial());

        outStream.print();

        env.execute("ex5_keys - Find Specialties");
    }

    public static boolean isFileExists(String filePath) {
        File file = new File(filePath);
        return file.exists() && file.isFile();
    }

    public static class ExtractSpecialties implements MapFunction<String, String> {
        public String map(String input) throws Exception {
            try {
                return input.split(",")[1].trim();
            } catch (Exception e) {
                return null;
            }
        }
    }

    public static class SplitSpecial implements FlatMapFunction<String, Tuple2<String, Integer>> {
        public void flatMap(String input, Collector<Tuple2<String, Integer>> out)
          throws Exception {
            String[] specialties = input.split("\t");
            for (String specialty : specialties) {
                out.collect(new Tuple2<>(specialty.trim(), 1));
            }
        }
    }
}
