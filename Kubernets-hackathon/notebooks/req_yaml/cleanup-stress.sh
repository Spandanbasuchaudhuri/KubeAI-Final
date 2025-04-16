#!/bin/bash
kubectl delete -f stress_files/ --namespace=monitoring --ignore-not-found
echo "🧹 Stressors deleted from 'monitoring' namespace."
