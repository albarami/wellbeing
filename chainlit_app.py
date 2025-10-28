"""
Academic Debate Council - Chainlit Interface
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

# Load environment variables
# Only load .env file when running locally (not in production)
if os.getenv('RAILWAY_ENVIRONMENT') is None:
    # Running locally - load from .env file
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
# In production (Railway), environment variables are already available via os.getenv()

# Import our debate engine
from src.academic_debate_council.direct_chat_agents import DebateAgentsManager

# Import verification tools
try:
    from src.academic_debate_council.tools import (
        verify_citation_standalone,
        verify_medical_claim_standalone,
        search_hadith_standalone,
        get_quran_verse_standalone,
        search_shamela_standalone,
        search_madhab_fatwa_standalone,
        brave_search_standalone,
        get_qatar_stats_standalone,
        perplexity_fact_check_standalone
    )
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    print("⚠️ Verification tools not available")


async def execute_tool_call(tool_line: str) -> str:
    """
    Parse and execute a tool call from the agent's output.
    
    Example input: TOOL: search_shamela_standalone("workplace prayer")
    """
    try:
        # Auto-fix broken tool calls
        tool_line = tool_line.strip()
        
        # Fix missing "TOOL:" prefix
        if not tool_line.startswith('TOOL:'):
            tool_line = 'TOOL: ' + tool_line
        
        # Fix truncated function names (common patterns)
        tool_line = tool_line.replace('_quran_verse_standalone', 'get_quran_verse_standalone')
        tool_line = tool_line.replace('ab_fatwa_standalone', 'search_madhab_fatwa_standalone')
        tool_line = tool_line.replace('_madhab_fatwa_standalone', 'search_madhab_fatwa_standalone')
        tool_line = tool_line.replace('_shamela_standalone', 'search_shamela_standalone')
        tool_line = tool_line.replace('_medical_claim_standalone', 'verify_medical_claim_standalone')
        tool_line = tool_line.replace('_citation_standalone', 'verify_citation_standalone')
        tool_line = tool_line.replace('_stats_standalone', 'get_qatar_stats_standalone')
        tool_line = tool_line.replace('_qatar_stats_standalone', 'get_qatar_stats_standalone')
        tool_line = tool_line.replace('plexity_fact_check_standalone', 'perplexity_fact_check_standalone')
        
        # Fix common abbreviations
        tool_line = tool_line.replace('"sh"', '"shafii"')
        tool_line = tool_line.replace('"han"', '"hanafi"')
        tool_line = tool_line.replace('"mal"', '"maliki"')
        tool_line = tool_line.replace('"hamb"', '"hanbali"')
        
        # Remove "TOOL:" prefix for processing
        tool_call = tool_line.replace('TOOL:', '').strip()
        
        # Parse function name and arguments
        if '(' not in tool_call:
            return "❌ Invalid tool call format"
        
        func_name = tool_call[:tool_call.index('(')].strip()
        args_str = tool_call[tool_call.index('(')+1:tool_call.rindex(')')].strip()
        
        # Parse arguments (simple parsing for quoted strings and numbers)
        args = []
        if args_str:
            # Split by comma, but respect quotes
            import re
            matches = re.findall(r'"([^"]*)"|(\d+)', args_str)
            # Flatten and filter empty matches
            for string_match, num_match in matches:
                if string_match:
                    args.append(string_match)
                elif num_match:
                    args.append(int(num_match))
        
        # Execute the tool
        if func_name == 'search_shamela_standalone':
            result = search_shamela_standalone(args[0] if args else "")
        elif func_name == 'search_madhab_fatwa_standalone':
            result = search_madhab_fatwa_standalone(args[0] if len(args) > 0 else "", 
                                                     args[1] if len(args) > 1 else "all")
        elif func_name == 'get_quran_verse_standalone':
            result = get_quran_verse_standalone(args[0] if len(args) > 0 else 1, 
                                                args[1] if len(args) > 1 else 1)
        elif func_name == 'search_hadith_standalone':
            result = search_hadith_standalone(args[0] if args else "")
        elif func_name == 'verify_citation_standalone':
            result = verify_citation_standalone(args[0] if len(args) > 0 else "", 
                                               args[1] if len(args) > 1 else "",
                                               args[2] if len(args) > 2 else "")
        elif func_name == 'verify_medical_claim_standalone':
            result = verify_medical_claim_standalone(args[0] if args else "")
        elif func_name == 'get_qatar_stats_standalone':
            result = get_qatar_stats_standalone(args[0] if args else "")
        elif func_name == 'perplexity_fact_check_standalone':
            result = perplexity_fact_check_standalone(args[0] if args else "")
        elif func_name == 'brave_search_standalone':
            result = brave_search_standalone(args[0] if args else "")
        else:
            return f"❌ Unknown tool: {func_name}"
        
        # Return the data from the result
        if isinstance(result, dict) and 'data' in result:
            return result['data'][:1000]  # Limit to 1000 chars
        else:
            return str(result)[:1000]
        
    except Exception as e:
        return f"❌ Tool execution error: {str(e)}"


@cl.on_chat_start
async def start():
    """Initialize the chat session."""
    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        await cl.Message(
            content="⚠️ **API Key Missing**\n\nPlease set your ANTHROPIC_API_KEY in the environment variables.",
            author="System"
        ).send()
        return
    
    # Welcome message
    await cl.Message(
        content="""# 🎓 Welcome to Academic Debate Council

**Multi-Agent AI System for Comprehensive Multi-Perspective Analysis**

I coordinate **7 AI expert agents** who will analyze ANY topic through **12 sequential tasks**, providing spiritual, emotional, intellectual, physical, and social perspectives.

## 🎯 The Experts:
- 🕌 **Sheikh Dr. Ibrahim al-Tazkiyah** - Spiritual Pillar Expert
- ❤️ **Dr. Layla al-Qalb** - Emotional Pillar Expert  
- 🧠 **Dr. Hassan al-Hikmah** - Intellectual Pillar Expert
- 💪 **Dr. Fatima al-Jism** - Physical Pillar Expert
- 🤝 **Dr. Aisha al-Mujtama'** - Social Pillar Expert
- ⚖️ **Dr. Yusuf al-Mudeer** - Debate Orchestrator
- 📊 **Dr. Amira al-Tawhid** - Synthesizer

## 💬 How It Works:
1. Ask ANY question about wellbeing, policy, lifestyle, or social issues
2. Watch 7 AI agents debate through 12 sequential tasks in real-time
3. Each agent appears as they complete (~60 seconds each)
4. Get a comprehensive multi-perspective analysis

## 📝 Example Topics:
- "Should prayer breaks be enforced in Qatar workplaces?"
- "Impact of mandatory Arabic education on expat children"
- "Remote work policies in Gulf corporations"
- "Traditional vs modern parenting approaches"
- "Social media influence on Qatari youth"

## 👨‍💻 Developer:
**Salim AL-Barami**

**Ready? Ask your question below!** 👇
""",
        author="System"
    ).send()
    
    # Store user session data
    cl.user_session.set("debate_history", [])
    cl.user_session.set("manager", DebateAgentsManager())


@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages and run the debate."""
    
    topic = message.content.strip()
    
    if not topic:
        await cl.Message(
            content="Please enter a topic to analyze.",
            author="System"
        ).send()
        return
    
    # Get the debate manager
    manager = cl.user_session.get("manager")
    
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
        
        # Add to context for next agents
        context_entry = f"**{agent_display_name}** ({category}, Task {task_num}):\n{full_response[:2000]}"
        context_history.append(context_entry)
    
    # Calculate total time
    total_elapsed = time.time() - start_time
    
    # Send completion message
    completion_msg = await cl.Message(
        content=f"""---

# ✅ Analysis Complete!

**Topic:** {topic}

**Duration:** {total_elapsed/60:.1f} minutes  
**Agents:** 12 tasks across 7 expert perspectives  
**Total Words:** ~{sum(len(o['output'].split()) for o in all_outputs):,}

🎉 All experts have completed their analysis. You can now:
- Review each expert's perspective above
- Ask a follow-up question
- Analyze a different topic

---

*Developed by **Salim AL-Barami***

Would you like to analyze another topic?
""",
        author="System"
    ).send()
    
    # Store in session
    debate_history = cl.user_session.get("debate_history")
    debate_history.append({
        'topic': topic,
        'outputs': all_outputs,
        'total_elapsed': total_elapsed,
        'timestamp': datetime.now().isoformat()
    })
    cl.user_session.set("debate_history", debate_history)


@cl.on_settings_update
async def setup_agent(settings):
    """Handle settings updates."""
    pass


if __name__ == "__main__":
    # For local testing
    pass
