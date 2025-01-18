#!/bin/bash

# Set variables
KEY_NAME="worker_key"
SECRET_NAME="ssh-keys"
OUTPUT_FILE="ssh-secret.yaml"

# Generate SSH key pair
ssh-keygen -t rsa -b 4096 -f "$KEY_NAME" -N "" -C "k8s-worker@cluster"

# Base64 encode the keys
PRIVATE_KEY=$(cat "${KEY_NAME}" | base64 -w 0)
PUBLIC_KEY=$(cat "${KEY_NAME}.pub" | base64 -w 0)

# Create Secret manifest
cat > "$OUTPUT_FILE" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: ${SECRET_NAME}
type: Opaque
data:
  ssh-privatekey: ${PRIVATE_KEY}
  ssh-publickey: ${PUBLIC_KEY}
  authorized_keys: ${PUBLIC_KEY}
EOF

rm "worker_key" "worker_key.pub"
mv "$OUTPUT_FILE" "kubernetes/$OUTPUT_FILE"

echo "Secret configuration has been generated in ${OUTPUT_FILE}"
echo "You can apply it using: kubectl apply -f ${OUTPUT_FILE}"
