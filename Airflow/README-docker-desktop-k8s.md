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

  Release "airflow" has been upgraded. Happy Helming!
  NAME: airflow
  ...
  Thank you for installing Apache Airflow 2.9.2!
  ...
  Default Webserver (Airflow UI) Login credentials:
      username: admin/password: admin
  Default Postgres connection credentials:
      username: postgres/password: postgres
      port: 5432

  You can get Fernet Key value by running the following:

      echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)
  ... end ...

helm ls -n airflow
    NAME    NAMESPACE       REVISION        UPDATED                  STATUS          CHART           APP VERSION
    airflow airflow         2               2024-07-04 17:46:58.99   deployed        airflow-1.14.0  2.9.2

echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

    Fernet Key: aGZTV1dWZ2lqU1ByaVlwcU1WaU94V2tyUzFBOGZOdnU=

// Create airflow-ingress.yaml
kubectl apply -f airflow-ingress.yaml
    ingress.networking.k8s.io/airflow-webserver-ingress created

kubectl get ingress -n airflow
    NAME              CLASS   HOSTS           ADDRESS     PORTS   AGE
    airflow-ingress   nginx   myairflow.com   localhost   80      7m56s

// Edit hosts file
notepad C:\Windows\System32\drivers\etc\hosts

        127.0.0.1       myairflow.com

<http://myairflow.com> # admin/admin

### Update Airflow

// airflow-values1.yaml
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f airflow-values1.yaml
kubectl apply -f ingress-nginx.yaml
<http://myairflow.com/>

Airflow UI > Cluster Activity

Airflow UI > Admin > Connections > Create
    Conn Id: kubernetes_default
    Conn Type: Kubernetes
    Extra: {"in_cluster": "true", "namespace": "airflow"}

### Add DAGs to Airflow

// Add 2 Dags

hello_world.py
fetch_and_preview.py

git add .
git commit -m "Add DAGs"
git push

// Edit airflow-values1.yaml

helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f airflow-values1.yaml

### Install MinIO

helm repo add minio https://operator.min.io/
helm install minio-operator minio/minio-operator --namespace minio-operator --create-namespace
kubectl get pods -n minio-operator
