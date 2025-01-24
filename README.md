# mpi-kubernetes

A simple example of running an MPI program on Kubernetes. Contains example program for:
* Word count of [NOW corpus](https://www.english-corpora.org/now/)
* Average rating calculation of each [Netflix movies](https://www.kaggle.com/datasets/rishitjavia/netflix-movie-rating-dataset/data)

See also: Implementation in [Hadoop Docker](https://github.com/ynshung/hadoop-docker)

## Prerequisites
- [Docker Desktop](https://docs.docker.com/get-docker/)
- [Kubernetes](https://kubernetes.io/)
  - In Docker Desktop, enable Kubernetes in the settings
  - [Untested] Use [microk8s](https://microk8s.io/) or [minikube](https://minikube.sigs.k8s.io/docs/)

## Usage

### Setup

```bash
# Check if docker image is available
docker pull ynshung/mpi-docker:latest

# Generate ssh keys (optional)
./generate-ssh-secret.sh

# Apply all Kubernetes configurations
kubectl apply -f kubernetes/

# Check the status of the pods
kubectl get pods
# Make sure all pods are running and the copied IP addresses for next command are only from mpi-workers-N

# Get the IP addresses of the pods, copy them temporarily
kubectl get pods -o custom-columns="IP:.status.podIP" --no-headers

# Enter the master pod
kubectl exec -it mpi-worker-0 -- bash

# Create a hostfile
echo "<paste copied ip addresses here>" > hostfile
```

### Word Count
The script counts the number of each words in a directory of text file containing a [sample](https://www.corpusdata.org/formats.asp) of [NoW corpus](https://www.english-corpora.org/now/) and saves the results to a CSV file while tracking execution time.

```bash
# Run the MPI program for word count
mpirun --allow-run-as-root \
    --hostfile hostfile \
    -np 3 python3 /app/word_count_mpi.py

# Run word count without MPI
python3 /app/word_count.py
```

### Netflix Ratings
The script calculates and sorts [Netflix movie ratings](https://www.kaggle.com/datasets/rishitjavia/netflix-movie-rating-dataset/data) by average rating, saving the results to a CSV file while tracking execution time.

```bash
# Run the MPI program for Netflix ratings
mpirun --allow-run-as-root \
    --hostfile hostfile \
    -np 3 python3 /app/netflix_mpi.py

# Run calculation without MPI
python3 /app/netflix.py
```