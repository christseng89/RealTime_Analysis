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

### Install Nginx Ingress

wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml -O ingress-nginx.yaml
kubectl apply -f ingress-nginx.yaml
kubectl get pods -n ingress-nginx

### Install Kubernetes Dashboard/Metrics Server

wget https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml -O kubernetes-dashboard.yaml

kubectl apply -f kubenertes-dashboard.yaml
kubectl get pods -n kubernetes-dashboard

// Write kubernetes-dashboard1.yaml with Ingress
kubectl apply -f kubernetes-dashboard1.yaml
    serviceaccount/admin-user created
    clusterrolebinding.rbac.authorization.k8s.io/admin-user created
    secret/admin-user created

kubectl get ingress -n kubernetes-dashboard
    NAMESPACE              NAME                           CLASS   HOSTS           ADDRESS     PORTS   AGE
    kubernetes-dashboard   kubernetes-dashboard-ingress   nginx   dashboard.com   localhost   80      2m1s

// Git Bash
kubectl -n kubernetes-dashboard get secret admin-user -o jsonpath="{.data.token}" | base64 --decode

eyJhbGciOiJSUzI1N...

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts

        127.0.0.1       dashboard.com

<https://dashboard.com/>

// Metrics Server
<https://github.com/kubernetes-sigs/metrics-server?tab=readme-ov-file>

kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/high-availability-1.21+.yaml

### Install Airflow

helm repo add apache-airflow https://airflow.apache.org

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace
helm upgrade airflow apache-airflow/airflow --namespace airflow
helm show values apache-airflow/airflow > airflow-values.yaml

helm ls -n airflow
    NAME    NAMESPACE       REVISION        UPDATED                  STATUS          CHART           APP VERSION
    airflow airflow         2               2024-07-04 17:46:58.99   deployed        airflow-1.14.0  2.9.2

echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

    Fernet Key: aGZTV1dWZ2lqU1ByaVlwcU1WaU94V2tyUzFBOGZOdnU=

### Update Airflow

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

### Add DAGs to Airflow

// Add 2 Dags

hello_world.py
fetch_and_preview.py

git add .
git commit -m "Add DAGs"
git push

### Airflow UI Setting Connections and Variables

Airflow UI > Cluster Activity

Airflow UI > Admin > Connections > Create
    Conn Id: kubernetes_default
    Conn Type: Kubernetes
    Extra: {"in_cluster": "true", "namespace": "airflow"}

### Airflow Environments SMTP

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

### Airflow for requirements.txt (not yet)

<https://airflow.apache.org/docs/docker-stack/build.html>

// Dockerfile
FROM apache/airflow:2.9.2
COPY requirements.txt /
COPY includes/ includes/
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt

docker build -t airflow-requirements:2.9.2 .

### Install MinIO by Helm

// Helm Minio Operator
<https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-operator-helm.html>

helm repo add minio-operator https://operator.min.io
helm upgrade --install minio-operator minio-operator/operator --namespace minio-operator --create-namespace
helm show values minio-operator/operator > minio-operator-values.yaml

helm-minio-operator.bat
kubectl -n minio-operator get secret/console-sa-secret -o jsonpath="{.data.token}" | base64 --decode

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts
    ...
    127.0.0.1       minio-operator.com

<https://minio-operator.com/>

// Minio Tenant
<https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-minio-tenant-helm.html>

helm search repo minio-operator
helm upgrade --install minio-tenant1 minio-operator/tenant --namespace minio-tenant1 --create-namespace
helm show values minio-operator/tenant > minio-tenant-values.yaml

helm-minio-tenant.bat
kubectl port-forward svc/minio-tenant1-console -n minio-tenant1 9443:9443
<http://localhost:9443> # minio/minio123

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

### Velero Backup to local

kubectl create namespace velero
kubectl create secret generic cloud-credentials \
  --namespace velero \
  --from-literal=aws=aws_access_key_id=minio;aws_secret_access_key=minio123

mkdir D:\k8s-backup
echo '{}' > k8s-backup-secret.txt

velero install \
  --provider aws \
  --plugins velero/velero-plugin-for-aws:v1.2.0 \
  --bucket velero \
  --secret-file k8s-backup-secret.txt \
  --backup-location-config region=minio,s3ForcePathStyle="true",s3Url=http://minio-tenant1.minio.svc.cluster.local:9000 \
  --snapshot-location-config region=minio

k get po -n velero
