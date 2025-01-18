# Dockerfile
FROM python:3.9-slim

# Install MPI
RUN apt-get update && apt-get install -y \
    openmpi-bin \
    libopenmpi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install mpi4py numpy

WORKDIR /app
COPY mpi_sort.py .