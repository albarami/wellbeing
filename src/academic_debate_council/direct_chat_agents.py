"""
Direct Claude API Integration for Real-Time Group Chat Debate
Loads agent configurations and executes them with streaming support.

Enhanced with verification tools for citation checking and fact verification.
ALL AGENTS GET ACCESS TO ALL TOOLS FOR COMPREHENSIVE FACT-CHECKING.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Iterator
from anthropic import Anthropic
import streamlit as st
import threading
import time

# Import verification tools
try:
    from academic_debate_council.tools import (
        # Citation verification
        verify_citation_standalone,
        verify_medical_claim_standalone,
        # Islamic texts
        search_hadith_standalone,
        get_quran_verse_standalone,
        search_shamela_standalone,
        search_madhab_fatwa_standalone,
        # Fact-checking
        brave_search_standalone,
        get_qatar_stats_standalone,
        perplexity_fact_check_standalone
    )
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    print("⚠️ Verification tools not available. Install with: pip install -e .")


class AgentExecutor:
    """
    Executes an agent task by calling Claude API directly with streaming support.
    """
    
    def __init__(self, name: str, config: Dict, model_override: Optional[str] = None):
        """
        Initialize agent executor.
        
        Args:
            name: Agent identifier (e.g., 'sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert')
            config: Agent configuration from agents.yaml
            model_override: Optional model to override the config
        """
        self.name = name
        self.config = config
        self.role = config.get('role', 'Expert')
        self.goal = config.get('goal', '')
        self.backstory = config.get('backstory', '')
        
        # Get model from config or use override
        self.model = model_override or self._extract_model_from_config()
        
        # Initialize Anthropic client
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
    
    def _extract_model_from_config(self) -> str:
        """Extract model name from config or use default."""
        # Default models based on agent type
        defaults = {
            'sheikh': 'claude-opus-4-20250514',
            'synthesizer': 'claude-opus-4-20250514',
            'tawhid': 'claude-opus-4-20250514'
        }
        
        name_lower = self.name.lower()
        for key, model in defaults.items():
            if key in name_lower:
                return model
        
        return 'claude-sonnet-4-20250514'  # Default for most agents
    
    def build_system_prompt(self) -> str:
        """Build the system prompt from agent configuration with tool instructions."""
        system_parts = []
        
        # Add role
        if self.role:
            system_parts.append(f"**YOUR ROLE:** {self.role}")
        
        # Add goal
        if self.goal:
            system_parts.append(f"\n**YOUR GOAL:**\n{self.goal}")
        
        # Add backstory
        if self.backstory:
            system_parts.append(f"\n**YOUR BACKGROUND:**\n{self.backstory}")
        
        # Add tool instructions - ALL AGENTS GET ALL TOOLS
        if TOOLS_AVAILABLE:
            tool_instructions = self._get_tool_instructions()
            if tool_instructions:
                system_parts.append(f"\n\n**VERIFICATION TOOLS AVAILABLE:**\n{tool_instructions}")
        
        return "\n".join(system_parts)
    
    def _get_tool_instructions(self) -> str:
        """Get tool instructions - ALL AGENTS GET ALL TOOLS."""
        name_lower = self.name.lower()
        
        # ALL AGENTS GET COMPLETE TOOL ACCESS
        base_tools = """
**🚨 MANDATORY TOOL USAGE POLICY 🚨**

⛔ STOP! READ THIS BEFORE PROCEEDING:

YOU ARE REQUIRED TO USE VERIFICATION TOOLS. DO NOT PROCEED WITHOUT THEM.

🔴 WORKFLOW YOU MUST FOLLOW:
1. FIRST: Call 2-3 verification tools to gather evidence
2. THEN: Write your analysis based on tool results
3. NEVER cite from memory or training data

❌ WRONG: Write response → Maybe use tools
✅ CORRECT: Use tools FIRST → Write response based on tool results

Before making ANY claim about:
- Quranic verses → MUST use get_quran_verse_standalone()
- Hadith → MUST use search_hadith_standalone()
- Research studies → MUST use verify_citation_standalone() or verify_medical_claim_standalone()
- Qatar statistics → MUST use get_qatar_stats_standalone()
- Any factual claim → MUST use perplexity_fact_check_standalone()

❌ DO NOT cite from memory - your training data may be outdated or wrong
✅ USE TOOLS to get current, verified information

🔧 COMPLETE VERIFICATION TOOLKIT:

📚 ISLAMIC SOURCES:
- get_quran_verse_standalone(surah, ayah) - Verify Quranic verses
- search_hadith_standalone(query) - Search authenticated hadith (Sahih Bukhari/Muslim)
- search_madhab_fatwa_standalone(topic, madhab) - Madhab-specific fatwas
- search_shamela_standalone(query) - Classical Islamic texts

📊 ACADEMIC VERIFICATION:
- verify_citation_standalone(author, year, keywords) - Verify any academic paper
- verify_medical_claim_standalone(keywords) - Search medical/psychological research (PubMed)

🌍 CURRENT DATA & STATISTICS:
- get_qatar_stats_standalone(topic) - Qatar statistics (World Bank, Trading Economics)
- perplexity_fact_check_standalone(claim) - AI web search with citations (USE FOR EVERYTHING!)

🔧 HOW TO USE TOOLS - COPY THIS EXACT FORMAT:

**STOP AND READ THIS CAREFULLY!**
You MUST write tool calls EXACTLY as shown below. Copy the format character-by-character.

**CORRECT FORMAT (copy this):**
```
TOOL: get_quran_verse_standalone(4, 103)
```

**WRONG FORMATS (never do this):**
❌ `_standalone(4, 103)` - Missing function name prefix
❌ `get_quran_verse(4, 103)` - Missing _standalone suffix  
❌ `quran_verse_standalone(4, 103)` - Missing "TOOL:" prefix
❌ `_quran_verse_standalone(4, 103)` - Wrong prefix

**CORRECT EXAMPLES TO COPY:**
```
TOOL: get_quran_verse_standalone(4, 103)
TOOL: search_hadith_standalone("prayer obligation")
TOOL: verify_citation_standalone("Beck", "1979", "cognitive therapy")
TOOL: verify_medical_claim_standalone("workplace stress")
TOOL: get_qatar_stats_standalone("labor force demographics")
TOOL: perplexity_fact_check_standalone("Qatar prayer policy 2024")
TOOL: search_madhab_fatwa_standalone("workplace prayer", "hanafi")
TOOL: search_shamela_standalone("Ibn Taymiyyah prayer")
```

⚠️ MANDATORY RULES:
1. Line MUST start with: `TOOL: `
2. Function name MUST end with: `_standalone`
3. Use double quotes "" for text, plain numbers for integers
4. ONE tool per line
5. Write NOTHING else on the tool line

⚠️ WHEN TO USE TOOLS:
- BEFORE citing Quran → TOOL: get_quran_verse_standalone(surah, ayah)
- BEFORE citing hadith → TOOL: search_hadith_standalone("query")
- BEFORE citing studies → TOOL: verify_citation_standalone("author", "year", "keywords")
- BEFORE stating statistics → TOOL: get_qatar_stats_standalone("topic")
- For current data → TOOL: perplexity_fact_check_standalone("claim")

✅ AFTER TOOL RESULTS:
- CITE THE SOURCES provided by tools
- If no results: Acknowledge limitation, don't fabricate

📝 **CRITICAL: READABLE FORMATTING REQUIRED!**

You MUST write short paragraphs with clear structure. NO walls of text!

**MANDATORY RULES:**
1. Put TWO blank lines before each ## header
2. Put ONE blank line after each ## header  
3. Maximum 2-3 sentences per paragraph
4. Put ONE blank line between paragraphs
5. Use bullet points with - for lists
6. Keep each bullet to ONE line

**CORRECT FORMAT (copy this exactly):**

[Previous content here]


## I. Islamic Foundation

The Quran establishes prayer as time-bound obligation. This verse frames prayer as divinely mandated appointments with Allah.

**Key References:**
- Quran 4:103 - Prayer decreed at specified times
- Prophetic teaching - First accountability on Judgment Day

Al-Ghazali emphasizes that earning halal livelihood enables religious duties. The workplace transforms into a space where deen and dunya harmonize.


## II. Maqasid Analysis

This policy serves three objectives:

**Hifz al-Din** - Facilitates second pillar of Islam by removing barriers to prayer.

**Hifz al-Nafs** - Regular spiritual breaks reduce workplace stress and anxiety.

**Hifz al-Aql** - Brief pauses enhance mental clarity and focus throughout the workday.


## III. Wellbeing Scores

**Connection to Allah: +3**
Timely prayer directly strengthens relationship with Allah.

**Purposeful Living: +3**
Workplace becomes space where spiritual and professional duties align.

**Inner Purification: +2**
Provides reset points, though rushed prayers may limit depth.

---

**WRONG FORMAT (NEVER do this):**
❌ "## I. Islamic Foundation The Quran establishes prayer as a time-bound obligation: Quran 4:103 indeed prayer has been decreed upon believers at specified times and the Prophet emphasized this and Al-Ghazali in his work emphasizes that earning halal livelihood becomes worship when it enables religious duties and the workplace thus transforms into a space where deen and dunya harmonize..."

**CRITICAL:** If you write a paragraph longer than 4 lines, STOP and break it into multiple short paragraphs!
"""
        
        # Add agent-specific priority guidance
        agent_priority = ""
        
        if 'sheikh' in name_lower or 'spiritual' in name_lower:
            agent_priority = """

🎯 YOUR PRIORITY TOOLS (Use these first):
1. get_quran_verse_standalone - For any Quranic reference
2. search_hadith_standalone - For hadith citations
3. search_madhab_fatwa_standalone - For madhab positions
4. perplexity_fact_check_standalone - For current Islamic rulings
"""
        elif 'physical' in name_lower or 'jism' in name_lower:
            agent_priority = """

🎯 YOUR PRIORITY TOOLS (Use these first):
1. verify_medical_claim_standalone - For medical/health research
2. verify_citation_standalone - For academic papers
3. get_qatar_stats_standalone - For Qatar health statistics
4. perplexity_fact_check_standalone - For current health data
"""
        elif 'social' in name_lower or 'mujtama' in name_lower:
            agent_priority = """

🎯 YOUR PRIORITY TOOLS (Use these first):
1. get_qatar_stats_standalone - For Qatar demographics/statistics
2. perplexity_fact_check_standalone - For current social data
3. verify_citation_standalone - For social science research
"""
        elif 'emotional' in name_lower or 'qalb' in name_lower:
            agent_priority = """

🎯 YOUR PRIORITY TOOLS (Use these first):
1. verify_medical_claim_standalone - For psychological research
2. verify_citation_standalone - For psychology papers
3. perplexity_fact_check_standalone - For current wellbeing research
"""
        elif 'intellectual' in name_lower or 'hikmah' in name_lower:
            agent_priority = """

🎯 YOUR PRIORITY TOOLS (Use these first):
1. verify_citation_standalone - For academic/philosophical papers
2. perplexity_fact_check_standalone - For current academic discourse
"""
        
        return base_tools + agent_priority

    def _get_anthropic_tools(self) -> List[Dict]:
        """
        Get Anthropic-formatted tool definitions based on agent type.

        Returns:
            List of tool definitions for Anthropic API
        """
        name_lower = self.name.lower()

        # Spiritual Agent Tools
        if 'sheikh' in name_lower or 'spiritual' in name_lower:
            return [
                {
                    "name": "search_hadith_standalone",
                    "description": "Search authenticated hadith collections for specific topics",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "Keywords to search"},
                            "collections": {"type": "array", "items": {"type": "string"}},
                            "max_results": {"type": "integer", "description": "Max results (default: 3)"}
                        },
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_quran_verse_standalone",
                    "description": "Get and verify a Quranic verse with Arabic and translation",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "surah": {"type": "integer", "description": "Surah number (1-114)"},
                            "ayah": {"type": "integer", "description": "Ayah number"}
                        },
                        "required": ["surah", "ayah"]
                    }
                },
                {
                    "name": "search_madhab_fatwa_standalone",
                    "description": "Search madhab-specific Islamic legal rulings",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"},
                            "madhab": {"type": "string", "enum": ["hanafi", "maliki", "shafii", "hanbali", "all"]},
                            "max_results": {"type": "integer"}
                        },
                        "required": ["topic", "madhab"]
                    }
                }
            ]

        # Physical/Health Agent Tools
        elif 'physical' in name_lower or 'jism' in name_lower:
            return [
                {
                    "name": "verify_citation_standalone",
                    "description": "Verify academic paper citations",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string"},
                            "year": {"type": "string"},
                            "title_keywords": {"type": "string"}
                        },
                        "required": ["author", "year", "title_keywords"]
                    }
                },
                {
                    "name": "verify_medical_claim_standalone",
                    "description": "Verify medical/health claims via PubMed",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "keywords": {"type": "string"}
                        },
                        "required": ["keywords"]
                    }
                },
                {
                    "name": "get_qatar_stats_standalone",
                    "description": "Get Qatar statistics from official sources",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"}
                        },
                        "required": ["topic"]
                    }
                }
            ]

        # Social Agent Tools
        elif 'social' in name_lower or 'mujtama' in name_lower:
            return [
                {
                    "name": "get_qatar_stats_standalone",
                    "description": "Get Qatar statistics",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "topic": {"type": "string"}
                        },
                        "required": ["topic"]
                    }
                },
                {
                    "name": "verify_citation_standalone",
                    "description": "Verify social science citations",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string"},
                            "year": {"type": "string"},
                            "title_keywords": {"type": "string"}
                        },
                        "required": ["author", "year", "title_keywords"]
                    }
                },
                {
                    "name": "perplexity_fact_check_standalone",
                    "description": "Fact-check claims using AI web search",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "claim": {"type": "string"}
                        },
                        "required": ["claim"]
                    }
                }
            ]

        # Emotional Agent Tools
        elif 'emotional' in name_lower or 'qalb' in name_lower:
            return [
                {
                    "name": "verify_citation_standalone",
                    "description": "Verify psychology citations",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string"},
                            "year": {"type": "string"},
                            "title_keywords": {"type": "string"}
                        },
                        "required": ["author", "year", "title_keywords"]
                    }
                },
                {
                    "name": "verify_medical_claim_standalone",
                    "description": "Verify psychological claims",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "keywords": {"type": "string"}
                        },
                        "required": ["keywords"]
                    }
                }
            ]

        # Intellectual Agent Tools
        elif 'intellectual' in name_lower or 'hikmah' in name_lower:
            return [
                {
                    "name": "verify_citation_standalone",
                    "description": "Verify academic citations",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "author": {"type": "string"},
                            "year": {"type": "string"},
                            "title_keywords": {"type": "string"}
                        },
                        "required": ["author", "year", "title_keywords"]
                    }
                },
                {
                    "name": "perplexity_fact_check_standalone",
                    "description": "Fact-check academic claims using AI web search",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "claim": {"type": "string"}
                        },
                        "required": ["claim"]
                    }
                }
            ]

        return []  # No tools for orchestrator/synthesizer

    def _execute_tool(self, tool_name: str, tool_input: Dict) -> str:
        """Execute a tool and return the result."""
        if not TOOLS_AVAILABLE:
            return "⚠️ Tools not available"

        try:
            if tool_name == "search_hadith_standalone":
                result = search_hadith_standalone(
                    query=tool_input.get('query', ''),
                    collections=tool_input.get('collections'),
                    max_results=tool_input.get('max_results', 3)
                )
                return result.get('data', 'No results')

            elif tool_name == "get_quran_verse_standalone":
                result = get_quran_verse_standalone(
                    surah=tool_input.get('surah'),
                    ayah=tool_input.get('ayah')
                )
                return result.get('data', 'Verse not found')

            elif tool_name == "search_madhab_fatwa_standalone":
                result = search_madhab_fatwa_standalone(
                    topic=tool_input.get('topic', ''),
                    madhab=tool_input.get('madhab', 'all'),
                    max_results=tool_input.get('max_results', 3)
                )
                return result.get('data', 'No results')

            elif tool_name == "verify_citation_standalone":
                result = verify_citation_standalone(
                    author=tool_input.get('author', ''),
                    year=tool_input.get('year', ''),
                    title_keywords=tool_input.get('title_keywords', '')
                )
                return result.get('data', 'Not verified')

            elif tool_name == "perplexity_fact_check_standalone":
                result = perplexity_fact_check_standalone(
                    claim=tool_input.get('claim', '')
                )
                return result.get('data', 'No results')

            elif tool_name == "verify_medical_claim_standalone":
                result = verify_medical_claim_standalone(
                    keywords=tool_input.get('keywords', ''),
                    max_results=tool_input.get('max_results', 3)
                )
                return result.get('data', 'No results')

            elif tool_name == "get_qatar_stats_standalone":
                result = get_qatar_stats_standalone(
                    topic=tool_input.get('topic', '')
                )
                return result.get('data', 'No statistics')

            else:
                return f"⚠️ Unknown tool: {tool_name}"

        except Exception as e:
            return f"⚠️ Error: {str(e)}"

    def build_user_message(self, topic: str, task_description: str, context: List[str] = None) -> str:
        """
        Build the user message with topic, task, and context.
        
        Args:
            topic: The wellbeing topic to analyze
            task_description: Description of the specific task
            context: List of previous agent responses
        
        Returns:
            Formatted user message string
        """
        message_parts = []

        # ADD TOOL USAGE INSTRUCTION AT THE VERY TOP
        # NOTE: When tool_choice="any" is set, Claude CANNOT emit text before tool use
        # So we instruct to use tools without asking for introductory text
        message_parts.append("""🚨 MANDATORY VERIFICATION REQUIREMENT 🚨

You MUST start by using 2-3 verification tools to gather evidence:
- search_hadith_standalone() for any hadith
- get_quran_verse_standalone() for Quran verses
- verify_medical_claim_standalone() for health research
- search_madhab_fatwa_standalone() for madhab positions
- get_qatar_stats_standalone() for Qatar data
- verify_citation_standalone() for academic papers

After you receive tool results, THEN write your analysis using the verified data.

DO NOT write analysis from memory - use tools first!""")

        # Add topic
        message_parts.append(f"\n**TOPIC TO ANALYZE:**\n{topic}")

        # Add task description
        message_parts.append(f"\n**YOUR TASK:**\n{task_description}")

        # Add context if available
        if context and len(context) > 0:
            message_parts.append(f"\n**CONTEXT FROM OTHER AGENTS:**")
            for ctx in context[-3:]:  # Last 3 context items
                message_parts.append(ctx)

        return "\n\n".join(message_parts)
    
    def execute_task(self, topic: str, task_description: str, context: List[str] = None, temperature: float = 0.3) -> str:
        """Execute the agent's task and return complete response."""
        system_prompt = self.build_system_prompt()
        user_message = self.build_user_message(topic, task_description, context)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            # Extract text from response
            return response.content[0].text
            
        except Exception as e:
            error_msg = f"Error executing {self.role}: {str(e)}"
            return error_msg
    
    def execute_task_streaming(
        self,
        topic: str,
        task_description: str,
        context: List[str] = None,
        temperature: float = 0.3
    ) -> Iterator[str]:
        """
        Execute the agent's task with streaming response and tool execution.

        Args:
            topic: The wellbeing topic
            task_description: Task description
            context: Previous agent responses
            temperature: Model temperature

        Yields:
            Chunks of the response as they arrive, including tool execution results
        """
        system_prompt = self.build_system_prompt()
        user_message = self.build_user_message(topic, task_description, context)
        tools = self._get_anthropic_tools()

        # DEBUG: Print at method start
        print(f"\n{'#'*80}")
        print(f"# EXECUTE_TASK_STREAMING CALLED")
        print(f"# Agent: {self.name}")
        print(f"# Tools fetched: {len(tools) if tools else 0}")
        if tools:
            print(f"# Tool names: {[t['name'] for t in tools]}")
        print(f"{'#'*80}\n")

        try:
            # Initial message
            messages = [{"role": "user", "content": user_message}]

            # Tool calling loop (allow multiple tool uses)
            max_iterations = 3  # Prevent infinite tool loops and timeouts
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # Stream the response with tool support and timeout protection
                stream_timeout = 180  # 3 minutes max per agent
                stream_start = time.time()
                timeout_triggered = False
                
                # CRITICAL: Force tool usage with tool_choice parameter
                # This prevents Claude from answering from memory without verification
                # Only set tool_choice if we have tools
                if tools and len(tools) > 0:
                    # Force tool usage on first iteration
                    tool_choice_config = {"type": "any"} if iteration == 1 else {"type": "auto"}
                else:
                    tool_choice_config = None

                # ALWAYS LOG THIS SO WE CAN DEBUG
                if iteration == 1:
                    print(f"\n{'='*80}")
                    print(f"🔧 AGENT: {self.name}")
                    print(f"🔧 TOOLS AVAILABLE: {len(tools) if tools else 0}")
                    print(f"🔧 TOOL_CHOICE: {tool_choice_config}")
                    if tools:
                        print(f"🔧 TOOL LIST: {[t['name'] for t in tools]}")
                    print(f"{'='*80}\n")

                # Build API call parameters
                api_params = {
                    "model": self.model,
                    "max_tokens": 8000,
                    "temperature": temperature,
                    "system": system_prompt,
                    "messages": messages
                }

                # Only add tools and tool_choice if we have tools
                if tools and len(tools) > 0:
                    api_params["tools"] = tools
                    api_params["tool_choice"] = tool_choice_config

                with self.client.messages.stream(**api_params) as stream:
                    # Collect tool uses and content blocks
                    tool_uses = []
                    text_content = ""

                    # Stream text and collect tool uses with timeout
                    for event in stream:
                        # Check timeout
                        if time.time() - stream_start > stream_timeout:
                            timeout_triggered = True
                            yield "\n\n⚠️ Response timeout (3 min) - continuing to next phase...\n"
                            break
                        if event.type == "content_block_start":
                            if hasattr(event, 'content_block') and event.content_block.type == "tool_use":
                                # Tool use started
                                pass

                        elif event.type == "content_block_delta":
                            if event.delta.type == "text_delta":
                                # Stream text to user
                                # DO NOT use time.sleep() here - it blocks the async event loop!
                                yield event.delta.text
                                text_content += event.delta.text

                        elif event.type == "content_block_stop":
                            # Content block finished
                            pass

                    # Get final message to check for tool uses
                    final_message = stream.get_final_message()

                    # LOG RESPONSE
                    print(f"📥 RESPONSE BLOCKS: {len(final_message.content)}")
                    for i, block in enumerate(final_message.content):
                        if block.type == "tool_use":
                            print(f"   ✅ Block {i}: TOOL_USE - {block.name}")
                        else:
                            print(f"   📝 Block {i}: {block.type}")

                    # Check if there are tool uses and collect ALL tool results
                    has_tool_use = False
                    tool_results = []

                    for block in final_message.content:
                        if block.type == "tool_use":
                            has_tool_use = True
                            tool_name = block.name
                            tool_input = block.input
                            tool_use_id = block.id

                            # Show tool execution
                            yield f"\n\n🔧 Executing tool: **{tool_name}**\n"

                            # Execute the tool with exception handling
                            try:
                                tool_result = self._execute_tool(tool_name, tool_input)
                            except Exception as tool_error:
                                tool_result = f"⚠️ Tool execution error: {str(tool_error)[:200]}"
                                yield f"⚠️ Error executing {tool_name}: {str(tool_error)[:200]}\n"

                            # Show result
                            yield f"📊 Tool result:\n{tool_result}\n\n"

                            # Store tool result for this tool
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": tool_use_id,
                                "content": tool_result
                            })

                    # If there were tool uses, add assistant message and ALL tool results
                    if has_tool_use:
                        # Add assistant message with ALL tool_use blocks
                        messages.append({
                            "role": "assistant",
                            "content": final_message.content
                        })

                        # Add user message with ALL tool results
                        messages.append({
                            "role": "user",
                            "content": tool_results
                        })

                    # If timeout triggered or no tool use, we're done
                    if timeout_triggered or not has_tool_use:
                        break

        except Exception as e:
            yield f"\n\n⚠️ Error executing {self.role}: {str(e)}"


class DebateAgentsManager:
    """
    Manages all debate agents and their configurations.
    Loads from agents.yaml and tasks.yaml.
    """
    
    def __init__(self, config_dir: Path = None):
        """
        Initialize the debate agents manager.
        
        Args:
            config_dir: Path to config directory (defaults to src/academic_debate_council/config)
        """
        if config_dir is None:
            # Default to the config directory
            base_dir = Path(__file__).parent
            config_dir = base_dir / 'config'
        
        self.config_dir = config_dir
        self.agents_config = self._load_yaml('agents.yaml')
        self.tasks_config = self._load_yaml('tasks.yaml')
        
        # Create agent executors
        self.agents = self._create_agents()
        
        # Define the 12-task sequence
        self.task_sequence = self._define_task_sequence()
    
    def _load_yaml(self, filename: str) -> Dict:
        """Load YAML configuration file."""
        filepath = self.config_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Config file not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _create_agents(self) -> Dict[str, AgentExecutor]:
        """Create AgentExecutor instances for all agents."""
        agents = {}
        
        for agent_name, agent_config in self.agents_config.items():
            agents[agent_name] = AgentExecutor(agent_name, agent_config)
        
        return agents
    
    def _define_task_sequence(self) -> List[Dict]:
        """
        Define the sequence of 12 tasks with their agent assignments.
        
        Returns:
            List of task configurations
        """
        # Map tasks to agent names (from agents.yaml keys)
        sequence = [
            {
                'task_num': 1,
                'task_name': 'spiritual_analysis',
                'agent_key': 'sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert',
                'category': 'Round 1',
                'emoji': '🕌'
            },
            {
                'task_num': 2,
                'task_name': 'emotional_analysis',
                'agent_key': 'dr_layla_al_qalb___emotional_pillar_expert',
                'category': 'Round 1',
                'emoji': '❤️'
            },
            {
                'task_num': 3,
                'task_name': 'intellectual_analysis',
                'agent_key': 'dr_hassan_al_hikmah___intellectual_pillar_expert',
                'category': 'Round 1',
                'emoji': '🧠'
            },
            {
                'task_num': 4,
                'task_name': 'physical_analysis',
                'agent_key': 'dr_fatima_al_jism___physical_pillar_expert',
                'category': 'Round 1',
                'emoji': '💪'
            },
            {
                'task_num': 5,
                'task_name': 'social_analysis',
                'agent_key': 'dr_aisha_al_mujtama___social_pillar_expert',
                'category': 'Round 1',
                'emoji': '🤝'
            },
            {
                'task_num': 6,
                'task_name': 'orchestrator_analysis_question_assignment',
                'agent_key': 'dr_yusuf_al_mudeer___debate_orchestrator',
                'category': 'Moderation',
                'emoji': '⚖️'
            },
            {
                'task_num': 7,
                'task_name': 'emotional_agent_response_to_orchestrator',
                'agent_key': 'dr_layla_al_qalb___emotional_pillar_expert',
                'category': 'Round 2',
                'emoji': '❤️'
            },
            {
                'task_num': 8,
                'task_name': 'intellectual_agent_response_to_orchestrator',
                'agent_key': 'dr_hassan_al_hikmah___intellectual_pillar_expert',
                'category': 'Round 2',
                'emoji': '🧠'
            },
            {
                'task_num': 9,
                'task_name': 'physical_agent_response_to_orchestrator',
                'agent_key': 'dr_fatima_al_jism___physical_pillar_expert',
                'category': 'Round 2',
                'emoji': '💪'
            },
            {
                'task_num': 10,
                'task_name': 'social_agent_response_to_orchestrator',
                'agent_key': 'dr_aisha_al_mujtama___social_pillar_expert',
                'category': 'Round 2',
                'emoji': '🤝'
            },
            {
                'task_num': 11,
                'task_name': 'spiritual_agent_response_to_orchestrator',
                'agent_key': 'sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert',
                'category': 'Round 2',
                'emoji': '🕌'
            },
            {
                'task_num': 12,
                'task_name': 'integrated_wellbeing_assessment',
                'agent_key': 'dr_amira_al_tawhid___synthesizer',
                'category': 'Synthesis',
                'emoji': '📊'
            }
        ]
        
        return sequence
    
    def get_task_info(self, task_num: int) -> Dict:
        """Get information about a specific task."""
        if 1 <= task_num <= len(self.task_sequence):
            return self.task_sequence[task_num - 1]
        return None
    
    def get_agent_for_task(self, task_num: int) -> AgentExecutor:
        """Get the agent executor for a specific task number."""
        task_info = self.get_task_info(task_num)
        if task_info:
            agent_key = task_info['agent_key']
            return self.agents.get(agent_key)
        return None
    
    def get_task_description(self, task_name: str) -> str:
        """Get the task description from tasks.yaml."""
        task_config = self.tasks_config.get(task_name, {})
        return task_config.get('description', '')
    
    def get_agent_display_name(self, agent_key: str) -> str:
        """Get the display name for an agent."""
        agent_config = self.agents_config.get(agent_key, {})
        role = agent_config.get('role', agent_key)
        # Extract name from role (e.g., "Sheikh Dr. Ibrahim al-Tazkiyah - Spiritual Pillar Expert")
        if ' - ' in role:
            return role.split(' - ')[0]
        return role
