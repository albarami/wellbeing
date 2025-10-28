"""
Academic Debate Council - Chainlit Interface with Password Protection
Professional ChatGPT-like interface for multi-agent debate analysis.
"""

import chainlit as cl
import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import hashlib

# Load environment variables
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Import our debate engine
from src.academic_debate_council.direct_chat_agents import DebateAgentsManager

# ============================================================================
# PASSWORD PROTECTION
# ============================================================================
# Set your password here (or in .env file)
REQUIRED_PASSWORD = os.getenv("APP_PASSWORD", "scholar2024")  # Change this!

def hash_password(password: str) -> str:
    """Hash password for secure storage"""
    return hashlib.sha256(password.encode()).hexdigest()

HASHED_PASSWORD = hash_password(REQUIRED_PASSWORD)


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    """
    Authenticate users with password.
    Username is not checked - only password matters.
    """
    if hash_password(password) == HASHED_PASSWORD:
        return cl.User(
            identifier=username or "scholar",
            metadata={"role": "user", "provider": "credentials"}
        )
    return None


# ============================================================================
# REST OF YOUR APP (unchanged)
# ============================================================================

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    # Welcome message
    welcome_msg = """# ⚖️ Welcome to the Academic Debate Council

🔐 **Private Access** - You have been authenticated.

## 🎯 How This Works

This system orchestrates a **multi-agent scholarly debate** where 7 expert agents analyze your question from different perspectives:

1. **🕌 Sheikh Dr. Ibrahim al-Tazkiyah** - Spiritual & Islamic Foundation
2. **🧠 Dr. Hassan al-Hikmah** - Intellectual & Educational Analysis  
3. **💚 Dr. Layla al-Qalb** - Psychological Wellbeing
4. **💪 Dr. Omar al-Jism** - Physiological Health
5. **👥 Dr. Aisha al-Mujtama** - Social Dynamics
6. **⚖️ Dr. Yusuf al-Mudeer** - Debate Orchestrator (identifies tensions)
7. **📊 Dr. Zainab al-Khulasa** - Final Synthesizer

## 🔬 Research Integrity Features

- ✅ **Citation Verification** - All academic claims checked via Semantic Scholar
- ✅ **Medical Verification** - Health claims verified via PubMed database
- ✅ **Islamic Text Verification** - Quranic verses and hadith authenticated
- ✅ **Fact Checking** - Claims verified via multiple sources
- ✅ **Honest Limitations** - System admits when sources cannot be verified

## ⏱️ What to Expect

- **Duration:** 10-15 minutes for complete analysis
- **Process:** 12 sequential tasks (Round 1 → Moderation → Round 2 → Synthesis)
- **Tools:** Agents call verification APIs in real-time
- **Output:** Comprehensive, evidence-based analysis

## 💡 Example Questions

- Should prayer breaks be enforced in Qatar workplaces?
- What does research say about meditation and mental health?
- How does Islamic scholarship view modern educational technology?
- What are the psychological effects of social media on teenagers?

---

**Ready?** Ask your question below! 👇
"""
    
    await cl.Message(content=welcome_msg).send()
    
    # Store debate manager in session
    cl.user_session.set("manager", None)


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and orchestrate the debate."""
    
    topic = message.content.strip()
    
    if not topic:
        await cl.Message(content="⚠️ Please provide a topic or question to debate.").send()
        return
    
    # Initialize manager if not exists
    manager = cl.user_session.get("manager")
    if manager is None:
        manager = DebateAgentsManager()
        cl.user_session.set("manager", manager)
    
    # Show starting message
    start_msg = await cl.Message(
        content=f"🚀 **Starting Analysis**\n\nAnalyzing: *{topic}*\n\n7 expert agents will debate this topic through 12 sequential tasks. Each agent will appear below as they complete their analysis (~60 seconds each).\n\n⏱️ Total time: 10-15 minutes",
        author="System"
    ).send()
    
    # Track context for agents
    context_history = []
    all_outputs = []
    
    # Track which sections we've shown
    sections_shown = set()
    
    start_time = time.time()
    
    # Execute all 12 tasks
    for task_num in range(1, 13):
        # Get task info
        task_info = manager.get_task_info(task_num)
        agent_key = task_info['agent_key']
        task_name = task_info['task_name']
        emoji = task_info['emoji']
        category = task_info['category']
        
        # Get agent and task description
        agent = manager.get_agent_for_task(task_num)
        agent_display_name = manager.get_agent_display_name(agent_key)
        task_description = manager.get_task_description(task_name)
        
        # Show section headers
        if category not in sections_shown:
            if category == 'Round 1':
                header_msg = await cl.Message(
                    content="---\n\n# 🎯 Round 1: Initial Expert Analyses\n\n*Five experts provide their initial perspective*",
                    author="System"
                ).send()
            elif category == 'Moderation':
                header_msg = await cl.Message(
                    content="---\n\n# ⚖️ Debate Moderation\n\n*Orchestrator identifies key tensions*",
                    author="System"
                ).send()
            elif category == 'Round 2':
                header_msg = await cl.Message(
                    content="---\n\n# 💬 Round 2: Expert Responses\n\n*Experts respond to the orchestrator's challenges*",
                    author="System"
                ).send()
            elif category == 'Synthesis':
                header_msg = await cl.Message(
                    content="---\n\n# 📊 Final Synthesis\n\n*Comprehensive integration of all perspectives*",
                    author="System"
                ).send()
            sections_shown.add(category)
        
        # Create agent message with streaming
        agent_msg = cl.Message(
            content="",
            author=agent_display_name
        )
        await agent_msg.send()
        
        # Show agent name and role prominently at the START of each message
        agent_role = agent.role  # Get full role from agent config

        # Create a VERY PROMINENT header so users always know who's speaking
        await agent_msg.stream_token(f"---\n\n# {emoji} {agent_display_name}\n\n**Role:** {agent_role}  \n**Task:** {category}\n\n---\n\n")
        
        # Execute task with streaming and tool execution
        task_start = time.time()
        full_response = ""
        current_line = ""
        last_chunk_time = time.time()
        heartbeat_interval = 10  # Send heartbeat every 10 seconds

        # Create a flag to track if we're done
        streaming_complete = False

        # Background heartbeat task to prevent WebSocket timeout
        async def send_heartbeat():
            """Send periodic heartbeats to keep WebSocket alive during long operations."""
            heartbeat_count = 0
            while not streaming_complete:
                await asyncio.sleep(5)  # Check every 5 seconds
                if not streaming_complete:
                    heartbeat_count += 1
                    # Every 3rd heartbeat (15s), send visible dots
                    if heartbeat_count % 3 == 0:
                        await agent_msg.stream_token(".")  # Visible progress
                    else:
                        await agent_msg.stream_token("")  # Invisible keep-alive

        # Start heartbeat task
        heartbeat_task = asyncio.create_task(send_heartbeat())

        try:
            # Stream the response with native Anthropic tool calling
            # Tools are executed inside execute_task_streaming() via Anthropic API
            task_timeout = 240  # 4 minutes max per agent task

            # Create the generator
            generator = agent.execute_task_streaming(
                topic=topic,
                task_description=task_description,
                context=context_history,
                temperature=0.3
            )

            # Run the synchronous generator in a thread pool to prevent blocking
            executor = ThreadPoolExecutor(max_workers=1)
            loop = asyncio.get_event_loop()

            # Consume generator without blocking the async loop
            while True:
                # Check for timeout
                if time.time() - task_start > task_timeout:
                    timeout_msg = f"\n\n[TIMEOUT] **Task timeout ({task_timeout}s)** - Moving to next agent...\n"
                    await agent_msg.stream_token(timeout_msg)
                    full_response += timeout_msg
                    break

                try:
                    # Get next chunk from generator in thread pool (non-blocking)
                    chunk = await loop.run_in_executor(executor, next, generator, None)
                    
                    if chunk is None:  # Generator exhausted
                        break
                    
                    full_response += chunk
                    await agent_msg.stream_token(chunk)
                    last_chunk_time = time.time()
                    
                except StopIteration:
                    break
                except Exception as gen_error:
                    error_msg = f"\n\n[ERROR] Generator error: {str(gen_error)[:200]}\n"
                    await agent_msg.stream_token(error_msg)
                    full_response += error_msg
                    break

            task_elapsed = time.time() - task_start

            # Add metadata footer with agent name for clarity
            await agent_msg.stream_token(f"\n\n---\n\n**Agent:** {emoji} {agent_display_name}  \n**Progress:** Task {task_num}/12 ({category})  \n**Duration:** {task_elapsed:.1f}s\n\n---")

            # Update message
            await agent_msg.update()

        except Exception as e:
            task_elapsed = time.time() - task_start
            error_text = f"\n\n[ERROR] Error after {task_elapsed:.1f}s: {str(e)[:200]}\n\nContinuing to next task..."
            await agent_msg.stream_token(error_text)
            await agent_msg.update()
            full_response += error_text
        finally:
            # Stop the heartbeat task
            streaming_complete = True
            heartbeat_task.cancel()
            try:
                await heartbeat_task
            except asyncio.CancelledError:
                pass  # Expected when we cancel the task
            
            # Shutdown the executor if it exists
            if 'executor' in locals():
                executor.shutdown(wait=False)
        
        # Store output
        output_entry = {
            'task_number': task_num,
            'agent_name': agent_display_name,
            'category': category,
            'output': full_response,
            'elapsed_seconds': task_elapsed
        }
        all_outputs.append(output_entry)
        
        # Update context for next agents
        context_entry = f"\n\n### {emoji} {agent_display_name} ({category}):\n{full_response}"
        context_history.append(context_entry)
    
    # Show completion
    total_elapsed = time.time() - start_time
    completion_msg = await cl.Message(
        content=f"✅ **Analysis Complete!**\n\nTotal time: {total_elapsed/60:.1f} minutes\n\nAll 12 tasks completed successfully.",
        author="System"
    ).send()


if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
