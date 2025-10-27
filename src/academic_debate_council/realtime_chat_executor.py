"""
Real-Time Chat Executor
Runs agents sequentially, updating UI after EACH agent completes.
"""

import streamlit as st
import time
from datetime import datetime
from typing import List, Dict
from academic_debate_council.direct_chat_agents import DebateAgentsManager
from academic_debate_council.chat_interface import (
    show_section_header,
    show_typing_indicator,
    show_agent_message,
    get_agent_avatar
)


def execute_realtime_debate(topic: str, language: str = "English") -> Dict:
    """
    Execute the 12-agent debate in real-time with UI updates after each completion.
    
    Args:
        topic: The wellbeing topic to analyze
        language: Language for responses (English/Arabic)
    
    Returns:
        Dictionary with all outputs and metadata
    """
    
    # Initialize the agents manager
    manager = DebateAgentsManager()
    
    # Track all outputs
    all_outputs = []
    context_history = []  # Running context for agents
    
    # Create main chat container
    chat_container = st.container()
    
    # Create progress and status containers
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_container = st.empty()
    with col2:
        status_container = st.empty()
    
    # Show user question at top
    with chat_container:
        with st.chat_message("user", avatar="🤔"):
            st.markdown(f"**Your Question:**\n\n{topic}")
    
    # Track section headers shown
    sections_shown = set()
    
    start_time = time.time()
    
    # Execute each of the 12 tasks
    for task_num in range(1, 13):
        # Get task information
        task_info = manager.get_task_info(task_num)
        agent_key = task_info['agent_key']
        task_name = task_info['task_name']
        emoji = task_info['emoji']
        category = task_info['category']
        
        # Get agent and task description
        agent = manager.get_agent_for_task(task_num)
        agent_display_name = manager.get_agent_display_name(agent_key)
        task_description = manager.get_task_description(task_name)
        
        # Show section header if new category
        if category not in sections_shown:
            with chat_container:
                if category == 'Round 1':
                    show_section_header("Round 1: Initial Expert Analyses", "🎯", st.container())
                elif category == 'Moderation':
                    show_section_header("Debate Moderation", "⚖️", st.container())
                elif category == 'Round 2':
                    show_section_header("Round 2: Expert Responses", "💬", st.container())
                elif category == 'Synthesis':
                    show_section_header("Final Synthesis", "📊", st.container())
            sections_shown.add(category)
        
        # Update progress
        progress = (task_num - 1) / 12
        progress_container.progress(progress, text=f"Task {task_num}/12")
        
        # Create a placeholder for this agent's message
        message_placeholder = st.empty()
        
        # Show agent starting to work
        with message_placeholder.container():
            with st.chat_message("assistant", avatar=emoji):
                st.markdown(f"**{agent_display_name}**")
                with st.spinner(f"Analyzing {category.lower()}..."):
                    # This is where the ACTUAL work happens
                    task_start = time.time()
                    
                    # Execute the task (blocks until complete)
                    response = agent.execute_task(
                        topic=topic,
                        task_description=task_description,
                        context=context_history,
                        temperature=0.3
                    )
                    
                    task_elapsed = time.time() - task_start
        
        # Clear the spinner and show the actual response
        with message_placeholder.container():
            with st.chat_message("assistant", avatar=emoji):
                st.markdown(f"**{agent_display_name}**")
                st.markdown(f"*Task {task_num}/12 • {category} • {task_elapsed:.1f}s*")
                st.markdown("---")
                st.markdown(response)
        
        # Update status
        status_container.success(f"✅ {task_num}/12")
        
        # Store the output
        output_entry = {
            'task_number': task_num,
            'task_name': task_name,
            'agent_name': agent_display_name,
            'agent_key': agent_key,
            'category': category,
            'emoji': emoji,
            'output': response,
            'elapsed_seconds': task_elapsed,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        all_outputs.append(output_entry)
        
        # Add to context for next agents
        # Include agent name and response
        context_entry = f"**{agent_display_name}** ({category}, Task {task_num}):\n{response}"
        context_history.append(context_entry)
        
        # Optional: Brief pause for UI update (helps with perceived responsiveness)
        time.sleep(0.1)
    
    # Final progress update
    progress_container.progress(1.0, text="Complete!")
    
    # Calculate total time
    total_elapsed = time.time() - start_time
    
    # Show completion message
    status_container.success(f"✅ Done!")
    
    with chat_container:
        st.success(f"🎉 **Analysis Complete!** All 12 agents completed in {total_elapsed/60:.1f} minutes")
    
    # Return all outputs
    return {
        'topic': topic,
        'language': language,
        'outputs': all_outputs,
        'total_elapsed_seconds': total_elapsed,
        'total_tasks': 12,
        'completion_time': datetime.now().isoformat()
    }


def execute_realtime_debate_with_streaming(topic: str, language: str = "English") -> Dict:
    """
    Execute debate with STREAMING responses (word-by-word).
    
    This version streams each response as it's generated for maximum real-time feel.
    
    Args:
        topic: The wellbeing topic
        language: Language for responses
    
    Returns:
        Dictionary with all outputs
    """
    
    manager = DebateAgentsManager()
    all_outputs = []
    context_history = []
    
    chat_container = st.container()
    
    col1, col2 = st.columns([3, 1])
    with col1:
        progress_container = st.empty()
    with col2:
        status_container = st.empty()
    
    # User question
    with chat_container:
        with st.chat_message("user", avatar="🤔"):
            st.markdown(f"**Your Question:**\n\n{topic}")
    
    sections_shown = set()
    start_time = time.time()
    
    for task_num in range(1, 13):
        task_info = manager.get_task_info(task_num)
        agent_key = task_info['agent_key']
        task_name = task_info['task_name']
        emoji = task_info['emoji']
        category = task_info['category']
        
        agent = manager.get_agent_for_task(task_num)
        agent_display_name = manager.get_agent_display_name(agent_key)
        task_description = manager.get_task_description(task_name)
        
        # Show section headers
        if category not in sections_shown:
            with chat_container:
                if category == 'Round 1':
                    show_section_header("Round 1: Initial Expert Analyses", "🎯", st.container())
                elif category == 'Moderation':
                    show_section_header("Debate Moderation", "⚖️", st.container())
                elif category == 'Round 2':
                    show_section_header("Round 2: Expert Responses", "💬", st.container())
                elif category == 'Synthesis':
                    show_section_header("Final Synthesis", "📊", st.container())
            sections_shown.add(category)
        
        progress = (task_num - 1) / 12
        progress_container.progress(progress, text=f"Task {task_num}/12")
        
        # Create message container
        with chat_container:
            with st.chat_message("assistant", avatar=emoji):
                st.markdown(f"**{agent_display_name}**")
                st.markdown(f"*Task {task_num}/12 • {category}*")
                st.markdown("---")
                
                # Stream the response
                response_placeholder = st.empty()
                full_response = ""
                
                task_start = time.time()
                
                # Stream chunks as they arrive
                for chunk in agent.execute_task_streaming(
                    topic=topic,
                    task_description=task_description,
                    context=context_history,
                    temperature=0.3
                ):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")  # Cursor effect
                
                # Remove cursor
                response_placeholder.markdown(full_response)
                
                task_elapsed = time.time() - task_start
        
        status_container.success(f"✅ {task_num}/12")
        
        # Store output
        output_entry = {
            'task_number': task_num,
            'task_name': task_name,
            'agent_name': agent_display_name,
            'output': full_response,
            'elapsed_seconds': task_elapsed,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        all_outputs.append(output_entry)
        
        # Add to context
        context_entry = f"**{agent_display_name}** ({category}, Task {task_num}):\n{full_response}"
        context_history.append(context_entry)
    
    progress_container.progress(1.0, text="Complete!")
    total_elapsed = time.time() - start_time
    status_container.success(f"✅ Done!")
    
    with chat_container:
        st.success(f"🎉 **Analysis Complete!** {total_elapsed/60:.1f} minutes")
    
    return {
        'topic': topic,
        'outputs': all_outputs,
        'total_elapsed_seconds': total_elapsed,
        'completion_time': datetime.now().isoformat()
    }
