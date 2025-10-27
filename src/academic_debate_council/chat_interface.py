"""
Chat-like interface for displaying agent outputs in real-time.
Shows agents typing and then their responses like a group chat.
"""

import streamlit as st
import time
from typing import Dict, Any


def get_agent_avatar(agent_name: str) -> str:
    """Get emoji avatar for each agent."""
    avatars = {
        'Sheikh Dr. Ibrahim al-Tazkiyah': '🕌',
        'Dr. Layla al-Qalb': '❤️',
        'Dr. Hassan al-Hikmah': '🧠',
        'Dr. Fatima al-Jism': '💪',
        'Dr. Aisha al-Mujtama\'': '🤝',
        'Dr. Yusuf al-Mudeer': '⚖️',
        'Dr. Amira al-Tawhid': '📊'
    }
    return avatars.get(agent_name, '👤')


def get_agent_short_name(agent_name: str) -> str:
    """Get short display name for agent."""
    short_names = {
        'Sheikh Dr. Ibrahim al-Tazkiyah': 'Sheikh al-Tazkiyah',
        'Dr. Layla al-Qalb': 'Dr. al-Qalb',
        'Dr. Hassan al-Hikmah': 'Dr. al-Hikmah',
        'Dr. Fatima al-Jism': 'Dr. al-Jism',
        'Dr. Aisha al-Mujtama\'': 'Dr. al-Mujtama\'',
        'Dr. Yusuf al-Mudeer': 'Dr. al-Mudeer',
        'Dr. Amira al-Tawhid': 'Dr. al-Tawhid'
    }
    return short_names.get(agent_name, agent_name)


def show_typing_indicator(agent_name: str, container):
    """Display typing indicator for an agent."""
    avatar = get_agent_avatar(agent_name)
    short_name = get_agent_short_name(agent_name)
    
    typing_html = f"""
    <div style="background: #f0f2f6; border-radius: 15px; padding: 12px 18px; margin: 8px 0; max-width: 200px; border-left: 4px solid #667eea;">
        <div style="font-weight: bold; color: #667eea; margin-bottom: 4px;">
            {avatar} {short_name}
        </div>
        <div style="color: #666; font-style: italic;">
            typing<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
        </div>
    </div>
    """
    
    with container:
        st.markdown(typing_html, unsafe_allow_html=True)


def show_agent_message(agent_name: str, message: str, task_number: int, container):
    """Display agent message in chat bubble format."""
    avatar = get_agent_avatar(agent_name)
    short_name = get_agent_short_name(agent_name)
    preview = message[:500]
    ellipsis = "..." if len(message) > 500 else ""
    
    message_html = f'<div style="background: white; border-radius: 15px; padding: 16px 20px; margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 4px solid #667eea;"><div style="font-weight: bold; color: #667eea; margin-bottom: 8px;"><span style="font-size: 1.3em;">{avatar}</span> {short_name} <span style="background: #667eea; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75em; float: right;">Task {task_number}/12</span></div><div style="color: #333; line-height: 1.6; white-space: pre-wrap;">{preview}{ellipsis}</div></div>'
    
    with container:
        st.markdown(message_html, unsafe_allow_html=True)
        if len(message) > 500:
            with st.expander("📖 Read Full Response"):
                st.markdown(message)


def show_user_question(question: str, container):
    """Display the user's question in chat format."""
    question_html = f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 16px 20px; margin: 12px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.15);"><div style="font-weight: bold; margin-bottom: 8px;"><span style="font-size: 1.3em;">🤔</span> Your Question</div><div style="line-height: 1.6;">{question}</div></div>'
    with container:
        st.markdown(question_html, unsafe_allow_html=True)


def show_section_header(title: str, emoji: str, container):
    """Show a section header in the chat (e.g., Round 1, Round 2)."""
    header_html = f'<div style="text-align: center; margin: 24px 0 16px 0;"><div style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 8px 24px; border-radius: 20px; font-weight: bold; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">{emoji} {title}</div></div>'
    with container:
        st.markdown(header_html, unsafe_allow_html=True)


def initialize_chat_session():
    """Initialize chat session state."""
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'current_agent_typing' not in st.session_state:
        st.session_state.current_agent_typing = None
    if 'chat_container' not in st.session_state:
        st.session_state.chat_container = None
