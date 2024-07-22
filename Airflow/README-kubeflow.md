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
