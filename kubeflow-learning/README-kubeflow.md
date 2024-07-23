## Kubeflow Installation Notes

<https://v1-6-branch.kubeflow.org/docs/components/pipelines/installation/localcluster-deployment/#deploying-kubeflow-pipelines>

### Deploy the Kubeflow Pipelines

export PIPELINE_VERSION=1.8.5
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic-pns?ref=$PIPELINE_VERSION"

kubectl get deployment minio -n kubeflow -o yaml > minio-deployment.yaml
nano minio-deployment.yaml
 // Change Image to minio/minio:latest

kubectl apply -f minio-deployment.yaml

### Run the following to port-forward the Kubeflow Pipelines UI

kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
<http://localhost:8080>

### Pipelines Pre-built Component

<https://github.com/kubeflow/pipelines/tree/master/components>
<https://cloud.google.com/vertex-ai/docs/pipelines/gcpc-list>

pip install kfp==1.8.5

python3 hello_pipeline.py

<http://localhost:8080/#/pipelines> => + Upload pipeline => 
- Pipeline Name (Hello pipeline)
- Pipeline Description (hello_pipeline)
- Upload a file (hello_pipeline.yaml) => Create

<http://localhost:8080/#/pipelines> => Hello pipeline => + Create run =>
- Experiements (Default) => Start

<http://localhost:8080/#/runs> => Run of Hello pipeline => Graph (Say hello) => Logs
    Hello !

### Kubeflow Git Clone

git clone https://github.com/kubeflow/manifests.git
cd manifests
git checkout v1.8.0

## Katib (AutoML) Installation

<https://v1-6-branch.kubeflow.org/docs/components/katib/hyperparameter/#installing-katib>

kubectl apply -k "github.com/kubeflow/katib.git/manifests/v1beta1/installs/katib-standalone?ref=master"
kubectl port-forward svc/katib-ui -n kubeflow 8180:80
<http://localhost:8180/katib>

pip install -U kubeflow-katib==0.17.0

### Create Katib Experiments

git clone https://github.com/kubeflow/katib.git
cd katib\examples\v1beta1\hp-tuning

kubectl create -f grid.yaml
kubectl create -f hyperband.yaml
python3 random_experiment.py

kubectl get experiment -n kubeflow
    NAME        TYPE        STATUS   AGE
    grid        Running     True     25s
    hyperband   Succeeded   True     4h44m
    random      Running     True     34m

kubectl get po -n kubeflow

<http://localhost:8180/katib/> => Namespace (kubeflow)
