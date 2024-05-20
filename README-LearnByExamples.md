# Learn by Examples

## Start Flink Server

source ~/.bashrc
start-cluster.sh
tail -f $FLINK_HOME/log/flink-*-taskexecutor-*.out

<http://localhost:8081/>

### Enable port 9000

lsof -i :9000
    COMMAND  PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    java    7308 christseng   99u  IPv6 107122      0t0  TCP *:9000 (LISTEN)
kill -9 'PID'
nc -lk 9000

### Example #1

// Read and Write from Text File
flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt \
    --output ./flinkOutputs/outputFromTextFile.csv

    Job has been submitted with JobID 230f541cd3308c9baa7613707535f750
    Program execution finished

// Read and Write from Socket
nc -zv localhost 9000
flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000 \
    --output flinkOutputs/outputFromSocket.csv

### Example #2

nc -zv localhost 9000
flink run -c ex2_filter target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

### Example #3

nc -zv localhost 9000
flink run -c ex3_Map target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

### Example #4

flink run -c ex4_flatMap target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt

    WebProgramming
    ComputerScience
    Java
    InterviewPrep
    ...

### 13. Stateless and Stateful Transformations

- Stateless
  - filter
  - map
  - flatMap
  - keyBy
- Stateful
  - reduce
  - sum
  - min
  - max
- Accumulate data
  - Entire data
  - Windowed data
  - Keyed data
  - Aggregated data
  - Reduced data
  - Processed data
