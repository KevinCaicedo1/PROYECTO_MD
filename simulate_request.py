import requests
import random
import time

for _ in range(50):  # 50 requests
    user_id = random.randint(1, 600)  # según tu dataset
    start = time.time()
    res = requests.get(f"http://localhost:8082/recommend/{user_id}")
    latency = time.time() - start
    print(f"User {user_id} - Status: {res.status_code} - Latency: {latency:.2f}s")
