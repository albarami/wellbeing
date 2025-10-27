"""
Simple real-time updates using log file polling.
This works with Streamlit's execution model.
"""

import os
import time
import threading
import re
from pathlib import Path
from datetime import datetime


class SimpleRealtimeMonitor:
    """Monitor CrewAI by tailing a log file."""
    
    def __init__(self, log_file="crew_progress.log"):
        self.log_file = Path(log_file)
        self.current_line = 0
        self.patterns = {
            'agent': re.compile(r'Working Agent: (.+)'),
            'task': re.compile(r'Starting Task: (.+)'),
            'output': re.compile(r'Task output:|Final Answer:'),
        }
    
    def clear_log(self):
        """Clear the log file."""
        if self.log_file.exists():
            self.log_file.unlink()
        self.current_line = 0
    
    def get_new_events(self):
        """Get new events from log file."""
        if not self.log_file.exists():
            return []
        
        events = []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Get new lines
            new_lines = lines[self.current_line:]
            self.current_line = len(lines)
            
            for line in new_lines:
                # Check for agent start
                if match := self.patterns['agent'].search(line):
                    agent = match.group(1).strip()
                    events.append({'type': 'agent_start', 'agent': agent, 'time': datetime.now()})
                
                # Check for task start  
                elif match := self.patterns['task'].search(line):
                    task = match.group(1).strip()
                    events.append({'type': 'task_start', 'task': task, 'time': datetime.now()})
                
                # Check for output
                elif self.patterns['output'].search(line):
                    events.append({'type': 'task_complete', 'time': datetime.now()})
        
        except Exception as e:
            print(f"Error reading log: {e}")
        
        return events


def setup_crew_logging(log_file="crew_progress.log"):
    """
    Setup logging to capture CrewAI output to a file.
    Returns the path to the log file.
    """
    import logging
    import sys
    
    # Create file handler
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # Add to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
    
    # Also capture stdout to file
    class LogToFile:
        def __init__(self, filename):
            self.terminal = sys.stdout
            self.log = open(filename, 'a', encoding='utf-8')
        
        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)
            self.log.flush()
        
        def flush(self):
            self.terminal.flush()
            self.log.flush()
    
    # Redirect stdout
    sys.stdout = LogToFile(log_file)
    
    return Path(log_file).absolute()
