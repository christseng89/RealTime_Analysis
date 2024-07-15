# Install Airflow on Docker Desktop Kubernetes

## Reference Links

- [Kubetools](https://collabnix.github.io/kubetools/)
- [Kubernetes](https://kubernetes.io/docs/tasks/tools/)

choco upgrade kubernetes-cli -y
kubectl version
kubectl cluster-info
kubectl config get-contexts
kubectl config use-context docker-desktop

choco upgrade kubernetes-helm -y
helm version

### 1. Install Nginx Ingress

wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml -O ingress-nginx.yaml
kubectl apply -f ingress-nginx.yaml
kubectl get pods -n ingress-nginx

### 2. Install Kubernetes Dashboard

wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml -O kubernetes-dashboard.yaml

kubectl apply -f kubernetes-dashboard.yaml
kubectl get pods -n kubernetes-dashboard

// Write kubernetes-dashboard1.yaml with Ingress
kubectl apply -f kubernetes-dashboard1.yaml
    serviceaccount/admin-user created
    clusterrolebinding.rbac.authorization.k8s.io/admin-user created
    secret/admin-user created

kubectl get ingress -n kubernetes-dashboard
    NAMESPACE              NAME                           CLASS   HOSTS           ADDRESS     PORTS   AGE
    kubernetes-dashboard   kubernetes-dashboard-ingress   nginx   dashboard.com   localhost   80      2m1s

kubectl -n kubernetes-dashboard get secret admin-user -o jsonpath="{.data.token}" | base64 --decode

eyJhbGciOiJSUzI1N...

// Edit hosts file and /etc/hosts in WSL2 (Use the WSL 2 based engine)
notepad C:\Windows\System32\drivers\etc\hosts

        127.0.0.1       dashboard.com

<https://dashboard.com/>

### 3. Install Metrics Server
<https://github.com/kubernetes-sigs/metrics-server?tab=readme-ov-file>

wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml -O metrics-server.yaml

kubectl apply -f metrics-server1.yaml

// metrics-server1 => with new line...
      containers:
      - args:
        ...
        - --metric-resolution=15s
        - --kubelet-insecure-tls # Run metrics-server with insecure TLS 

kubectl top node
kubectl top pod -A

### 4. Install Airflow

helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace
helm upgrade airflow apache-airflow/airflow --namespace airflow
helm show values apache-airflow/airflow > airflow-values.yaml

helm ls -n airflow
    NAME    NAMESPACE       REVISION        UPDATED                  STATUS          CHART           APP VERSION
    airflow airflow         2               2024-07-04 17:46:58.99   deployed        airflow-1.14.0  2.9.2

echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

    Fernet Key: aGZTV1dWZ2lqU1ByaVlwcU1WaU94V2tyUzFBOGZOdnU=

#### Update Airflow 1

// Create airflow-values.yaml
// Create helm-airflow.bat

helm-airflow.bat

kubectl get ingress -n airflow
    NAME                     CLASS   HOSTS           ADDRESS     PORTS   AGE
    airflow-flower-ingress   nginx   myflower.com    localhost   80      28m
    airflow-ingress          nginx   myairflow.com   localhost   80      32m

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts

        127.0.0.1       myairflow.com
        127.0.0.1       myflower.com

<http://myairflow.com> # admin/admin
<http://myflower.com/>

#### Add DAGs to Airflow

// Add 2 Dags

hello_world.py
fetch_and_preview.py

git add .
git commit -m "Add DAGs"
git push

#### Airflow UI Setting Connections and Variables

Airflow UI > Cluster Activity

Airflow UI > Admin > Connections > Create
    Conn Id: kubernetes_default
    Conn Type: Kubernetes
    Extra: {"in_cluster": "true", "namespace": "airflow"}

#### Airflow Environments SMTP

<https://airflow.apache.org/docs/apache-airflow/stable/howto/email-config.html>

// Edit airflow-values1.yaml
env:
  - name: AIRFLOW__SMTP__SMTP_HOST
    value: "smtp.gmail.com"
  - name: AIRFLOW__SMTP__SMTP_STARTTLS
    value: "True"
  - name: AIRFLOW__SMTP__SMTP_SSL
    value: "False"
  ...

#### Update Airflow 2

helm-airflow.bat

kubectl exec -it airflow-webserver-586666dd95-96hnz -n airflow -- /bin/bash
    env | grep SMTP
    AIRFLOW__SMTP__SMTP_PORT=587
    AIRFLOW__SMTP__SMTP_PASSWORD=s...
    AIRFLOW__SMTP__SMTP_USER=...@gmail.com
    AIRFLOW__SMTP__SMTP_MAIL_FROM=...@gmail.com
    AIRFLOW__SMTP__SMTP_STARTTLS=True

kubectl describe deploy airflow-webserver -n airflow | grep Image
    Image:      apache/airflow:2.9.2

#### Airflow for requirements.txt (not yet)

<https://airflow.apache.org/docs/docker-stack/build.html>

// Dockerfile
FROM apache/airflow:2.9.2
COPY requirements.txt /
COPY includes/ includes/
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

docker build -t airflow-requirements:2.9.2 .

### 5 Install MinIO by Helm

// Helm Minio Operator
<https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html>

helm repo add minio-operator https://operator.min.io
helm upgrade --install minio-operator minio-operator/operator --namespace minio-operator --create-namespace
helm repo update
helm show values minio-operator/operator > minio-operator-values.yaml

helm-minio-operator.bat

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts
    ...
    127.0.0.1       minio-operator.com

// Minio Tenant
<https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-minio-tenant-helm.html>

helm search repo minio-operator
helm upgrade --install minio-tenant1 minio-operator/tenant --namespace minio-tenant1 --create-namespace
helm show values minio-operator/tenant > minio-tenant-values.yaml

helm-minio-tenant.bat
kubectl port-forward svc/minio-tenant1-console -n minio-tenant1 9443:9443 
<http://localhost:9443> # minio/minio123

kubectl -n minio-operator get secret/console-sa-secret -o jsonpath="{.data.token}" | base64 --decode
<https://minio-operator.com/>

Login with JWT => minio-tenant1 => Management Console (icon) => Minio Tenant1

### Metabase

helm repo add stable https://charts.helm.sh/stable
helm repo update

helm search repo stable/metabase
helm upgrade --install metabase stable/metabase --namespace metabase --create-namespace

// Edit Metabase Components Manually

kubectl get deployment metabase -o=jsonpath='{$.spec.template.spec.containers[:1].image}' -n metabase
kubectl set image deployment/metabase metabase=metabase/metabase:v0.50.4 -n metabase
kubectl apply -f metabase-ingress.yaml

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts
    ...
    127.0.0.1       mymetabase.com

<https://mymetabase.com>

// Add Database

- Data Type: PostgreSQL
- Display Name: Postgres DW
- Host: airflow-postgresql.airflow.svc.cluster.local
- Port: 5432
- Database Name: postgres
- Username: postgres
- Password: postgres

### Yunikorn (Spark) Installation

helm repo add yunikorn https://apache.github.io/yunikorn-release
helm repo update

helm upgrade --install yunikorn yunikorn/yunikorn --namespace yunikorn --create-namespace
helm show values yunikorn/yunikorn > yunikorn-values.yaml

kubectl port-forward svc/yunikorn-service 9889:9889 -n yunikorn
<http://localhost:9889>

### Install Spark Job on Kubernetes (kubernetes-dashboard)

<https://hub.docker.com/_/spark>

docker pull spark
docker run -it --rm --name spark spark /opt/spark/bin/spark-shell
    spark.range(1000 * 1000 * 1000).count()
        res2: Long = 1000000000
    :q

docker run -it --rm --name spark spark:latest python3 --version
    Python 3.8.10

kubectl apply -f kubernetes-spark.yaml
kubectl get pods -n spark
    NAME                            READY   STATUS    RESTARTS   AGE
    spark-master-cff6f984d-6vhqr    1/1     Running   0          8m44s
    spark-worker-7d45b479b9-wq9lr   1/1     Running   0          8m44s
    spark-worker-7d45b479b9-z7mvv   1/1     Running   0          8m44s

kubectl exec -it spark-master-cff6f984d-6vhqr -n spark -- /bin/bash

### Test Spark via PySpark

// Install Hadoop for Windows
<https://cwiki.apache.org/confluence/display/HADOOP2/WindowsProblems>

git clone https://github.com/steveloughran/winutils
<https://hadoop.apache.org/release/3.0.0.html>

tar -xzvf hadoop-3.0.0.tar.gz
ren hadoop-3.0.0 Hadoop
copy winutils.exe to Hadop\bin

- set HADOOP_HOME=C:\Hadoop
- add C:\Hadoop\bin to PATH

// Pip Install Spark for Windows
pip install spark pyspark
where spark
where pyspark

python -m venv .venv

// Git Bash
cd /d/development/Real_Time_Analysis/Airflow/kubernetes

source .venv/Scripts/activate
    (.venv)

    pip install spark pyspark
    which spark
        /d/development/Real_Time_Analysis/Airflow/kubernetes/.venv/Scripts/spark
    which spark-submit
        /d/development/Real_Time_Analysis/Airflow/kubernetes/.venv/Scripts/spark-submit

    export PATH="/c/Program Files/Java/jdk1.8.0_211/bin:$PATH"
    java -version
        java version "1.8.0_211"

    which java
        /c/Program Files/Java/jdk1.8.0_211/bin/java
    which hadoop
        /c/Hadoop/bin/hadoop
    which winutils
        /c/Hadoop/bin/winutils

    python spark/spark-process.py
        ...
        Spark Session created
        Hello World!

    // *** SPECIAL NOTES ***
    // ERROR ShutdownHookManager: Exception while deleting Spark temp dir:
    // - Known Issue: <https://issues.apache.org/jira/browse/SPARK-12216?jql=text%20~%20%22ERROR%20ShutdownHookManager%22>
    // Temporary Solution: Wait for 30 seconds for the Spark Session to be closed

### Spark Submit a Spark Jobs to Kubernetes (kubernetes-dashboard)

// Install Apache Spark for Windows
tar -xzvf spark-3.5.1-bin-hadoop3.tgz
ren spark-3.5.1-bin-hadoop3 spark-3.5.1

- set SPARK_HOME=C:\spark-3.5.1
- add C:\spark-3.5.1\bin to PATH

#### Build and Test Spark Job's Docker Image

    cd spark
    docker build -t christseng89/myspark:1.0 .
    docker push christseng89/myspark:1.0
    docker run -it --rm --name myspark christseng89/myspark:1.0 cat /opt/spark/spark-process.py
    docker run -it --rm --name myspark christseng89/myspark:1.0 python3 --version
        Python 3.8.10
    
    docker run -it --rm --name myspark christseng89/myspark:1.0
        ...
        Spark Session created
        Hello World!

#### Running Spark Job on Kubernetes

    kubectl apply -f spark-job.yaml
    kubectl get pods -n kubernetes-dashboard
        NAME                                         READY   STATUS      RESTARTS       AGE
        dashboard-metrics-scraper-5657497c4c-8l4s2   1/1     Running     19 (23h ago)   5d22h
        kubernetes-dashboard-78f87ddfc-62b9c         1/1     Running     22 (23h ago)   5d22h
        spark-application-v64jl                      0/1     Completed   0              97s

    kubectl logs spark-application-v64jl -n kubernetes-dashboard
        ...
        Spark Session created
        Hello World!

    deactivate

#### Spark Submit a Spark Jobs to Kubernetes

// Spark Submit
spark-submit \
  --name spark-processing \
  --master k8s://https://kubernetes.docker.internal:6443 \
  --deploy-mode cluster \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=admin-user \
  --conf spark.kubernetes.namespace=kubernetes-dashboard \
  --conf spark.executor.instances=1 \
  --conf spark.kubernetes.container.image=christseng89/myspark:1.0 \
  --conf spark.kubernetes.container.image.pullPolicy=Always \
  local:///opt/spark/spark-process.py

    ...
    24/07/10 21:45:12 INFO ShutdownHookManager: Shutdown hook called
    24/07/10 21:45:12 INFO ShutdownHookManager: Deleting directory C:\Users\Chris Tseng\AppData\Local\Temp\spark-52b51970-95ab-47aa-9038-f18133d54e11

deactivate

# Velero Backup/Restore w S3 and Minio on Docker Desktop

## Part I: Velero Backup/Restore w AWS S3

### Create S3 Bucket

aws configure
  AWS Access Key ID [None]: AKIA2HOUI....
  AWS Secret Access Key [None]: W2qlSKRodqT....
  Default region name [None]: us-east-2
  Default output format [None]: json

aws s3 ls
  2020-07-11 12:36:12 cf-templates-1gsoe1tlou6y4-us-east-1
  2020-08-09 19:23:42 elasticstack7-indepth
  ...

aws s3api create-bucket --bucket k8s-bucket-backup --region us-east-1
  {
      "Location": "/k8s-bucket-backup"
  }

### Install Velero Client

wget https://github.com/vmware-tanzu/velero/releases/download/v1.14.0/velero-v1.14.0-linux-amd64.tar.gz
tar -xvf velero-v1.14.0-linux-amd64.tar.gz
sudo mv velero-v1.14.0-linux-amd64/velero /usr/local/bin/

### Install Velero Server w S3

// Credentials file for Velero

cat <<EOF > credentials-velero
[default]
aws_access_key_id=AKIA2HOUI....
aws_secret_access_key=W2qlSKRodqT....
EOF

// Install Velero to work with S3

velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.5.1 \
  --bucket k8s-bucket-backup \
  --secret-file ./credentials-velero \
  --backup-location-config region=us-east-1 \
  --snapshot-location-config region=us-east-1

velero version
    Client:
            Version: v1.14.0
            Git commit: 2fc6300f2239f250b40b0488c35feae59520f2d3
    Server:
            Version: v1.14.0

### Velero Backup w S3

BACKUP_NAME="k8s-backup-$(date +%Y.%m.%d-%H.%M)"
echo $BACKUP_NAME

velero backup create $BACKUP_NAME --wait
  Backup completed with status: Completed. You may check for more information using the commands `velero backup describe k8s-backup-2024.07.12-19.50` and `velero backup logs k8s-backup-2024.07.12-19.50`.

velero backup logs $BACKUP_NAME
  ..
  time="2024-07-12T11:50:58Z" level=info msg="Backed up a total of 864 items" backup=velero/k8s-backup-2024.07.12-19.50 logSource="pkg/backup/backup.go:498" progress=

velero get backup
  NAME                          STATUS      ERRORS   WARNINGS   CREATED             EXPIRES   STORAGE LOCATION   SELECTOR
  k8s-backup-2024.07.12-19.50   Completed   0        36         2024-07-12 19:50:55 29d       default

### Velero Restore w S3

velero restore create $BACKUP_NAME --from-backup $BACKUP_NAME --wait
  Restore completed with status: Completed. You may check for more information using the commands `velero restore describe k8s-backup-2024.07.12-19.50` and `velero restore logs k8s-backup-2024.07.12-19.50`.

velero restore describe $BACKUP_NAME
velero restore logs $BACKUP_NAME
  time="2024-07-12T12:06:01Z" level=info msg="restore completed" logSource="pkg/controller/restore_controller.go:605" restore=velero/k8s-backup-2024.07.12-19.50

velero uninstall

## Part II: Velero Backup/Restore w Minio

<https://medium.com/@ithesadson/how-to-use-velero-installation-backup-and-restore-guide-with-minio-7e2c907d0a44>

### Uninstall Minio Tenant1 (Optional)

helm uninstall minio-tenant1 -n minio-tenant1
kubectl delete ns minio-tenant1

### Install Velero Client (Same as above)

wget https://github.com/vmware-tanzu/velero/releases/download/v1.14.0/velero-v1.14.0-linux-amd64.tar.gz
tar -xvf velero-v1.14.0-linux-amd64.tar.gz
sudo mv velero-v1.14.0-linux-amd64/velero /usr/local/bin/

which velero

### Create Minio Credentials

// Credentials file for Minio

cat <<EOF > credentials-minio
[default]
aws_access_key_id=minio
aws_secret_access_key=minio123
EOF

### Install Minio in Velero

kubectl apply -f minio-velero.yaml
kubectl get po -n minio
  NAME                    READY   STATUS      RESTARTS   AGE
  minio-c44b4df8d-6cmfn   1/1     Running     0          11s
  minio-setup-mzkm5       0/1     Completed   0          11s

kubectl get ing -n minio
  NAME    CLASS   HOSTS         ADDRESS     PORTS   AGE
  minio   nginx   myminio.com   localhost   80      9m7s

notepad C:\Windows\System32\drivers\etc\hosts
  ...
  127.0.0.1       myminio.com

<https://myminio.com> => Buckets => Create Bucket + (velero-bucket) => Create Bucket

### Install Velero Server

velero install \
  --provider aws \
  --image velero/velero:v1.14.0 \
  --plugins velero/velero-plugin-for-aws:v1.10.0 \
  --bucket velero-bucket \
  --secret-file ./credentials-minio \
  --use-node-agent \
  --use-volume-snapshots=false \
  --uploader-type kopia \
  --default-volumes-to-fs-backup \
  --namespace velero \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio.minio.svc.cluster.local:9000 \
  --wait

kubectl logs deployment/velero -n velero
  ...
  time="2024-07-15T03:46:07Z" level=info msg="BackupStorageLocations is valid, marking as available" backup-storage-location=velero/default controller=backup-storage-location logSource="pkg/controller/backup_storage_location_controller.go:126"
  ...

velero version
    Client:
            Version: v1.14.0
            Git commit: 2fc6300f2239f250b40b0488c35feae59520f2d3
    Server:
            Version: v1.14.0

kubectl get backupstoragelocations -n velero
  NAME      PHASE       LAST VALIDATED   AGE     DEFAULT
  default   Available   8s               2m10s   true

### Create Backups

BACKUP_NAME="full-cluster-backup-$(date +%Y.%m.%d-%H.%M)"
velero backup create $BACKUP_NAME --wait
  ...
  Backup completed with status: Completed. You may check for more information using the commands `velero backup describe full-cluster-backup-2024.07.15-11.48` and `velero backup logs full-cluster-backup-2024.07.15-11.48`.

velero backup describe $BACKUP_NAME
velero backup logs $BACKUP_NAME

velero get backup
  NAME                                   STATUS      ERRORS   WARNINGS   CREATED              EXPIRES   STORAGE LOCATION   SELECTOR
  full-cluster-backup-2024.07.15-14.09   Completed   0        5          2024-07-15 14:09:19  29d       default
