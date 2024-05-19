# Learn by Examples

## Start Flink Server

source ~/.bashrc

flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt \
    --output ./flinkOutputs/outputFromTextFile.csv

    Job has been submitted with JobID 230f541cd3308c9baa7613707535f750
    Program execution finished

tail $FLINK_HOME/log/flink-*-taskexecutor-*.out

    ==> /home/christseng/flink/flink-1.17.2/log/flink-christseng-taskexecutor-0-Chris-SP8.out <==
    (Janani,,WebProgramming ComputerScience Java    InterviewPrep   BigData)
    (Swetha,,MachineLearning        BigData )
    ...

// Test socket steps
// 1. Start Flink Logs
source ~/.bashrc
tail -f $FLINK_HOME/log/flink-*-taskexecutor-*.out

// 2. Port 9000 input
nc -lk 9000

    Input some text here ...


nc -zv localhost 9000
flink run -c ex1_readingData target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000 \
    --output ./flinkOutputs/outputFromSocket.csv
