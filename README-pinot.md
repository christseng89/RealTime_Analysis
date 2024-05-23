# Pinot Courses

## Pinot Overview / Architecture

<https://docs.pinot.apache.org/v/release-1.0.0>
<https://docs.pinot.apache.org/v/release-1.0.0/basics/architecture>

## Pinot Quick Start

<https://docs.pinot.apache.org/v/release-1.0.0/basics/getting-started/running-pinot-locally>

java --version
    openjdk 11.0.22 2024-01-16
    OpenJDK Runtime Environment (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1)
    OpenJDK 64-Bit Server VM (build 11.0.22+7-post-Ubuntu-0ubuntu222.04.1, mixed mode, sharing)

PINOT_VERSION=1.0.0
wget https://downloads.apache.org/pinot/apache-pinot-$PINOT_VERSION/apache-pinot-$PINOT_VERSION-bin.tar.gz
tar -xvf apache-pinot-$PINOT_VERSION-bin.tar.gz
mv ./apache-pinot-1.0.0-bin ~/pinot

sudo nano ~/.bashrc
    export PINOT_HOME=~/pinot
    export PATH=$PATH:$PINOT_HOME/bin

source ~/.bashrc
echo $PINOT_HOME
mkdir ~/PinotData

### Start Pinot Zookeeper

pinot-admin.sh StartZookeeper -zkPort 2191 -dataDir ~/PinotData/PinotAdmin/zkData> ./zookeeper-console.log 2>&1 &
    [1] 6970

### Start Pinot Controller

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-controller.log"
pinot-admin.sh StartController -zkAddress [::1]:2191 -controllerPort 9000 -dataDir ~/PinotData/data/PinotController > ./controller-console.log 2>&1 &
    [2] 6771

### Start Pinot Broker

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200  -Xloggc:gc-pinot-broker.log"
pinot-admin.sh StartBroker -zkAddress [::1]:2191 > ./broker-console.log 2>&1 &
    [3] 6971

### Start Pinot Server

export JAVA_OPTS="-Xms32M -Xmx300M -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -Xloggc:gc-pinot-server.log"
pinot-admin.sh StartServer -zkAddress [::1]:2191 -dataDir ~/PinotData/data/pinotServerData -segmentDir ~/PinotData/data/pinotSegments > ./server-console.log 2>&1 &
    [4] 7136

### Pinot ui

<http://localhost:9000/#/>
