"""
Streaming callback handler for CrewAI to Streamlit integration.
Captures agent outputs and streams them to Streamlit in real-time.
"""

import streamlit as st
from typing import Any, Dict, Optional
from datetime import datetime


class StreamlitCallbackHandler:
    """
    Custom callback handler to capture CrewAI agent outputs and stream them to Streamlit.
    Compatible with CrewAI's callback system.
    """
    
    def __init__(self, progress_placeholder=None, status_placeholder=None, output_container=None):
        """Initialize the streaming handler with session state and placeholders."""
        self.current_agent = None
        self.current_task = None
        self.task_counter = 0
        self.total_tasks = 12
        self.progress_placeholder = progress_placeholder
        self.status_placeholder = status_placeholder
        self.output_container = output_container
        
        # Initialize session state for outputs if not exists
        if 'agent_outputs' not in st.session_state:
            st.session_state.agent_outputs = []
        if 'current_status' not in st.session_state:
            st.session_state.current_status = ""
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
    
    def on_task_start(self, task: Any) -> None:
        """Called when a task starts - CrewAI callback."""
        task_name = getattr(task, 'description', 'Unknown Task')[:50]
        agent_name = getattr(task, 'agent', None)
        if agent_name:
            agent_name = getattr(agent_name, 'role', 'Unknown Agent')
        else:
            agent_name = 'Unknown Agent'
        
        self.task_counter += 1
        self.current_task = task_name
        self.current_agent = agent_name
        
        # Update progress
        progress = self.task_counter / self.total_tasks
        st.session_state.progress = progress
        
        # Update status
        status_msg = f"🔄 **Task {self.task_counter}/{self.total_tasks}:** {agent_name}"
        st.session_state.current_status = status_msg
        
        # Update UI placeholders
        if self.progress_placeholder:
            self.progress_placeholder.progress(progress)
        if self.status_placeholder:
            self.status_placeholder.info(status_msg)
        
        # Create new output entry
        output_entry = {
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'task_number': self.task_counter,
            'task_name': task_name,
            'agent_name': agent_name,
            'output': "",
            'status': 'running'
        }
        st.session_state.agent_outputs.append(output_entry)
        
        # Force UI update
        if self.output_container:
            with self.output_container:
                st.rerun()
    
    def on_task_end(self, output: Any) -> None:
        """Called when a task ends - CrewAI callback."""
        if self.task_counter > 0 and st.session_state.agent_outputs:
            # Get output text
            output_text = str(output.raw) if hasattr(output, 'raw') else str(output)
            
            # Mark current task as complete
            current_output = st.session_state.agent_outputs[-1]
            current_output['status'] = 'completed'
            current_output['output'] = output_text
            
            # Update status
            status_msg = f"✅ **Completed {self.task_counter}/{self.total_tasks}:** {current_output['agent_name']}"
            st.session_state.current_status = status_msg
            
            if self.status_placeholder:
                self.status_placeholder.success(status_msg)


class StreamToStreamlit:
    """
    Context manager to capture and stream CrewAI output to Streamlit.
    """
    
    def __init__(self, container):
        """
        Initialize with a Streamlit container to write to.
        
        Args:
            container: Streamlit container for output display
        """
        self.container = container
        self.output_buffer = []
    
    def write(self, text: str):
        """Capture text output."""
        if text and text.strip():
            self.output_buffer.append(text)
            # Update container with buffered output
            with self.container:
                st.text(text)
    
    def flush(self):
        """Flush the buffer."""
        pass
    
    def get_output(self) -> str:
        """Get all captured output as a single string."""
        return "\n".join(self.output_buffer)


def create_task_mapping():
    """
    Create a mapping of task names to user-friendly display names and categories.
    
    Returns:
        dict: Mapping of task names to display information
    """
    return {
        'spiritual_analysis': {
            'display_name': 'Spiritual Analysis (Sheikh al-Tazkiyah)',
            'category': 'Round 1: Initial Analyses',
            'order': 1,
            'agent': 'Sheikh Dr. Ibrahim al-Tazkiyah',
            'emoji': '🕌'
        },
        'emotional_analysis': {
            'display_name': 'Emotional Analysis (Dr. al-Qalb)',
            'category': 'Round 1: Initial Analyses',
            'order': 2,
            'agent': 'Dr. Layla al-Qalb',
            'emoji': '❤️'
        },
        'intellectual_analysis': {
            'display_name': 'Intellectual Analysis (Dr. al-Hikmah)',
            'category': 'Round 1: Initial Analyses',
            'order': 3,
            'agent': 'Dr. Hassan al-Hikmah',
            'emoji': '🧠'
        },
        'physical_analysis': {
            'display_name': 'Physical Analysis (Dr. al-Jism)',
            'category': 'Round 1: Initial Analyses',
            'order': 4,
            'agent': 'Dr. Fatima al-Jism',
            'emoji': '💪'
        },
        'social_analysis': {
            'display_name': 'Social Analysis (Dr. al-Mujtama)',
            'category': 'Round 1: Initial Analyses',
            'order': 5,
            'agent': 'Dr. Aisha al-Mujtama',
            'emoji': '🤝'
        },
        'orchestrator_analysis_question_assignment': {
            'display_name': 'Orchestrator Analysis & Questions',
            'category': 'Debate Moderation',
            'order': 6,
            'agent': 'Dr. Yusuf al-Mudeer',
            'emoji': '⚖️'
        },
        'emotional_agent_response_to_orchestrator': {
            'display_name': 'Emotional Expert Response',
            'category': 'Round 2: Expert Responses',
            'order': 7,
            'agent': 'Dr. Layla al-Qalb',
            'emoji': '❤️'
        },
        'intellectual_agent_response_to_orchestrator': {
            'display_name': 'Intellectual Expert Response',
            'category': 'Round 2: Expert Responses',
            'order': 8,
            'agent': 'Dr. Hassan al-Hikmah',
            'emoji': '🧠'
        },
        'physical_agent_response_to_orchestrator': {
            'display_name': 'Physical Expert Response',
            'category': 'Round 2: Expert Responses',
            'order': 9,
            'agent': 'Dr. Fatima al-Jism',
            'emoji': '💪'
        },
        'social_agent_response_to_orchestrator': {
            'display_name': 'Social Expert Response',
            'category': 'Round 2: Expert Responses',
            'order': 10,
            'agent': 'Dr. Aisha al-Mujtama',
            'emoji': '🤝'
        },
        'spiritual_agent_response_to_orchestrator': {
            'display_name': 'Spiritual Expert Response',
            'category': 'Round 2: Expert Responses',
            'order': 11,
            'agent': 'Sheikh Dr. Ibrahim al-Tazkiyah',
            'emoji': '🕌'
        },
        'integrated_wellbeing_assessment': {
            'display_name': 'Integrated Wellbeing Assessment',
            'category': 'Final Synthesis',
            'order': 12,
            'agent': 'Dr. Amira al-Tawhid',
            'emoji': '📊'
        }
    }
