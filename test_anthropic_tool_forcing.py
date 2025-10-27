"""
Test if Anthropic API actually respects tool_choice parameter.
"""
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load environment
load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Define simple tools
tools = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                }
            },
            "required": ["location"]
        }
    }
]

print("="*80)
print("🧪 TESTING ANTHROPIC TOOL_CHOICE FORCING")
print("="*80)

# Test 1: With tool_choice="auto" (should allow text)
print("\n📝 TEST 1: tool_choice='auto' (Claude decides)")
print("-"*80)

response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=500,
    tools=tools,
    tool_choice={"type": "auto"},
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

print(f"Stop reason: {response.stop_reason}")
print(f"Content blocks: {len(response.content)}")
for i, block in enumerate(response.content):
    print(f"  Block {i}: {block.type}")
    if block.type == "tool_use":
        print(f"    Tool: {block.name}")

# Test 2: With tool_choice="any" (MUST use tool)
print("\n" + "="*80)
print("📝 TEST 2: tool_choice='any' (FORCED to use tool)")
print("-"*80)

response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=500,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[{"role": "user", "content": "What's the weather in Paris?"}]
)

print(f"Stop reason: {response.stop_reason}")
print(f"Content blocks: {len(response.content)}")
for i, block in enumerate(response.content):
    print(f"  Block {i}: {block.type}")
    if block.type == "tool_use":
        print(f"    ✅ Tool: {block.name}")
        print(f"    ✅ Input: {block.input}")

# Test 3: With our actual prompt style
print("\n" + "="*80)
print("📝 TEST 3: With 'MUST use tools' instruction + tool_choice='any'")
print("-"*80)

response = client.messages.create(
    model="claude-opus-4-20250514",
    max_tokens=500,
    tools=tools,
    tool_choice={"type": "any"},
    messages=[{
        "role": "user",
        "content": """🚨 MANDATORY VERIFICATION REQUIREMENT 🚨

You MUST start by using verification tools to gather evidence.

**TOPIC:** What's the weather like in Paris today?

**YOUR TASK:** Provide a weather report.

DO NOT write analysis from memory - use tools first!"""
    }]
)

print(f"Stop reason: {response.stop_reason}")
print(f"Content blocks: {len(response.content)}")
for i, block in enumerate(response.content):
    print(f"  Block {i}: {block.type}")
    if block.type == "tool_use":
        print(f"    ✅ Tool: {block.name}")

print("\n" + "="*80)
print("✅ ANTHROPIC API TEST COMPLETE")
print("="*80)
