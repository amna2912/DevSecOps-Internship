import requests
import time
import random

print("=" * 50)
print("TRAFFIC GENERATOR FOR FLASK APP")
print("Hitting endpoints every 5-10 seconds...")
print("=" * 50)

while True:
    try:
        # Home page
        requests.get('http://localhost:5000/')
        
        # Login (30% fail chance in app)
        requests.post('http://localhost:5000/login', json={'username': f'user{random.randint(1,10)}'})
        
        # Products (10% error chance)
        requests.get('http://localhost:5000/products')
        
        # Generate logs
        requests.get('http://localhost:5000/generate_logs')
        
        # Status
        requests.get('http://localhost:5000/status')
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Traffic sent!")
        
    except Exception as e:
        print(f"Error sending traffic: {e} (Flask might not be running yet)")
    
    # Random sleep 5-10s
    time.sleep(random.uniform(5, 10))