"""
Test agent execution with explicit logging to diagnose tool calling issue.
"""
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment first
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pathlib import Path
from academic_debate_council.direct_chat_agents import DebateAgentsManager

print("="*80)
print("🧪 TESTING AGENT WITH FULL LOGGING")
print("="*80)

# Create manager
manager = DebateAgentsManager()

# Get spiritual agent (Task 1)
print("\n📋 Getting spiritual agent...")
agent = manager.get_agent_for_task(1)
task_info = manager.get_task_info(1)

print(f"Agent: {agent.name}")
print(f"Role: {agent.role}")
print(f"Model: {agent.model}")

# Get tools for this agent
tools = agent._get_anthropic_tools()
print(f"\n🔧 Tools available: {len(tools) if tools else 0}")
if tools:
    for tool in tools:
        print(f"   - {tool['name']}")

# Get task description
task_desc = manager.get_task_description(task_info['task_name'])

# Execute with streaming
print("\n" + "="*80)
print("🚀 EXECUTING AGENT (watch for debug output)...")
print("="*80 + "\n")

topic = "Should workplaces allow prayer breaks?"

try:
    for chunk in agent.execute_task_streaming(
        topic=topic,
        task_description=task_desc,
        context=[],
        temperature=0.3
    ):
        # Only print tool execution markers, not all text
        if "🔧" in chunk or "📊" in chunk or "Executing tool" in chunk:
            print(chunk, end="", flush=True)
        elif "AGENT:" in chunk or "TOOLS AVAILABLE:" in chunk or "RESPONSE BLOCKS:" in chunk:
            print(chunk)
            
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("✅ TEST COMPLETE")
print("="*80)
