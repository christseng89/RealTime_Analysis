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
  k8s-backup-2024.07.12-19.50   Completed   0        36         2024-07-12 19:50:55 29d       default            <none>

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

### Install Velero Client

wget https://github.com/vmware-tanzu/velero/releases/download/v1.14.0/velero-v1.14.0-linux-amd64.tar.gz
tar -xvf velero-v1.14.0-linux-amd64.tar.gz
sudo mv velero-v1.14.0-linux-amd64/velero /usr/local/bin/

which velero

### Create Minio Credentails

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

// Buckets => Create Bucket + (velero-bucket) => Create Bucket

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

## Part II: Velero Backup/Restore w Minio

<https://medium.com/@ithesadson/how-to-use-velero-installation-backup-and-restore-guide-with-minio-7e2c907d0a44>

### Uninstall Minio Tenant1 (Optional)

helm uninstall minio-tenant1 -n minio-tenant1
kubectl delete ns minio-tenant1

### Install Velero Client

wget https://github.com/vmware-tanzu/velero/releases/download/v1.14.0/velero-v1.14.0-linux-amd64.tar.gz
tar -xvf velero-v1.14.0-linux-amd64.tar.gz
sudo mv velero-v1.14.0-linux-amd64/velero /usr/local/bin/

which velero

### Create Minio Credentails

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

// Buckets => Create Bucket + (velero-bucket) => Create Bucket

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
