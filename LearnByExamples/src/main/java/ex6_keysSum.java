import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;

import java.nio.file.Files;
import java.nio.file.Paths;

public class ex6_keysSum {

    public static void main(String[] args) throws Exception {
        // Checking input parameters
        final ParameterTool params = ParameterTool.fromArgs(args);

        // Check if input file exists
        String inputFilePath = params.get("input");
        if (inputFilePath == null || !Files.exists(Paths.get(inputFilePath))) {
            System.out.println("Input file does not exist. Exiting program.");
            System.exit(1);
            return;
        }

        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().setGlobalJobParameters(params);

        DataStream<String> dataStream = StreamUtil.getDataStream(env, params);
        if (dataStream == null) {
            System.exit(1);
            return;
        }

        DataStream<Tuple2<String, Integer>> outStream = dataStream
          .map(new ExtractSpecialties())
          .flatMap(new SplitSpecial())
          .keyBy(0)
          .sum(1);

        outStream.print();

        env.execute("ex6_keysSum - Specialties");
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
        public void flatMap(String input, Collector<Tuple2<String, Integer>> out) throws Exception {
            String[] specialties = input.split("\t");
            for (String specialty : specialties) {
                out.collect(new Tuple2<>(specialty.trim(), 1));
            }
        }
    }
}
