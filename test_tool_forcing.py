"""
Test tool_choice forcing with Anthropic API
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Define a simple test tool
tools = [
    {
        "name": "search_hadith",
        "description": "Search for hadith by topic",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
]

print("=" * 80)
print("🧪 TESTING TOOL_CHOICE FORCING")
print("=" * 80)
print()

# Test 1: Without tool_choice (should be able to answer without tools)
print("TEST 1: Without tool_choice (auto)")
print("-" * 80)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    tools=tools,
    tool_choice={"type": "auto"},
    messages=[
        {
            "role": "user",
            "content": "What does Islam say about prayer timing?"
        }
    ]
)

print(f"Stop reason: {response.stop_reason}")
print(f"Content blocks: {len(response.content)}")
for i, block in enumerate(response.content):
    print(f"  Block {i}: {block.type}")
    if block.type == "tool_use":
        print(f"    Tool: {block.name}")

print()
print("=" * 80)
print()

# Test 2: WITH tool_choice="any" (MUST use tool)
print("TEST 2: WITH tool_choice='any' (FORCED)")
print("-" * 80)

response2 = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    tools=tools,
    tool_choice={"type": "any"},  # FORCE tool usage
    messages=[
        {
            "role": "user",
            "content": "What does Islam say about prayer timing?"
        }
    ]
)

print(f"Stop reason: {response2.stop_reason}")
print(f"Content blocks: {len(response2.content)}")
for i, block in enumerate(response2.content):
    print(f"  Block {i}: {block.type}")
    if block.type == "tool_use":
        print(f"    ✅ Tool: {block.name}")
        print(f"    ✅ Input: {block.input}")

print()
print("=" * 80)
print()

if response2.stop_reason == "tool_use":
    print("✅ SUCCESS! tool_choice='any' forced Claude to use the tool")
else:
    print("❌ FAILURE! tool_choice='any' did NOT force tool usage")
    print(f"   Stop reason: {response2.stop_reason}")

print()
print("=" * 80)
