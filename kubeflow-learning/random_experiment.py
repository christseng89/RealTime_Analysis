import kfp
from kfp import Client
from kubernetes.client import V1ObjectMeta
from kubeflow.katib import KatibClient
from kubeflow.katib.models import V1beta1Experiment, V1beta1ExperimentSpec, V1beta1ObjectiveSpec, V1beta1AlgorithmSpec, V1beta1TrialTemplate, V1beta1TrialParameterSpec, V1beta1TrialSpec, V1beta1ParameterSpec, V1beta1FeasibleSpace

# Define the experiment
experiment = V1beta1Experiment(
    api_version="kubeflow.org/v1beta1",
    kind="Experiment",
    metadata=V1ObjectMeta(
        namespace="kubeflow",
        name="random"
    ),
    spec=V1beta1ExperimentSpec(
        objective=V1beta1ObjectiveSpec(
            type="minimize",
            goal=0.001,
            objective_metric_name="loss"
        ),
        algorithm=V1beta1AlgorithmSpec(
            algorithm_name="random"
        ),
        parallel_trial_count=3,
        max_trial_count=12,
        max_failed_trial_count=3,
        parameters=[
            V1beta1ParameterSpec(
                name="lr",
                parameter_type="double",
                feasible_space=V1beta1FeasibleSpace(
                    min="0.01",
                    max="0.05"
                )
            ),
            V1beta1ParameterSpec(
                name="momentum",
                parameter_type="double",
                feasible_space=V1beta1FeasibleSpace(
                    min="0.5",
                    max="0.9"
                )
            )
        ],
        trial_template=V1beta1TrialTemplate(
            primary_container_name="training-container",
            trial_parameters=[
                V1beta1TrialParameterSpec(
                    name="learningRate",
                    description="Learning rate for the training model",
                    reference="lr"
                ),
                V1beta1TrialParameterSpec(
                    name="momentum",
                    description="Momentum for the training model",
                    reference="momentum"
                )
            ],
            trial_spec={
                "apiVersion": "batch/v1",
                "kind": "Job",
                "spec": {
                    "template": {
                        "spec": {
                            "containers": [
                                {
                                    "name": "training-container",
                                    "image": "docker.io/kubeflowkatib/pytorch-mnist-cpu:latest",
                                    "command": [
                                        "python3",
                                        "/opt/pytorch-mnist/mnist.py",
                                        "--epochs=1",
                                        "--batch-size=16",
                                        "--lr=${trialParameters.learningRate}",
                                        "--momentum=${trialParameters.momentum}"
                                    ],
                                    "resources": {
                                        "limits": {
                                            "memory": "1Gi",
                                            "cpu": "0.5"
                                        }
                                    }
                                }
                            ],
                            "restartPolicy": "Never"
                        }
                    }
                }
            }
        )
    )
)

# Create a Katib client
katib_client = KatibClient()

# Create the experiment
experiment_result = katib_client.create_experiment(experiment)
# print("Experiment created:", experiment_result)
print(f"Experiment: {experiment.metadata.name} created in namespace {experiment.metadata.namespace}")
