"""
Agent Integration Example

This example shows how to integrate verification tools with your CrewAI agents
to eliminate hallucinated citations and improve factual accuracy.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Import verification tools
from academic_debate_council.tools import (
    # Citation verification
    CitationVerifierTool,
    MedicalClaimVerifierTool,
    
    # Islamic texts
    HadithSearchTool,
    QuranVerseTool,
    
    # Fact-checking
    BraveSearchTool,
    QatarStatsTool
)

# Load environment variables
load_dotenv()


def create_enhanced_agents():
    """
    Create agents with verification tools integrated.
    
    Returns:
        dict: Dictionary of enhanced agents
    """
    
    # Physical & Health Agent with citation verification
    physical_agent = Agent(
        role="Physical & Health Analyst",
        goal="Analyze physical health and wellbeing aspects with verified sources",
        backstory=(
            "You are a health researcher with expertise in evidence-based medicine. "
            "You ALWAYS verify citations before making claims. "
            "You have access to PubMed and Semantic Scholar to verify research papers."
        ),
        tools=[
            CitationVerifierTool(),
            MedicalClaimVerifierTool(),
            BraveSearchTool()
        ],
        verbose=True
    )
    
    # Spiritual Agent with Islamic text verification
    spiritual_agent = Agent(
        role="Islamic Spiritual Advisor",
        goal="Provide Islamic perspective with authenticated sources",
        backstory=(
            "You are a knowledgeable Islamic scholar trained in traditional Islamic sciences. "
            "You ALWAYS verify hadith and Quranic references before citing them. "
            "You have access to authenticated hadith collections and Quranic texts."
        ),
        tools=[
            HadithSearchTool(),
            QuranVerseTool()
        ],
        verbose=True
    )
    
    # Social Agent with Qatar statistics
    social_agent = Agent(
        role="Social & Economic Analyst",
        goal="Analyze social and economic aspects with verified data",
        backstory=(
            "You are a social scientist specializing in Gulf states, particularly Qatar. "
            "You ALWAYS verify statistics before citing them. "
            "You have access to official Qatar government data and web search."
        ),
        tools=[
            QatarStatsTool(),
            BraveSearchTool(),
            CitationVerifierTool()
        ],
        verbose=True
    )
    
    return {
        'physical': physical_agent,
        'spiritual': spiritual_agent,
        'social': social_agent
    }


def create_verification_tasks(topic: str, agents: dict):
    """
    Create tasks that require agents to verify their sources.
    
    Args:
        topic: The topic to analyze
        agents: Dictionary of agents
        
    Returns:
        list: List of tasks
    """
    
    # Task 1: Physical agent analyzes with verified citations
    physical_task = Task(
        description=(
            f"Analyze the physical and health aspects of: {topic}\n\n"
            "VERIFICATION PROTOCOL:\n"
            "1. Before citing any research study, use verify_citation tool\n"
            "2. For medical claims, use verify_medical_claim tool\n"
            "3. Mark verified citations with [VERIFIED]\n"
            "4. If citation cannot be verified, reframe as general statement\n"
            "5. Never cite sources you cannot verify\n\n"
            "Provide your analysis with only verified sources."
        ),
        agent=agents['physical'],
        expected_output="Health analysis with verified citations"
    )
    
    # Task 2: Spiritual agent analyzes with verified Islamic texts
    spiritual_task = Task(
        description=(
            f"Analyze the Islamic spiritual perspective on: {topic}\n\n"
            "VERIFICATION PROTOCOL:\n"
            "1. Before citing hadith, use search_hadith tool to verify\n"
            "2. Before citing Quran, use get_quran_verse tool to verify\n"
            "3. Cite verified hadith as: [Collection Book:Number]\n"
            "4. Cite Quran as: [Quran Surah:Ayah]\n"
            "5. If source cannot be verified, use general Islamic principles\n\n"
            "Provide your analysis with only verified Islamic sources."
        ),
        agent=agents['spiritual'],
        expected_output="Islamic perspective with verified sources"
    )
    
    # Task 3: Social agent analyzes with verified Qatar data
    social_task = Task(
        description=(
            f"Analyze the social and economic aspects of: {topic}\n\n"
            "VERIFICATION PROTOCOL:\n"
            "1. For Qatar statistics, use get_qatar_statistics tool\n"
            "2. For academic sources, use verify_citation tool\n"
            "3. For current information, use brave_search tool\n"
            "4. Always cite sources with URLs when available\n"
            "5. Never cite statistics you cannot verify\n\n"
            "Provide your analysis with only verified data and sources."
        ),
        agent=agents['social'],
        expected_output="Social analysis with verified data"
    )
    
    return [physical_task, spiritual_task, social_task]


def run_verified_analysis(topic: str):
    """
    Run a complete analysis with verification.
    
    Args:
        topic: Topic to analyze
        
    Returns:
        str: Analysis results
    """
    
    print("=" * 80)
    print(f"🔍 VERIFIED ANALYSIS: {topic}")
    print("=" * 80)
    print()
    
    # Create agents with verification tools
    print("🤖 Creating agents with verification tools...")
    agents = create_enhanced_agents()
    
    # Create verification tasks
    print("📋 Creating verification tasks...")
    tasks = create_verification_tasks(topic, agents)
    
    # Create crew
    print("👥 Assembling crew...")
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )
    
    # Execute
    print("🚀 Starting verified analysis...\n")
    result = crew.kickoff()
    
    return result


# Example usage with research phase
def run_with_research_phase(topic: str):
    """
    Run analysis with pre-query research phase.
    This gathers verified sources BEFORE agents analyze.
    
    Args:
        topic: Topic to analyze
        
    Returns:
        str: Analysis results
    """
    
    from academic_debate_council.tools import (
        verify_medical_claim_standalone,
        search_hadith_standalone,
        brave_search_standalone,
        get_qatar_stats_standalone
    )
    
    print("=" * 80)
    print(f"🔍 PRE-QUERY RESEARCH PHASE: {topic}")
    print("=" * 80)
    print()
    
    # Phase 1: Gather research
    print("📚 Phase 1: Gathering verified sources...")
    print("-" * 80)
    
    research = {}
    
    # Medical research
    print("\n1️⃣ Searching medical literature (PubMed)...")
    medical_result = verify_medical_claim_standalone(
        keywords=topic,
        max_results=5
    )
    research['medical_studies'] = medical_result['data']
    print("   ✅ Medical literature search complete")
    
    # Islamic sources
    print("\n2️⃣ Searching Islamic texts...")
    hadith_result = search_hadith_standalone(
        query=topic,
        collections=['bukhari', 'muslim'],
        max_results=3
    )
    research['islamic_sources'] = hadith_result['data']
    print("   ✅ Islamic text search complete")
    
    # Qatar data (if API key available)
    if os.getenv('BRAVE_API_KEY'):
        print("\n3️⃣ Searching Qatar statistics...")
        qatar_result = get_qatar_stats_standalone(topic=topic)
        research['qatar_data'] = qatar_result['data']
        print("   ✅ Qatar statistics search complete")
    
    # Web search (if API key available)
    if os.getenv('BRAVE_API_KEY'):
        print("\n4️⃣ Searching academic web sources...")
        web_result = brave_search_standalone(
            query=f"{topic} academic research",
            academic_only=True,
            max_results=10
        )
        research['web_sources'] = web_result['data']
        print("   ✅ Web search complete")
    
    print("\n" + "=" * 80)
    print("📊 RESEARCH SUMMARY")
    print("=" * 80)
    for source_type, content in research.items():
        print(f"\n{source_type.upper()}:")
        print(content[:300] + "..." if len(content) > 300 else content)
    
    print("\n\n" + "=" * 80)
    print("🤖 Phase 2: Agent Analysis with Research Context")
    print("=" * 80)
    print()
    
    # Phase 2: Run agents with research context
    # You would pass the research results to your agents here
    # For now, we'll just show how the research is structured
    
    return research


# Main execution
if __name__ == "__main__":
    
    # Example 1: Simple verified analysis
    print("\n" + "=" * 80)
    print("EXAMPLE 1: VERIFIED ANALYSIS")
    print("=" * 80)
    
    topic1 = "The impact of workplace discrimination on mental health"
    
    try:
        result = run_verified_analysis(topic1)
        print("\n✅ Analysis complete!")
        print(result)
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Analysis with research phase
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: ANALYSIS WITH RESEARCH PHASE")
    print("=" * 80)
    
    topic2 = "Islamic ethics in modern employment practices"
    
    try:
        research = run_with_research_phase(topic2)
        print("\n✅ Research phase complete!")
        print("\nNext step: Pass this research to your agents for analysis")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Quick tool testing
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: QUICK TOOL TESTS")
    print("=" * 80)
    
    from academic_debate_council.tools import (
        verify_citation_standalone,
        get_quran_verse_standalone
    )
    
    # Test citation verification
    print("\n📚 Testing citation verification:")
    citation_result = verify_citation_standalone(
        author="Beck",
        year="1979",
        title_keywords="cognitive therapy depression"
    )
    print(citation_result['data'][:500] + "...")
    
    # Test Quran retrieval
    print("\n📖 Testing Quran verse retrieval:")
    quran_result = get_quran_verse_standalone(surah=49, ayah=13)
    print(quran_result['data'][:500] + "...")
    
    print("\n" + "=" * 80)
    print("🎉 All examples complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review VERIFICATION_TOOLS_GUIDE.md for detailed integration")
    print("2. Update your actual agent configurations")
    print("3. Test with real topics")
    print("4. Measure citation accuracy improvement")
