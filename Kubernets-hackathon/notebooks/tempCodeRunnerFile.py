def augment_data(row, counter):
#     if counter % 10 == 0:
#         row["memory_usage_pod"] *= random.uniform(1.3, 1.6)
#         row["oom_kills"] += random.randint(1, 3)
#         row["pod_restarts"] += random.randint(2, 6)
#         row["pending_pods"] += random.randint(3, 8)

#     if counter % 15 == 0:
#         row["packet_drop"] += random.uniform(100, 300)
#         row["tcp_retransmit"] += random.uniform(50, 150)
#         row["network_receive_pod"] *= random.uniform(0.5, 0.8)
#         row["network_transmit_pod"] *= random.uniform(0.5, 0.8)

#     if counter % 20 == 0:
#         row["node_down"] = 1
#         row["node_not_ready"] = 1
#         row["cpu_usage_node"] = min(row["cpu_usage_node"] + random.uniform(30, 50), 100)
#         row["memory_available_node"] = max(row["memory_available_node"] - random.uniform(10, 25), 0)

#     if counter % 30 == 0:
#         row["disk_write"] += random.uniform(1e6, 2e6)
#         row["disk_read"] += random.uniform(0.8e6, 1.5e6)

#     if counter % 40 == 0:
#         row["service_errors"] += random.randint(5, 15)
#         row["filesystem_full"] = 1

#     for key in row:
#         if key not in ["timestamp", "node_down", "node_not_ready", "filesystem_full"]:
#             jitter = random.uniform(-1.0, 1.0)
#             row[key] = max(0, row[key] + jitter)
#     return row