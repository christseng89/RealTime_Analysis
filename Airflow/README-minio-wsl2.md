## Install Minio Service on WSL2

sudo apt update
sudo apt upgrade -y

wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

minio --version
  minio version RELEASE.2024-07-13T01-46-15Z (commit-id=459985f0fa5c5c9bc19e8bf2b81f624cee18519b)
  Runtime: go1.22.5 linux/amd64
  License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
  Copyright: 2015-2024 MinIO, Inc.

sudo mkdir -p ~/minio/data
sudo mkdir -p ~/minio/config

sudo chown -R christseng89:christseng89 ~/minio/data
sudo chmod -R u+rxw ~/minio/data

export MINIO_ROOT_USER=minio
export MINIO_ROOT_PASSWORD=minio123

minio server ~/minio/data --console-address ":9001"
    MinIO Object Storage Server
    Copyright: 2015-2024 MinIO, Inc.
    License: GNU AGPLv3 - https://www.gnu.org/licenses/agpl-3.0.html
    Version: RELEASE.2024-07-13T01-46-15Z (go1.22.5 linux/amd64)

    API: http://10.255.255.254:9000  http://172.17.116.87:9000  http://127.0.0.1:9000
      RootUser: minio
      RootPass: minio123

    WebUI: http://10.255.255.254:9001 http://172.17.116.87:9001 http://127.0.0.1:9001
      RootUser: minio
      RootPass: minio123

  CLI: https://min.io/docs/minio/linux/reference/minio-mc.html#quickstart
    $ mc alias set 'myminio' 'http://10.255.255.254:9000' 'minio' 'minio123'

  Docs: https://min.io/docs/minio/linux/index.html

<http://localhost:9001/>

// Cntl C to terminate the Minio Server 

### Run MinIO as a Service

whoami
  christseng89

id -gn
  christseng89

sudo nano /etc/systemd/system/minio.service
=================
[Unit]
Description=MinIO
Documentation=https://docs.min.io
Wants=network-online.target
After=network-online.target

[Service]
User=christseng89
Group=christseng89
Environment="MINIO_ROOT_USER=minio"
Environment="MINIO_ROOT_PASSWORD=minio123"
ExecStart=/usr/local/bin/minio server /home/christseng89/minio/data --console-address ":9001"
Restart=always
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target

=================

sudo systemctl daemon-reload
sudo systemctl enable minio
sudo systemctl start minio
  sudo systemctl start minio
  Created symlink /etc/systemd/system/multi-user.target.wants/minio.service → /etc/systemd/system/minio.service.

sudo systemctl status minio
  ● minio.service - MinIO
      Loaded: loaded (/etc/systemd/system/minio.service; enabled; vendor preset: enabled)
      Active: active (running) since Sat 2024-07-13 14:42:07 CST; 14s ago
        Docs: https://docs.min.io
      ...

<http://localhost:9001/> => Create Bucker => k8s-bucket-backup

curl http://localhost:9001

  StatusCode        : 200
  StatusDescription : OK
  Content           : <!doctype html><html lang="en"><head><meta charset="utf-8"/><base href="/"/><meta 
  ...
  RawContent        : HTTP/1.1 200 OK
  ...

sudo systemctl stop minio
