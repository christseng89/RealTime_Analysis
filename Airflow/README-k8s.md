# Airflow on Kubernetes

Apache Airflow provides support for running tasks on Kubernetes through the KubernetesExecutor and KubernetesPodOperator. To define Kubernetes configurations for Airflow tasks, you need to set up the appropriate executor and configure the KubernetesPodOperator. Here are the steps and configurations required:

## 1. Using KubernetesExecutor

The KubernetesExecutor allows Airflow to dynamically launch tasks as Kubernetes Pods. Here are the steps to configure it:

**Step 1: Modify `airflow.cfg`**
Update your `airflow.cfg` to set the executor to KubernetesExecutor:

[core]
executor = KubernetesExecutor

**Step 2: Configure Kubernetes Section**
Add the necessary Kubernetes configuration in the `airflow.cfg`:

[kubernetes]
// Path to the Kubernetes configuration file (kubeconfig)
kube_config_path = /path/to/your/kubeconfig
// Namespace to launch pods in
namespace = airflow
// Additional configuration options

**Step 3: Airflow Deployment**
Ensure your Airflow scheduler and webserver are running with access to the Kubernetes cluster. You might deploy Airflow itself on Kubernetes, using Helm charts or custom Kubernetes manifests.

## 2. Using KubernetesPodOperator

The KubernetesPodOperator allows you to run individual tasks as Kubernetes Pods. Here is an example DAG using KubernetesPodOperator:

**Step 1: Import Required Modules**
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago

**Step 2: Define Default Arguments and DAG**
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'k8s_pod_operator_example',
    default_args=default_args,
    schedule_interval=None,
)

**Step 3: Configure KubernetesPodOperator**
k = KubernetesPodOperator(
    namespace='airflow',
    image="python:3.8-slim",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="hello-world",
    task_id="hello-world-task",
    get_logs=True,
    dag=dag,
)

### 3. Advanced Configuration

You can specify more advanced configurations for the KubernetesPodOperator, such as resource limits, environment variables, and volume mounts.

**Resource Requests and Limits:**
k = KubernetesPodOperator(
    namespace='airflow',
    image="python:3.8-slim",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="hello-world",
    task_id="hello-world-task",
    get_logs=True,
    resources={
        'request_memory': '64Mi',
        'request_cpu': '250m',
        'limit_memory': '128Mi',
        'limit_cpu': '500m',
    },
    dag=dag,
)

**Environment Variables:**
from kubernetes.client import V1EnvVar

k = KubernetesPodOperator(
    namespace='airflow',
    image="python:3.8-slim",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="hello-world",
    task_id="hello-world-task",
    get_logs=True,
    env_vars=[V1EnvVar(name='MY_ENV_VAR', value='SOME_VALUE')],
    dag=dag,
)

**Volume Mounts:**
from kubernetes.client import V1Volume, V1VolumeMount

volume = V1Volume(
    name='my-volume',
    host_path={'path': '/tmp'}
)

volume_mount = V1VolumeMount(
    name='my-volume',
    mount_path='/tmp'
)

k = KubernetesPodOperator(
    namespace='airflow',
    image="python:3.8-slim",
    cmds=["python", "-c"],
    arguments=["print('hello world')"],
    labels={"foo": "bar"},
    name="hello-world",
    task_id="hello-world-task",
    get_logs=True,
    volumes=[volume],
    volume_mounts=[volume_mount],
    dag=dag,
)

### Conclusion

By configuring the KubernetesExecutor and KubernetesPodOperator correctly, you can leverage the power of Kubernetes to run and manage your Airflow tasks. Ensure you have the necessary Kubernetes configurations and permissions set up for Airflow to interact with your Kubernetes cluster.

### References

<https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/kubernetes.html>
<https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/kubernetes_executor.html>
<https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#howto-operator-kubernetespodoperator>

### Reference Links

- [Kubetools](https://collabnix.github.io/kubetools/)
- [Kubernetes](https://kubernetes.io/docs/tasks/tools/)

choco upgrade kubernetes-cli -y
kubectl version
kubectl cluster-info
kubectl config get-contexts
kubectl config use-context docker-desktop

choco upgrade kubernetes-helm -y
helm version

### Nginx Ingress

wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml -O ingress-nginx.yaml
kubectl apply -f ingress-nginx.yaml
kubectl get pods -n ingress-nginx

### Kubernetes Dashboard

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

### Install Airflow on Docker Desktop k8s

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
