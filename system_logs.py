import pythoncom
import win32evtlog
import json
import time
from datetime import datetime
import socket
import logging
import os

def setup_system_logger():
    """Set up logging for system events"""
    logger = logging.getLogger('system_logs')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Remove existing handlers
    if logger.handlers:
        logger.handlers = []
    
    # File handler with proper encoding (appends by default)
    file_handler = logging.FileHandler('system.log', encoding='utf-8')
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

def escape_json_string(s):
    """Escape special characters for JSON"""
    if not s:
        return ""
    
    # First convert to string if it's not already
    s = str(s)
    
    # Escape backslashes first
    s = s.replace('\\', '\\\\')
    
    # Escape other JSON special characters
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    
    return s

def collect_system_logs():
    """Collect Windows system logs and write to a file"""
    hostname = socket.gethostname()
    logger = setup_system_logger()
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Collecting system logs...")
    
    # Initialize COM for Windows event log
    pythoncom.CoInitialize()
    
    # Read from multiple log sources
    log_types = ["Application", "System"]
    
    for log_type in log_types:
        try:
            hand = win32evtlog.OpenEventLog(None, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            
            # Read recent events
            events = win32evtlog.ReadEventLog(hand, flags, 0, 20)
            
            if events:
                print(f"  Found {len(events)} events in {log_type} logs")
                
                for event in events:
                    try:
                        # Extract message safely
                        message = "No message"
                        if event.StringInserts and len(event.StringInserts) > 0:
                            message_parts = []
                            for insert in event.StringInserts:
                                if insert:
                                    try:
                                        message_parts.append(str(insert))
                                    except:
                                        continue
                            message = ' '.join(message_parts)[:300]  # Limit length
                        
                        # ESCAPE THE MESSAGE PROPERLY for JSON
                        message = escape_json_string(message)
                        
                        # Determine log level
                        level = 'info'
                        if hasattr(event, 'EventType'):
                            if event.EventType == win32evtlog.EVENTLOG_ERROR_TYPE:
                                level = 'error'
                            elif event.EventType == win32evtlog.EVENTLOG_WARNING_TYPE:
                                level = 'warning'
                        
                        log_data = {
                            'timestamp': datetime.fromtimestamp(event.TimeGenerated.timestamp()).isoformat(),
                            'level': level,
                            'message': message,
                            'source': 'windows_system',
                            'hostname': hostname,
                            'event_id': event.EventID,
                            'event_category': event.EventCategory,
                            'event_type': log_type
                        }
                        
                        # Convert to JSON and log (ensure proper JSON)
                        json_str = json.dumps(log_data, ensure_ascii=False)
                        logger.info(json_str)
                        
                    except Exception as e:
                        print(f"Error processing event: {e}")
                        continue
            else:
                print(f"  No events found in {log_type} logs")
            
            win32evtlog.CloseEventLog(hand)
            
        except Exception as e:
            print(f"Could not access {log_type} logs: {e}")
            continue
    
    pythoncom.CoUninitialize()
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] System logs collected!")

if __name__ == '__main__':
    print("=" * 50)
    print("WINDOWS SYSTEM LOG COLLECTOR (FIXED JSON)")
    print("=" * 50)
    
    # NO DELETION - Append to existing file
    
    # Run once (or in loop via batch)
    collect_system_logs()