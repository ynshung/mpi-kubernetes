# mpi-kubernetes

A simple example of running an MPI program on Kubernetes.

## Prerequisites
- [Docker Desktop](https://docs.docker.com/get-docker/)
- [Kubernetes](https://kubernetes.io/)
  - In Docker Desktop, enable Kubernetes in the settings
  - [Untested] Use [microk8s](https://microk8s.io/) or [minikube](https://minikube.sigs.k8s.io/docs/)

## Usage

```bash
# Generate ssh keys (optional)
./generate-ssh-secret.sh

# Apply all Kubernetes configurations
kubectl apply -f kubernetes/

# Check the status of the pods
kubectl get pods # Make sure all pods are running

# Get the IP addresses of the pods, copy them temporarily
kubectl get pods -o custom-columns="IP:.status.podIP"

# Enter the master pod
kubectl exec -it mpi-worker-0 -- bash

# Create a hostfile
echo "<paste copied ip addresses here>" > hostfile

# Run the MPI program
mpirun --allow-run-as-root \
    --hostfile hostfile \
    -np 4 python3 /app/mpi_sort.py
```