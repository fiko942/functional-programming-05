import time

data = list(range(100000))

# Do-While loop (simulated)
start_time = time.time()
i = 0
while True:
    # Simulate do-while
    _ = data[i]
    i += 1
    if not (i < len(data)):
        break
end_time = time.time()
print(f"Do-While loop: {(end_time - start_time) * 1000:.4f} ms")

# While loop
start_time = time.time()
i = 0
while i < len(data):
    _ = data[i]
    i += 1
end_time = time.time()
print(f"While loop: {(end_time - start_time) * 1000:.4f} ms")

# For loop
start_time = time.time()
for i in range(len(data)):
    _ = data[i]
end_time = time.time()
print(f"For loop: {(end_time - start_time) * 1000:.4f} ms")

# Foreach loop
start_time = time.time()
for item in data:
    _ = item
end_time = time.time()
print(f"Foreach loop: {(end_time - start_time) * 1000:.4f} ms")