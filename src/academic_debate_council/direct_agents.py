"""
Direct Claude API integration for TRUE real-time streaming.
Each agent calls Claude API directly, allowing UI updates between agents.
"""

import os
from anthropic import Anthropic
from typing import Dict, List
import streamlit as st


class DirectAgent:
    """Agent that calls Claude API directly for immediate streaming."""
    
    def __init__(self, name: str, role: str, goal: str, backstory: str, model: str = "claude-sonnet-4-20250514"):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def execute_task(self, task_description: str, context: List[str] = None, topic: str = "") -> str:
        """
        Execute a task by calling Claude API directly.
        Returns the agent's response.
        """
        # Build context from previous agents
        context_text = ""
        if context:
            context_text = "\n\n**Previous Expert Analyses:**\n" + "\n\n".join(context)
        
        # Build the prompt
        system_prompt = f"""You are {self.name}.

**Your Role:** {self.role}

**Your Goal:** {self.goal}

**Your Background:** {self.backstory}

**Instructions:**
{task_description}

**Topic to Analyze:** {topic}

{context_text}

Provide your analysis now. Be thorough, cite sources properly, and follow your goal exactly."""

        # Call Claude API
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.3,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": f"Analyze this wellbeing topic: {topic}"}
                ]
            )
            
            # Extract text from response
            return response.content[0].text
            
        except Exception as e:
            return f"Error executing task: {str(e)}"


def create_debate_agents() -> List[DirectAgent]:
    """Create all 7 debate agents with their configurations."""
    
    agents = [
        DirectAgent(
            name="Sheikh Dr. Ibrahim al-Tazkiyah",
            role="Spiritual Pillar Expert",
            goal="""You ALWAYS speak FIRST. Provide spiritual foundation through: (1) Islamic Foundation with Quranic verses (cite surah:ayah), hadith (cite source), classical scholars. (2) Maqasid al-Shariah Analysis - which objectives affected? (3) Spiritual Impact on tazkiyah, taqwa, ikhlas. (4) Three scores from -3 to +3: Connection to Allah, Purposeful Living, Inner Purification. Keep to 400-600 words.""",
            backstory="Distinguished Islamic scholar, PhD from Al-Azhar, 30+ years in spiritual psychology. Expert in Quranic sciences, hadith, maqasid al-shariah.",
            model="claude-opus-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Layla al-Qalb",
            role="Emotional Pillar Expert",
            goal="""You speak SECOND. Start with "Sheikh al-Tazkiyah established [X]..." Build on spiritual foundation through: (1) Emotional landscape analysis. (2) Islamic Emotional Framework (Al-Ghazali). (3) Cite 2-3 psychological studies (Author, Year, Journal). (4) Three scores: Balance, Resilience, Transformation. 500-700 words.""",
            backstory="Clinical psychologist, Harvard PhD, 15 years in Doha. Expert in emotion regulation, positive psychology, Islamic emotional frameworks.",
            model="claude-sonnet-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Hassan al-Hikmah",
            role="Intellectual Pillar Expert",
            goal="""You speak THIRD. Start with "Sheikh al-Tazkiyah and Dr. al-Qalb showed [X], yet intellectually I must ask..." CHALLENGE assumptions. Analyze: (1) Knowledge classification. (2) Learning mechanisms (Bloom's taxonomy). (3) Islamic intellectual tradition. (4) Pose 2-3 critical questions. (5) Three scores: Truth-Seeking, Wisdom, Contemplation. 500-700 words.""",
            backstory="Cambridge PhD in Philosophy of Education, 30 years researching learning sciences and Islamic epistemology.",
            model="claude-sonnet-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Fatima al-Jism",
            role="Physical Pillar Expert",
            goal="""You speak FOURTH. Ground abstract concepts in measurable health outcomes. Cite 3-4 studies with quantitative data (RR, OR, effect sizes). Include Gulf epidemiology. Islamic bioethics (body as Amanah). Three scores: Health, Strength, Prevention. 500-700 words.""",
            backstory="Public health physician, MD from Weill Cornell-Qatar, DrPH from Johns Hopkins. Expert in evidence-based medicine, Gulf epidemiology.",
            model="claude-sonnet-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Aisha al-Mujtama'",
            role="Social Pillar Expert",
            goal="""You speak FIFTH. Reference ALL FOUR prior experts. Analyze: (1) Social structure (micro/meso/macro). (2) Power & inequality - who benefits? (3) Gulf context (expat-national, kafala, gender). (4) Apply sociological theory. (5) Identify 2-3 tensions for synthesizer. Three scores: Care, Cooperation, Responsibility. 600-800 words.""",
            backstory="LSE PhD in Sociology, 28 years researching Gulf societies. Expert in Ibn Khaldun, Qatar demographics, social theory.",
            model="claude-sonnet-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Yusuf al-Mudeer",
            role="Debate Orchestrator",
            goal="""Read ALL FIVE analyses. Identify 2-3 BIGGEST tensions where experts contradict. Pose ONE challenging question to 3-4 experts that forces them to address contrary claims. Be DIRECT and CRITICAL. 400-500 words.""",
            backstory="Senior academic administrator, 25 years chairing interdisciplinary panels. Expert in Socratic method, critical discourse, productive conflict.",
            model="claude-sonnet-4-20250514"
        ),
        
        DirectAgent(
            name="Dr. Amira al-Tawhid",
            role="Synthesizer",
            goal="""Read the COMPLETE debate. Produce comprehensive 1500-2000 word report with: Executive Summary, Round 1 Summary, Key Tensions, Resolution Status, Cross-Pillar Synergies, Integrated Assessment, Recommendations, Conclusion. Be scrupulously fair to all perspectives.""",
            backstory="Oxford DPhil in Systems Thinking, 20 years as editor-in-chief of Journal of Integrated Wellbeing Studies. Expert in complex adaptive systems, cross-disciplinary synthesis.",
            model="claude-opus-4-20250514"
        )
    ]
    
    return agents


def get_task_descriptions() -> List[str]:
    """Get task descriptions for each of the 12 tasks."""
    
    return [
        # Round 1: Initial Analyses (Tasks 1-5)
        "Provide your initial spiritual analysis of this topic.",
        "Provide your initial emotional analysis, building on the spiritual foundation.",
        "Provide your initial intellectual analysis, engaging with prior perspectives.",
        "Provide your initial physical health analysis with quantitative evidence.",
        "Provide your initial social analysis, integrating all four prior perspectives.",
        
        # Orchestrator (Task 6)
        "Identify the key tensions and contradictions between the five expert analyses. Pose challenging questions.",
        
        # Round 2: Expert Responses (Tasks 7-11)
        "Respond to the orchestrator's question about your emotional analysis (300-400 words).",
        "Respond to the orchestrator's question about your intellectual analysis (300-400 words).",
        "Respond to the orchestrator's question about your physical analysis (300-400 words).",
        "Respond to the orchestrator's question about your social analysis (300-400 words).",
        "Respond to the orchestrator's question about your spiritual analysis (300-400 words).",
        
        # Final Synthesis (Task 12)
        "Provide your comprehensive integrated synthesis of the entire two-round debate.",
    ]
