# WebSocket Timeout Fix - Complete Solution

## Problem
The application was showing "Could not reach the server" error and freezing at Task 2/12 when agents tried to use verification tools (like `get_quran_verse_standalone`).

## Root Cause
When the agent executed API calls (Quran API, Hadith API, etc.), there were periods of 10-30 seconds where **no data was sent to the Chainlit frontend**. This caused the WebSocket connection to timeout and disconnect, showing "Could not reach the server".

## Solutions Implemented

### 1. Background Heartbeat Task ⭐ **KEY FIX**
**File:** `chainlit_app.py` (lines 274-292, 332-339)

```python
# Background task that sends keep-alive signals every 5 seconds
async def send_heartbeat():
    heartbeat_count = 0
    while not streaming_complete:
        await asyncio.sleep(5)
        if not streaming_complete:
            heartbeat_count += 1
            if heartbeat_count % 3 == 0:
                await agent_msg.stream_token(".")  # Visible progress
            else:
                await agent_msg.stream_token("")  # Invisible keep-alive
```

**Impact:** Ensures WebSocket **always** receives data every 5 seconds, even during long API calls.

### 2. API Retry Logic with Progressive Timeouts
**File:** `src/academic_debate_council/tools/islamic_texts.py` (lines 338-430)

```python
# Retry with increasing timeouts
max_retries = 2
timeouts = [5, 10]  # First try 5s, then 10s

for attempt in range(max_retries):
    try:
        response = requests.get(url, timeout=timeouts[attempt])
        # ... handle response
    except (Timeout, ConnectionError):
        if attempt < max_retries - 1:
            continue  # Try again
```

**Impact:** Handles temporary network issues and gives slow APIs more time on second attempt.

### 3. Stream Speed Reduction
**File:** `src/academic_debate_council/direct_chat_agents.py` (lines 732, 764, 777)

```python
# Delay between text chunks
time.sleep(0.01)  # 10ms

# Delay before tool execution
time.sleep(0.5)   # 500ms

# Delay after tool result
time.sleep(0.3)   # 300ms
```

**Impact:** Prevents API rate limiting and gives external services time to respond.

### 4. Enhanced Error Handling
**File:** `src/academic_debate_council/direct_chat_agents.py` (lines 766-771)

```python
try:
    tool_result = self._execute_tool(tool_name, tool_input)
except Exception as tool_error:
    tool_result = f"⚠️ Tool execution error: {str(tool_error)[:200]}"
```

**Impact:** Tool failures no longer crash the entire debate - agents continue with partial information.

### 5. Task-Level Timeout Protection
**File:** `chainlit_app.py` (lines 305-310)

```python
task_timeout = 240  # 4 minutes max per agent
if time.time() - task_start > task_timeout:
    timeout_msg = "Task timeout - Moving to next agent..."
    break
```

**Impact:** Even if an agent gets stuck, the system automatically continues to the next task.

### 6. WebSocket Configuration
**File:** `.chainlit/config.toml` (lines 17-22)

```toml
session_timeout = 7200
websocket_ping_interval = 10
websocket_ping_timeout = 60
```

**Impact:** Increased session timeout and configured WebSocket ping intervals.

## How to Test

### Option 1: Use the Startup Script
```bash
START_CHAINLIT.bat
```

### Option 2: Manual Start
```bash
cd "D:\Academic debate"
chainlit run chainlit_app.py
```

### Option 3: Test API Directly
```bash
python test_timeout_fix.py
```

## Expected Behavior After Fix

### Before (Broken)
1. Agent starts Task 2/12
2. Calls `get_quran_verse_standalone(2, 256)`
3. API takes 10-15 seconds
4. **WebSocket times out** → "Could not reach the server"
5. Application freezes permanently

### After (Fixed)
1. Agent starts Task 2/12
2. Calls `get_quran_verse_standalone(2, 256)`
3. **Background heartbeat sends "." every 5 seconds** → WebSocket stays alive
4. API responds (or times out gracefully after 2 retries)
5. Agent continues with result (or error message)
6. **All 12 tasks complete successfully**

## Monitoring Progress

You'll now see:
- `🔧 Executing tool: get_quran_verse_standalone` - Tool is being called
- `.` dots appearing every 15 seconds - Heartbeat keeping connection alive
- `📊 Tool result:` - Tool completed (success or error)
- Agent continues writing response

## Troubleshooting

### If you still see "Could not reach the server":

1. **Check your internet connection**
   - The Quran API (api.quran.com) must be reachable
   - Test: Open https://api.quran.com/api/v4/verses/by_key/2:256 in browser

2. **Check firewall/antivirus**
   - May be blocking WebSocket connections on localhost:8000
   - Add exception for `chainlit.exe` and `python.exe`

3. **Restart the Chainlit server**
   - Close the terminal running Chainlit
   - Run `START_CHAINLIT.bat` again
   - Refresh browser (Ctrl+F5 for hard refresh)

4. **Check port 8000 availability**
   ```bash
   netstat -ano | findstr :8000
   ```
   If port is in use, kill the process or use different port:
   ```bash
   chainlit run chainlit_app.py --port 8001
   ```

5. **Increase heartbeat frequency** (if still timing out)
   Edit `chainlit_app.py` line 282:
   ```python
   await asyncio.sleep(3)  # Changed from 5 to 3 seconds
   ```

## Performance Impact

- **Heartbeat overhead:** Negligible (~10 bytes per 5 seconds)
- **Stream delays:** Adds ~1-2 seconds total per agent
- **API retries:** May add 5-10 seconds on first failure
- **Overall impact:** +10-15 seconds per complete 12-task debate (acceptable trade-off for stability)

## Success Criteria

✅ Application completes all 12 tasks without freezing
✅ "Could not reach the server" error never appears
✅ Tool execution errors are shown but don't crash the system
✅ WebSocket connection stays alive for entire 10-15 minute debate
✅ Progress indicators (dots) visible during long operations

## Developer Notes

The critical insight here is that **Chainlit's WebSocket requires periodic activity** to stay alive.

In a normal chatbot, the LLM generates tokens continuously, naturally keeping the WebSocket alive. But in our multi-agent system with tool calling:

1. Agent sends tool request to Anthropic API
2. **Anthropic API waits** for our tool to execute
3. Our tool makes HTTP request to external API (Quran, Hadith, etc.)
4. **External API takes 5-15 seconds** to respond
5. During this time, **nothing is sent to Chainlit frontend**
6. WebSocket assumes connection is dead → timeout

The `send_heartbeat()` background task solves this by **decoupling** heartbeat generation from the main streaming flow. It runs independently and ensures data flows to the frontend every 5 seconds, regardless of what the agent is doing.

## Additional Resources

- Chainlit WebSocket docs: https://docs.chainlit.io/
- Anthropic streaming API: https://docs.anthropic.com/claude/reference/messages-streaming
- Python asyncio: https://docs.python.org/3/library/asyncio.html

---

**Last Updated:** 2025-10-27
**Status:** ✅ Implemented and tested
**Author:** Claude Code Assistant
