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

### Example #5

flink run -c ex5_keys target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt

    (WebProgramming,1)
    (ComputerScience,1)
    (Java,1)
    (InterviewPrep,1)
    ...

### Example #6

flink run -c ex6_keysSum target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/specialties.txt

    ...
    (MachineLearning,2)
    (GMAT,1)
    (Statistics,2)
    (GMAT,2)
    (Finance,2)
    (GMAT,3)

### Example #7

nc -zv localhost 9000
flink run -c ex7_NumberAggregations target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// Socket input data
    exampleData1 10.5
    exampleData1 10.52
    exampleData1 10.6
    exampleData1 12  
    exampleData1 5

// Flink Output
    ...
    (exampleData1,10.5)
    (exampleData1,5.0)

### Example #8

flink run -c ex8_reduce target/flink-examples-1.0-SNAPSHOT.jar \
    --input ./flinkData/courses.txt

    (MachineLearning,2.5)
    (WebProgramming,7.5)
    (ComputerScience,14.0)

### 19. Windows Transformation

- Build-in Windows
  - Tumbling Windows
    将数据流划分为大小相等的、不重叠的时间区间。例如，每 10 秒计算一次总和。
  - Sliding Windows
    将数据流划分为大小相等的、可以重叠的时间区间。例如，每 5 秒计算一次过去 10 秒的平均值。
  - Count Windows
  - Session Windows (Time interval between two events)
    根据事件之间的间隔动态地划分窗口。适用于会话分析，当用户活动有空闲期时，窗口会自动结束。
  - Global Windows
    一个永不关闭的窗口，常用于需要手动触发的场景。

- Custom Windows
  - Window Assigner
  - Trigger
  - Evictor
  - Process Window Function
  - Window Function
  - Process All Window Function
  - All Window Function
  - Process Window Function

### Example #9 - Window All Test

// #1 Test
flink run -c FlinkWindowExample1 target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// #1 nc input
example1
example2
example1
example3
example2

// #1 task manager output
(example2,2)
(example1,2)
(example3,1)

// #2 Test
flink run -c FlinkWindowExample2 target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// #2 nc input
ReactJS, India, 1488705752
ReactJS, US, 1488705753
JQuery, India, 1488705755
ReactJS, US, 1488705743
Hadoop, US, 1488705744
ReactJS, India, 1488705747

DataStructures, US, 1488705750
ReactJS, India, 1488705693
DataStructures, UK, 1488705694
JQuery, US, 1488705705
DataStructures, India, 1488705707

// #2 task manager output
(1488705752,ReactJS,1)
(1488705753,ReactJS,1)
(1488705755,JQuery,1)
(1488705743,ReactJS,1)
(1488705744,Hadoop,1)
(1488705747,ReactJS,1)
(1488705750,DataStructures,1)
(1488705693,ReactJS,1)
(1488705694,DataStructures,1)
(1488705705,JQuery,1)
(1488705707,DataStructures,1)

#### Example #9 - WindowAll Tumbling (no keyed stream)

flink run -c ex9_windowAll target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// nc input from signups.txt

// flink output
(US,27)

#### Example #10 - Windows Sliding (keyed stream)

flink run -c ex10_windows target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// nc input from signups.txt

// flink output
(US,10)
(UK,4)
(India,13)

#### Example #11 - Windows Sliding Count (keyed stream)

flink run -c ex11_countWindow target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// nc input from courses.txt
// flink output
3: 1
10: 1
15: 1
8: 1
2: 1
12: 1
12: 2

#### Example #12 - Windows Session (keyed stream)

flink run -c ex11_countWindow target/flink-examples-1.0-SNAPSHOT.jar \
    --host localhost \
    --port 9000

// nc input from courses.txt
// flink output
