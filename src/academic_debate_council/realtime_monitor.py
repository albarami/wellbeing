"""
Real-time monitoring of CrewAI execution by capturing verbose output.
This captures stdout/stderr to detect when agents start and complete tasks.
"""

import sys
import io
import threading
import queue
import re
import time
import streamlit as st
from datetime import datetime
from typing import Optional, Dict


class RealTimeCrewMonitor:
    """
    Monitor CrewAI execution in real-time by capturing console output.
    Detects agent activity and task completion from verbose output.
    """
    
    def __init__(self):
        self.output_queue = queue.Queue()
        self.current_agent = None
        self.current_task = None
        self.task_counter = 0
        self.monitoring = False
        
        # Patterns to detect in CrewAI output
        self.patterns = {
            'agent_start': re.compile(r'Working Agent: (.+)'),
            'task_start': re.compile(r'Starting Task: (.+)'),
            'task_output': re.compile(r'Task output: (.+)'),
            'agent_name': re.compile(r'## Agent: (.+)'),
        }
    
    def parse_output_line(self, line: str) -> Optional[Dict]:
        """Parse a line of output and extract agent/task information."""
        line = line.strip()
        
        # Check for agent start
        if 'Working Agent:' in line:
            match = self.patterns['agent_start'].search(line)
            if match:
                agent_name = match.group(1).strip()
                return {'type': 'agent_start', 'agent': agent_name}
        
        # Check for task start
        if 'Starting Task:' in line:
            match = self.patterns['task_start'].search(line)
            if match:
                task_name = match.group(1).strip()
                return {'type': 'task_start', 'task': task_name}
        
        # Check for task completion
        if 'Task output:' in line or 'Final Answer:' in line:
            return {'type': 'task_output', 'output': line}
        
        return None
    
    def capture_output(self, crew, inputs):
        """Run crew and capture output in real-time."""
        # Create string buffers to capture output
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        
        # Save original stdout/stderr
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        try:
            # Custom writer that sends to both original and buffer
            class TeeWriter:
                def __init__(self, original, buffer, queue_obj):
                    self.original = original
                    self.buffer = buffer
                    self.queue_obj = queue_obj
                
                def write(self, text):
                    self.original.write(text)
                    self.buffer.write(text)
                    if text.strip():
                        self.queue_obj.put(('output', text))
                    return len(text)
                
                def flush(self):
                    self.original.flush()
                    self.buffer.flush()
            
            # Redirect stdout/stderr
            sys.stdout = TeeWriter(original_stdout, stdout_buffer, self.output_queue)
            sys.stderr = TeeWriter(original_stderr, stderr_buffer, self.output_queue)
            
            # Run the crew
            result = crew.kickoff(inputs=inputs)
            
            # Signal completion
            self.output_queue.put(('done', result))
            
            return result
            
        finally:
            # Restore original stdout/stderr
            sys.stdout = original_stdout
            sys.stderr = original_stderr
    
    def start_monitoring(self, crew, inputs):
        """Start monitoring crew execution in a background thread."""
        self.monitoring = True
        
        def run_crew():
            self.capture_output(crew, inputs)
        
        thread = threading.Thread(target=run_crew, daemon=True)
        thread.start()
        return thread


def update_chat_from_output(line: str, chat_container) -> bool:
    """
    Update chat interface based on crew output line.
    Returns True if a significant event was detected.
    """
    line = line.strip()
    
    # Detect agent starting work
    if 'Working Agent:' in line:
        # Extract agent name
        match = re.search(r'Working Agent: (.+)', line)
        if match:
            agent_name = match.group(1).strip()
            
            # Show typing indicator
            if 'current_typing_agent' not in st.session_state:
                st.session_state.current_typing_agent = agent_name
                return True
    
    # Detect task completion
    if 'Task output:' in line or ('===' in line and 'output' in line.lower()):
        # Agent finished - clear typing indicator
        if 'current_typing_agent' in st.session_state:
            del st.session_state.current_typing_agent
            return True
    
    return False


def monitor_crew_realtime(crew, inputs, chat_container, progress_placeholder, status_placeholder):
    """
    Monitor crew execution in real-time and update Streamlit UI.
    This function runs the crew and updates the chat interface as agents work.
    """
    import time
    from academic_debate_council.streaming_handler import create_task_mapping
    from academic_debate_council.chat_interface import show_typing_indicator, show_agent_message
    
    # Initialize monitoring
    monitor = RealTimeCrewMonitor()
    
    # Start crew in background thread
    thread = monitor.start_monitoring(crew, inputs)
    
    # Get task mapping
    task_map = create_task_mapping()
    task_list = list(task_map.keys())
    current_task_idx = 0
    
    # Monitor output queue
    last_update = time.time()
    typing_container = st.empty()
    
    while thread.is_alive() or not monitor.output_queue.empty():
        try:
            # Get output with timeout
            msg_type, content = monitor.output_queue.get(timeout=0.5)
            
            if msg_type == 'output':
                # Parse the output line
                parsed = monitor.parse_output_line(content)
                
                if parsed:
                    if parsed['type'] == 'agent_start':
                        # Agent started working
                        agent_name = parsed['agent']
                        st.session_state.current_typing_agent = agent_name
                        
                        # Show typing indicator
                        with typing_container:
                            show_typing_indicator(agent_name, typing_container)
                        
                        # Update status
                        task_info = task_map.get(task_list[current_task_idx], {}) if current_task_idx < len(task_list) else {}
                        with status_placeholder:
                            st.info(f"🔄 Task {current_task_idx + 1}/12: {agent_name} is analyzing...")
                        
                        # Update progress
                        progress = (current_task_idx + 0.5) / 12
                        progress_placeholder.progress(progress)
                    
                    elif parsed['type'] == 'task_output':
                        # Task completed - we'll get the actual output when crew finishes
                        current_task_idx += 1
                        
                        # Clear typing indicator
                        typing_container.empty()
                        
                        # Update progress
                        progress = current_task_idx / 12
                        progress_placeholder.progress(progress)
                
                # Force UI update every 2 seconds
                if time.time() - last_update > 2:
                    st.rerun()
                    last_update = time.time()
            
            elif msg_type == 'done':
                # Crew finished
                typing_container.empty()
                return content
                
        except queue.Empty:
            # No output yet, continue waiting
            # Force UI update if agent is typing
            if 'current_typing_agent' in st.session_state:
                if time.time() - last_update > 3:
                    st.rerun()
                    last_update = time.time()
            continue
    
    return None
