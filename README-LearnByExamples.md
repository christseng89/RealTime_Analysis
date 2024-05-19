# Learn by Examples

## Start Flink Server

source ~/.bashrc
start-cluster.sh

flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt \
    --output ./flinkOutputs/outputFromTextFile.csv

    Job has been submitted with JobID 230f541cd3308c9baa7613707535f750
    Program execution finished

tail -f $FLINK_HOME/log/flink-*-taskexecutor-*.out

    ==> /home/christseng/flink/flink-1.17.2/log/flink-christseng-taskexecutor-0-Chris-SP8.out <==
    (Janani,,WebProgramming ComputerScience Java    InterviewPrep   BigData)
    (Swetha,,MachineLearning        BigData )
    ...

// Test socket steps
// 1. Start Flink Logs
source ~/.bashrc
tail -f $FLINK_HOME/log/flink-*-taskexecutor-*.out

// 2. Port 9000 input
lsof -i :9000
    COMMAND  PID       USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
    java    7308 christseng   99u  IPv6 107122      0t0  TCP *:9000 (LISTEN)
kill -9 'PID'

nc -lk 9000

    Input some text here ...

// 3. Check Port 9000 and Flink Run
nc -zv localhost 9000
flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000 \
    --output flinkOutputs/outputFromSocket.csv
