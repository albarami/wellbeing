"""
Streamlit interface for the Academic Debate Council CrewAI application.
Provides real-time streaming output for the multi-agent debate system.
"""

import streamlit as st
import sys
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from academic_debate_council.realtime_chat_executor import (
    execute_realtime_debate,
    execute_realtime_debate_with_streaming
)

# Load environment variables from project root
project_root = Path(__file__).parent.parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Page configuration
st.set_page_config(
    page_title="Academic Debate Council",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .agent-card {
        background: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .task-category {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'crew_running' not in st.session_state:
        st.session_state.crew_running = False
    if 'agent_outputs' not in st.session_state:
        st.session_state.agent_outputs = []
    if 'current_status' not in st.session_state:
        st.session_state.current_status = ""
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'final_output' not in st.session_state:
        st.session_state.final_output = None
    if 'execution_time' not in st.session_state:
        st.session_state.execution_time = None


def render_header():
    """Render the application header."""
    st.markdown('<p class="main-header">🎓 Academic Debate Council</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Multi-Agent AI System for Comprehensive Wellbeing Analysis</p>',
        unsafe_allow_html=True
    )
    
    # Display agent information in expandable section
    with st.expander("ℹ️ About the Expert Panel", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Round 1 Experts:**
            - 🕌 **Sheikh Dr. Ibrahim al-Tazkiyah** - Spiritual Pillar
            - ❤️ **Dr. Layla al-Qalb** - Emotional Pillar
            - 🧠 **Dr. Hassan al-Hikmah** - Intellectual Pillar
            - 💪 **Dr. Fatima al-Jism** - Physical Pillar
            - 🤝 **Dr. Aisha al-Mujtama'** - Social Pillar
            """)
        
        with col2:
            st.markdown("""
            **Debate Facilitation:**
            - ⚖️ **Dr. Yusuf al-Mudeer** - Debate Orchestrator
            - 📊 **Dr. Amira al-Tawhid** - Synthesizer
            
            **Process:**
            1. Round 1: Initial expert analyses
            2. Orchestrator identifies tensions
            3. Round 2: Experts respond to challenges
            4. Final synthesis and recommendations
            """)


def render_input_form():
    """Render the input form for wellbeing topic."""
    st.markdown("---")
    st.subheader("📝 Enter Your Wellbeing Topic")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        topic = st.text_area(
            "Wellbeing Topic to Analyze",
            placeholder="e.g., Social media usage among teenagers, Workplace stress management, Prayer in daily life...",
            height=100,
            help="Enter any wellbeing topic for comprehensive analysis across spiritual, emotional, intellectual, physical, and social dimensions."
        )
    
    with col2:
        language = st.selectbox(
            "Language",
            options=["English", "Arabic"],
            help="The experts will respond in the language you select."
        )
        
        st.markdown("")  # Spacing
        st.markdown("")  # Spacing
        
        run_button = st.button(
            "🚀 Start Analysis",
            type="primary",
            disabled=st.session_state.crew_running or not topic.strip(),
            use_container_width=True
        )
    
    return topic, language, run_button


def render_progress_section():
    """Render the progress tracking section."""
    if st.session_state.crew_running or st.session_state.progress > 0:
        st.markdown("---")
        st.subheader("📊 Analysis Progress")
        
        # Progress bar
        progress_bar = st.progress(st.session_state.progress)
        
        # Current status
        status_placeholder = st.empty()
        if st.session_state.current_status:
            status_placeholder.info(st.session_state.current_status)
        
        return progress_bar, status_placeholder
    
    return None, None


def render_agent_outputs():
    """Render agent outputs organized by category."""
    if not st.session_state.agent_outputs:
        return
    
    st.markdown("---")
    st.subheader("🎯 Expert Analyses")
    
    # Get task mapping
    task_map = create_task_mapping()
    
    # Organize outputs by category
    categories = {}
    for output in st.session_state.agent_outputs:
        task_name = output['task_name']
        if task_name in task_map:
            category = task_map[task_name]['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(output)
    
    # Render each category
    category_order = [
        'Round 1: Initial Analyses',
        'Debate Moderation',
        'Round 2: Expert Responses',
        'Final Synthesis'
    ]
    
    for category in category_order:
        if category in categories:
            st.markdown(f'<div class="task-category">{category}</div>', unsafe_allow_html=True)
            
            for output in categories[category]:
                task_name = output['task_name']
                task_info = task_map.get(task_name, {})
                emoji = task_info.get('emoji', '📄')
                display_name = task_info.get('display_name', task_name)
                agent_name = task_info.get('agent', output['agent_name'])
                
                # Status indicator
                if output['status'] == 'completed':
                    status_icon = '✅'
                elif output['status'] == 'running':
                    status_icon = '🔄'
                else:
                    status_icon = '❌'
                
                # Create expandable section for each task
                with st.expander(
                    f"{status_icon} {emoji} {display_name}",
                    expanded=(output['status'] == 'running' or category == 'Final Synthesis')
                ):
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.caption(f"⏱️ {output['timestamp']}")
                    with col2:
                        st.caption(f"👤 {agent_name}")
                    with col3:
                        st.caption(f"📋 Task {output['task_number']}/12")
                    
                    st.markdown("---")
                    
                    if output['output']:
                        st.markdown(output['output'])
                    else:
                        st.info("⏳ Waiting for output...")


def render_final_output():
    """Render the final comprehensive report."""
    if st.session_state.final_output:
        st.markdown("---")
        st.success("✅ **Analysis Complete!**")
        
        # Display execution time
        if st.session_state.execution_time:
            st.info(f"⏱️ Total execution time: {st.session_state.execution_time:.2f} seconds")
        
        # Download button for the report
        st.download_button(
            label="📥 Download Full Report (Markdown)",
            data=st.session_state.final_output,
            file_name=f"wellbeing_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )


def run_crew_analysis(topic: str, language: str):
    """
    Run the CrewAI analysis with the given topic.
    
    Args:
        topic: The wellbeing topic to analyze
        language: The language for responses (English/Arabic)
    """
    try:
        # Mark as running
        st.session_state.crew_running = True
        st.session_state.agent_outputs = []
        st.session_state.progress = 0
        st.session_state.final_output = None
        
        # Start time
        start_time = datetime.now()
        
        # Create inputs
        inputs = {
            'wellbeing_topic': topic
        }
        
        # Initialize the crew
        crew = AcademicDebateCouncilCrew().crew()
        
        # Create a custom callback to capture task execution
        task_map = create_task_mapping()
        total_tasks = len(task_map)
        
        # Run the crew
        st.info("🚀 Starting multi-agent debate analysis...")
        
        # Since CrewAI doesn't have built-in streaming callbacks that work easily with Streamlit,
        # we'll run the crew and capture output
        result = crew.kickoff(inputs=inputs)
        
        # Calculate execution time
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        st.session_state.execution_time = execution_time
        
        # Store final output
        if hasattr(result, 'raw'):
            st.session_state.final_output = result.raw
        else:
            st.session_state.final_output = str(result)
        
        # Mark all tasks as complete
        st.session_state.progress = 1.0
        st.session_state.current_status = "✅ All tasks completed!"
        
        st.success(f"✅ Analysis completed in {execution_time:.2f} seconds!")
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)
    
    finally:
        st.session_state.crew_running = False


def run_realtime_analysis(topic: str, language: str, use_streaming: bool = False):
    """
    Run the debate with TRUE real-time updates after each agent completes.
    
    Args:
        topic: The wellbeing topic to analyze
        language: Language for responses (English/Arabic)
        use_streaming: If True, use word-by-word streaming; if False, show complete response
    """
    try:
        st.session_state.crew_running = True
        
        # Execute the real-time debate
        if use_streaming:
            result = execute_realtime_debate_with_streaming(topic, language)
        else:
            result = execute_realtime_debate(topic, language)
        
        # Store results in session state
        st.session_state.debate_result = result
        st.session_state.agent_outputs = result['outputs']
        st.session_state.execution_time = result['total_elapsed_seconds']
        
        # Prepare final output for download
        final_text = f"# Academic Debate Council Analysis\n\n"
        final_text += f"**Topic:** {topic}\n\n"
        final_text += f"**Completed:** {result['completion_time']}\n\n"
        final_text += f"**Duration:** {result['total_elapsed_seconds']/60:.1f} minutes\n\n"
        final_text += "---\n\n"
        
        for output in result['outputs']:
            final_text += f"## {output['emoji']} {output['agent_name']}\n"
            final_text += f"*{output['category']} - Task {output['task_number']}/12*\n\n"
            final_text += f"{output['output']}\n\n"
            final_text += "---\n\n"
        
        st.session_state.final_output = final_text
        
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        st.exception(e)
    
    finally:
        st.session_state.crew_running = False


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Render header
    render_header()
    
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        st.error("""
        ⚠️ **Missing API Key!**
        
        Please set your ANTHROPIC_API_KEY in the `.env` file:
        1. Copy `.env.example` to `.env`
        2. Add your Anthropic API key
        3. Restart the application
        """)
        st.stop()
    
    # Render input form
    topic, language, run_button = render_input_form()
    
    # Handle run button click
    if run_button and topic.strip():
        # Run the real-time debate (agents appear one by one!)
        run_realtime_analysis(topic, language, use_streaming=False)
    
    # Show download button if analysis is complete
    if 'final_output' in st.session_state and st.session_state.final_output:
        st.markdown("---")
        st.download_button(
            label="📥 Download Full Report",
            data=st.session_state.final_output,
            file_name=f"debate_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
    
    # Sidebar with information
    with st.sidebar:
        st.header("📚 About")
        st.markdown("""
        **Academic Debate Council** is a sophisticated multi-agent AI system that analyzes 
        wellbeing topics through five expert perspectives:
        
        - **Spiritual** (Islamic framework)
        - **Emotional** (Psychology)
        - **Intellectual** (Learning sciences)
        - **Physical** (Public health)
        - **Social** (Sociology)
        
        The system uses a two-round debate format with an orchestrator who identifies 
        tensions, followed by a synthesizer who integrates all perspectives.
        """)
        
        st.markdown("---")
        
        st.header("⚙️ System Info")
        st.markdown(f"""
        - **Agents:** 7 expert agents
        - **Tasks:** 12 sequential tasks
        - **Models:** Claude Opus 4 & Sonnet 4.5
        - **Status:** {'🔄 Running' if st.session_state.crew_running else '⏸️ Idle'}
        """)
        
        if st.session_state.progress > 0:
            st.metric("Progress", f"{int(st.session_state.progress * 100)}%")
        
        st.markdown("---")
        
        st.header("🔧 Actions")
        if st.button("🔄 Reset Session", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


if __name__ == "__main__":
    main()
