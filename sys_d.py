import platform

print("=== System Information ===")
print("System:", platform.system())
print("Node Name:", platform.node())
print("Release:", platform.release())
print("Version:", platform.version())
print("Machine:", platform.machine())
print("Processor:", platform.processor())

import psutil

print("\n=== CPU Info ===")
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
print("CPU Frequency:", psutil.cpu_freq().current, "MHz")
print("CPU Usage per core:", psutil.cpu_percent(percpu=True, interval=1))
print("Total CPU Usage:", psutil.cpu_percent(), "%")

print("\n=== Memory Info ===")
mem = psutil.virtual_memory()
print("Total:", round(mem.total / (1024 ** 3), 2), "GB")
print("Available:", round(mem.available / (1024 ** 3), 2), "GB")
print("Used:", round(mem.used / (1024 ** 3), 2), "GB")
print("Percentage:", mem.percent, "%")

print("\n=== Disk Info ===")
for partition in psutil.disk_partitions():
    print(f"Device: {partition.device}, Mountpoint: {partition.mountpoint}, File system: {partition.fstype}")
    usage = psutil.disk_usage(partition.mountpoint)
    print("  Total:", round(usage.total / (1024 ** 3), 2), "GB")
    print("  Used:", round(usage.used / (1024 ** 3), 2), "GB")
    print("  Free:", round(usage.free / (1024 ** 3), 2), "GB")
    print("  Percentage:", usage.percent, "%")

print("\n=== Network Info ===")
for name, stats in psutil.net_if_stats().items():
    print(f"Interface: {name}, Is up: {stats.isup}, Speed: {stats.speed} Mbps")
