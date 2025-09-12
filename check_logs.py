import json

def check_log_file(filename):
    print(f"Checking {filename}...")
    print("=" * 50)
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
        print(f"Total lines: {len(lines)}")
        
        for i, line in enumerate(lines[-5:]):  # Check last 5 lines
            print(f"Line {len(lines)-5+i}: {line.strip()}")
            
            try:
                data = json.loads(line.strip())
                print(f"  ✓ Valid JSON: {data.get('source', 'Unknown source')}")
            except json.JSONDecodeError:
                print(f"  ✗ INVALID JSON - This might be the problem!")
                
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"Error: {e}")
    
    print("=" * 50)

# Check both log files
check_log_file('system.log')
check_log_file('app.log')