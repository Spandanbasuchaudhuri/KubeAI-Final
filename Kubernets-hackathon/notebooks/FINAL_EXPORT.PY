import prometheus_api_client
from prometheus_api_client import PrometheusConnect
import pandas as pd
import time
from datetime import datetime, timedelta
import random

# Connect to Prometheus
prom = PrometheusConnect(url="http://localhost:9090", disable_ssl=True)

queries = {
    "node_cpu_utilization": '100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)',
    "container_cpu_usage": 'sum(rate(container_cpu_usage_seconds_total[5m]))',
    "node_memory_utilization": '(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100',
    "container_memory_usage": 'sum(container_memory_usage_bytes)',
    "node_disk_read": 'sum(rate(node_disk_read_bytes_total[5m]))',
    "node_disk_write": 'sum(rate(node_disk_written_bytes_total[5m]))',
    "disk_io_time": 'sum(rate(node_disk_io_time_seconds_total[5m]))',
    "network_receive": 'sum(rate(node_network_receive_bytes_total[5m]))',
    "network_transmit": 'sum(rate(node_network_transmit_bytes_total[5m]))',
    "network_drops": 'sum(rate(node_network_receive_drop_total[5m]))',
    "pod_cpu_limits": 'sum(cluster:namespace:pod_cpu:active:kube_pod_container_resource_limits) by (namespace)',
    "pod_cpu_requests": 'sum(cluster:namespace:pod_cpu:active:kube_pod_container_resource_requests) by (namespace)',
    "pod_memory_requests": 'sum(cluster:namespace:pod_memory:active:kube_pod_container_resource_requests) by (namespace)',
    "pod_memory_limits": 'sum(cluster:namespace:pod_memory:active:kube_pod_container_resource_limits) by (namespace)',
    "active_alerts": 'count(ALERTS{alertstate="firing"})',
    "pending_alerts": 'count(ALERTS{alertstate="pending"})',
    "pod_crash_events": 'sum(kube_pod_container_status_restarts_total)',
    "node_failures": 'sum(up == 0)',
    "cpu_manager_errors": 'sum(rate(kubelet_cpu_manager_pinning_errors_total[5m]))',
    "memory_manager_errors": 'sum(rate(kubelet_memory_manager_pinning_errors_total[5m]))'
}

csv_file = "FINAL_EXPORTED.csv"
pd.DataFrame(columns=["timestamp"] + list(queries.keys()) + ["anomaly_label", "anomaly_type"]).to_csv(csv_file, index=False)

print("🟢 Streaming Kubernetes metrics with high-frequency anomalies...")

anomaly_mode = False
anomaly_start = datetime.utcnow()
anomaly_duration = timedelta(seconds=random.randint(15, 45))  # ⏱️ shorter anomaly

while True:
    try:
        current_time = datetime.utcnow()
        row = {"timestamp": current_time}
        label = 0
        anomaly_type = "none"

        # 🔁 Start anomalies more frequently
        if not anomaly_mode and random.random() < 0.4:  # ⚡ 40% chance
            anomaly_mode = True
            anomaly_start = current_time
            anomaly_duration = timedelta(seconds=random.randint(15, 45))  # ⏱️ shorter duration
            anomaly_type = random.choice(["cpu", "memory", "disk", "network", "alert"])
            print(f"⚠️ Synthetic anomaly ({anomaly_type.upper()}) started at {anomaly_start}")

        if anomaly_mode and current_time > (anomaly_start + anomaly_duration):
            anomaly_mode = False
            print(f"✅ Anomaly ended at {current_time}")

        for key, query in queries.items():
            try:
                data = prom.custom_query(query)

                if data and isinstance(data, list):
                    values = [float(d["value"][1]) for d in data if "value" in d]
                    val = sum(values) / len(values) if values else 0

                    if anomaly_mode:
                        if anomaly_type == "cpu" and "cpu" in key:
                            val *= random.uniform(1.5, 2.5)
                            label = 1
                        elif anomaly_type == "memory" and "memory" in key:
                            val *= random.uniform(1.5, 2.5)
                            label = 1
                        elif anomaly_type == "disk" and "disk" in key:
                            val *= random.uniform(2.0, 4.0)
                            label = 1
                        elif anomaly_type == "network" and ("network" in key or "drop" in key):
                            val *= random.uniform(2.0, 4.0)
                            label = 1
                        elif anomaly_type == "alert" and ("alert" in key or "crash" in key or "failures" in key or "errors" in key):
                            val += random.randint(10, 100)
                            label = 1

                    row[key] = round(val, 3)
                else:
                    row[key] = 0
            except Exception as e:
                print(f"[!] Query error for {key}: {e}")
                row[key] = 0

        row["anomaly_label"] = label
        row["anomaly_type"] = anomaly_type

        pd.DataFrame([row]).to_csv(csv_file, mode="a", header=False, index=False)
        print(f"[{row['timestamp']}] Row written. Anomaly: {label}, Type: {anomaly_type}")

        time.sleep(1.0)

    except KeyboardInterrupt:
        print("⛔ Stopped by user.")
        break
