FROM apache/airflow:2.4.2

USER root

# Install dependencies for building Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    wget \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libreadline-dev \
    libsqlite3-dev \
    libgdbm-dev \
    libdb5.3-dev \
    libbz2-dev \
    libexpat1-dev \
    liblzma-dev \
    tk-dev \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12.2
RUN wget https://www.python.org/ftp/python/3.12.2/Python-3.12.2.tgz \
    && tar xzf Python-3.12.2.tgz \
    && cd Python-3.12.2 \
    && ./configure --enable-optimizations \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.12.2 Python-3.12.2.tgz

# Update alternatives to set Python 3.12 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.12 1 \
    && update-alternatives --install /usr/bin/pip3 pip3 /usr/local/bin/pip3.12 1

# Verify the installation
RUN python3.12 --version \
    && pip3.12 --version

COPY requirements.txt .

USER airflow

# Upgrade pip and install required Python packages
RUN pip3.12 install --upgrade pip \
    && pip3.12 install --no-cache-dir -r requirements.txt
