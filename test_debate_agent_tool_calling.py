"""
Test a single debate agent with tool calling
"""

import os
import sys
from dotenv import load_dotenv

# Fix encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

from src.academic_debate_council.direct_chat_agents import DebateAgentsManager

print("=" * 80)
print("🧪 TESTING DEBATE AGENT TOOL CALLING")
print("=" * 80)
print()

# Create manager
manager = DebateAgentsManager()

# Get spiritual agent (Task 1)
agent = manager.get_agent_for_task(1)
agent_name = manager.get_agent_display_name('sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert')

print(f"Agent: {agent_name}")
print(f"Model: {agent.model}")
print(f"Role: {agent.role}")
print()

# Get tools for this agent
tools = agent._get_anthropic_tools()
print(f"Tools available: {len(tools)}")
for tool in tools:
    print(f"  - {tool['name']}")
print()

# Test with a topic that REQUIRES tool usage
topic = "Should prayer breaks be mandatory in Qatar workplaces?"
task_desc = manager.get_task_description('analyze_spiritual_foundation')

print("Topic:", topic)
print("Task:", task_desc[:100] + "...")
print()
print("-" * 80)
print("Executing agent with DEBUG logging...")
print("-" * 80)
print()

# Stream the response
for chunk in agent.execute_task_streaming(
    topic=topic,
    task_description=task_desc,
    context=[],
    temperature=0.3
):
    print(chunk, end='', flush=True)

print()
print()
print("=" * 80)
print("✅ Test complete! Check debug output above for tool usage details.")
print("=" * 80)
