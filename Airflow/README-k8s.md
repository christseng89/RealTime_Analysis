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
