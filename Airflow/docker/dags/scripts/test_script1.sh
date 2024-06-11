#!/bin/bash
echo "Execute command" 
echo "Task Id: {{ti.task_id}}"
echo "AWS API Key: {{var.value.api_key_aws}}"
echo "Who am I?" && whoami
env
exit 0
# exit 10 # Bash command returned exit code 10. Skipping.