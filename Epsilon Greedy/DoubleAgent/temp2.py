import psutil
import numpy as np
import os

# Get initial memory usage
mem = psutil.virtual_memory()
print(f"Total RAM: {mem.total / (1024 ** 3):.2f} GB")
print(f"Available RAM Before: {mem.available / (1024 ** 3):.2f} GB")

process = psutil.Process(os.getpid())
print(f"Python RAM Usage Before: {process.memory_info().rss / (1024 ** 3):.2f} GB")

# Define full Q-tables (non-sparse)
Q_table_1 = np.random.rand(500, 500, 1000, 5).astype(np.float64)
Q_table_2 = np.random.rand(500, 500, 1000, 5).astype(np.float64)
Q_table_3 = np.random.rand(500, 500, 1000, 5).astype(np.float64)
Q_table_4 = np.random.rand(500, 500, 1000, 5).astype(np.float64)

# Access some elements to force memory allocation
Q_table_1[0, 0, 0, 0] = 1.0
Q_table_2[0, 0, 0, 0] = 1.0
Q_table_3[0, 0, 0, 0] = 1.0
Q_table_4[0, 0, 0, 0] = 1.0

# Get memory usage after allocation
mem = psutil.virtual_memory()
print(f"Available RAM After: {mem.available / (1024 ** 3):.2f} GB")
print(f"Python RAM Usage After: {process.memory_info().rss / (1024 ** 3):.2f} GB")

# Print actual memory size of each Q-table
print(f"Size of Q_table_1: {Q_table_1.nbytes / (1024 ** 3):.2f} GB")
print(f"Total Q-table Memory: {(Q_table_1.nbytes * 4) / (1024 ** 3):.2f} GB")
