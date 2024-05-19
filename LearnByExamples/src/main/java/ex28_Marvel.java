import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.graph.Graph;

public class ex28_Marvel {

    public static void main(String[] args) throws Exception {
        // Checking input parameters
        final ParameterTool params = ParameterTool.fromArgs(args);

        String verticesFilePath = params.get("vertices");
        String edgesFilePath = params.get("edges");
        if (verticesFilePath == null || edgesFilePath == null) {
            System.err.println("Both vertices and edges file paths are required. Use --vertices and --edges to specify them.");
            return;
        }

        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);

        DataSet<Tuple3<Long,String,Integer>> vertexData = env.readCsvFile(verticesFilePath)
          .fieldDelimiter("|")
          .ignoreInvalidLines()
          .types(Long.class, String.class, Integer.class);

        DataSet<Tuple2<Long,Tuple2<String, Integer>>> vertexTuples  = vertexData
          .map(new GetVertex());

        DataSet<Tuple3<Long,Long,Integer>> edgeTuples  = env.readCsvFile(edgesFilePath)
          .fieldDelimiter(",")
          .ignoreInvalidLines()
          .types(Long.class, Long.class, Integer.class);

        Graph<Long, Tuple2<String, Integer>, Integer> graph =
          Graph.fromTupleDataSet(vertexTuples, edgeTuples, env);

        System.out.println("Number of edges: " + graph.numberOfEdges());
        System.out.println("Number of vertices: " + graph.numberOfVertices());
    }

    private static class GetVertex implements MapFunction<Tuple3<Long, String, Integer>,
      Tuple2<Long, Tuple2<String, Integer>>> {
        public Tuple2<Long, Tuple2<String, Integer>> map(Tuple3<Long, String, Integer> input) throws Exception {
            return Tuple2.of(input.f0, Tuple2.of(input.f1, input.f2));
        }
    }
}
