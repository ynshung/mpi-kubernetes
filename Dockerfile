FROM python:3.9-slim

# Install MPI and SSH
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install mpi4py numpy

# Setup SSH
RUN mkdir /var/run/sshd
RUN echo '    StrictHostKeyChecking no' >> /etc/ssh/ssh_config

WORKDIR /app
COPY mpi_sort.py .
COPY sort.py .