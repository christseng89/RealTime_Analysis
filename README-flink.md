# Flink

<https://ithelp.ithome.com.tw/m/articles/10336408>
<https://medium.com/devtechie/setting-up-linux-environment-to-install-apache-flink-2fab7e949a79>

## Install Softwares

- Java 11
  java --version
  which java
  JAVA_HOME=/usr/bin/java
  echo $JAVA_HOME

- Firefox
  sudo apt-get install firefox
  firefox --version
  firefox

## Download Flink

cd ~
mkdir flink
cd flink
<!-- wget https://dlcdn.apache.org/flink/flink-1.17.2/flink-1.17.2-bin-scala_2.12.tgz -->
wget https://dlcdn.apache.org/flink/flink-1.17.2/flink-1.17.2-bin-scala_2.12.tgz
tar zxvf flink-1.17.2-bin-scala_2.12.tgz
rm flink-1.17.2-bin-scala_2.12.tgz
ls ~/flink/flink-1.17.2 -l

## Configure Flink

sudo nano ~/.bashrc
    export JAVA_HOME=/usr/bin/java
    export FLINK_HOME=~/flink/flink-1.17.2
    export PATH=$PATH:$FLINK_HOME/bin

source ~/.bashrc
echo $FLINK_HOME
    /home/christseng/flink/flink-1.17.2

nano $FLINK_HOME/conf/flink-conf.yaml
    rest.bind-address: 0.0.0.0
    env.java.opts.all: -Xms1024m -Xmx1024m --add-opens java.base/java.lang=ALL-UNNAMED -XX:MaxDirectMemorySize=1024m -XX:MaxMe>

flink --version
    Version: 1.17.2, Commit ID: c0027e5

### Start Flink

start-cluster.sh
    Starting cluster.
    Starting standalonesession daemon on host Chris-SP8.
    Starting taskexecutor daemon on host Chris-SP8.

sql-client.sh embedded
    exit;

flink run $FLINK_HOME/examples/streaming/WordCount.jar
tail $FLINK_HOME/log/flink-*-taskexecutor-*.out
    (nymph,1)
    (in,3)
    (thy,1)
    (orisons,1)
    (be,4)
    (all,2)
    (my,1)
    (sins,1)
    (remember,1)
    (d,4)

### Flink Web UI

<http://localhost:8081>
