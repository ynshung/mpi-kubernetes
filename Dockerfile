FROM python:3.9-slim

# Install MPI and SSH
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev \
    openssh-server \
    wget \
    unzip \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install mpi4py numpy pandas

# Setup SSH
RUN mkdir /var/run/sshd
RUN echo '    StrictHostKeyChecking no' >> /etc/ssh/ssh_config

WORKDIR /app

# Install sample data
RUN wget https://www.corpusdata.org/now/samples/now-text-2024.zip -O /app/dataset.zip && \
    mkdir /app/input-now && \
    unzip /app/dataset.zip -d /app/input-now && \
    rm /app/dataset.zip && \
    chmod 777 /app/input-now/*

RUN wget https://github.com/ynshung/netflix-movie-rating-dataset/releases/download/v1.0/netflix-dataset.zip -O /app/dataset.zip && \
    mkdir /app/input-netflix && \
    unzip /app/dataset.zip -d /app/input-netflix && \
    rm /app/dataset.zip && \
    chmod 777 /app/input-netflix/*

RUN mkdir /app/output

COPY scripts/ /app/