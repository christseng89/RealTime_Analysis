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

### Install Kubernetes Dashboard

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

eyJhbGciOiJSUzI1NiIsImtpZCI6IkVGRVFHU1pYY3hMNnhlQ0F5TkMtLUdtSEh6UXNVRmhsRHgyTHhsX1dYaTgifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiIyMzFiYzk3OC01YmI4LTQ4ZDYtOWU4YS0wMDkwNDU4OTAwMDYiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.uWKxzzITzVhRGTGUlsEBhCG0C_zZMn-EnvWyGdrPfX9EEw3ba54XAEF6ntJ5FRaMeOcf39YFFR7Rt5jpjBqk82uOG0Cn9019rmTJiCf6bupsNDUM4YBVJMUXevLSNCgUpDgFPoRqFYSo_vDIr7TCN6VgIXwkfIrbuYZYJGDtFXoo6eYRWB_Pxh14KfRht5oQW9Zc4_vj91cEG8VQcMXUpgUj3yxDKD26YPqlADW3VA5KlXU8BOadM76f5fetNNEgT_DQ-NG1E3-vl8kuByeAS2guGKUYIAj0IURJwoO-ENCsXY8VTvQ7elIAxkRUB8ZNXQvNG-uDg7ZdEMCMSTUx1A

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts

        127.0.0.1       dashboard.com

<https://dashboard.com/>

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

kubectl get po -n minio-operator
kubectl port-forward svc/console -n minio-operator 9090:9090
kubectl -n minio-operator get secret/console-sa-secret -o jsonpath="{.data.token}" | base64 --decode

<http://localhost:9090/>

// Minio Tenant
<https://min.io/docs/minio/kubernetes/upstream/operations/install-deploy-manage/deploy-minio-tenant-helm.html>

helm search repo minio-operator
helm upgrade --install minio-tenant1 minio-operator/tenant --namespace minio-tenant1 --create-namespace
helm show values minio-operator/tenant > minio-tenant-values.yaml

helm-minio-tanent.bat
kubectl port-forward svc/minio-tenant1-console -n minio-tenant1 9443:9443

<http://localhost:9443>

### Spark Installation

choco install hadoop -y

// Git Bash


pip install spark pyspark

cd Airflow/kubernetes/
python -m venv spark
source spark/bin/activate

whick spark
whick pyspark
which spark-submit
    /c/Python312/Scripts/spark-submit
    (spark)
mkdir spark

// Edit spark-process.py
python spark/spark-process.py

### Metabase

helm repo add stable https://charts.helm.sh/stable
helm install --name metabase stable/metabase

### Force delete Airflow

kubectl delete all --all -n airflow --force
kubectl delete ns airflow

### Helm Uninstall

helm uninstall minio-operator -n minio-operator
