import os

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Import verification tools
try:
    from academic_debate_council.tools.islamic_texts import (
        HadithSearchTool,
        QuranVerseTool,
        ShamelaSearchTool,
        MadhabFatwaTool
    )
    from academic_debate_council.tools.citation_verifier import (
        CitationVerifierTool,
        MedicalClaimVerifierTool
    )
    from academic_debate_council.tools.fact_checker import (
        BraveSearchTool,
        PerplexityFactCheckTool,
        QatarStatsTool
    )
    TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Warning: Could not import tools: {e}")
    TOOLS_AVAILABLE = False







@CrewBase
class AcademicDebateCouncilCrew:
    """AcademicDebateCouncil crew"""

    
    @agent
    def sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert(self) -> Agent:
        # Islamic verification tools for spiritual expert
        spiritual_tools = []
        if TOOLS_AVAILABLE:
            spiritual_tools = [
                HadithSearchTool(),
                QuranVerseTool(),
                ShamelaSearchTool(),
                MadhabFatwaTool()
            ]

        return Agent(
            config=self.agents_config["sheikh_dr_ibrahim_al_tazkiyah___spiritual_pillar_expert"],


            tools=spiritual_tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-opus-4-1-20250805",
                temperature=0.3,
            ),
            
        )
    
    @agent
    def dr_layla_al_qalb___emotional_pillar_expert(self) -> Agent:
        # Psychology research tools for emotional expert
        emotional_tools = []
        if TOOLS_AVAILABLE:
            emotional_tools = [
                CitationVerifierTool(),
                MedicalClaimVerifierTool()
            ]

        return Agent(
            config=self.agents_config["dr_layla_al_qalb___emotional_pillar_expert"],


            tools=emotional_tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-sonnet-4-5-20250929",
                temperature=0.4,
            ),
            
        )
    
    @agent
    def dr_hassan_al_hikmah___intellectual_pillar_expert(self) -> Agent:
        # Academic research tools for intellectual expert
        intellectual_tools = []
        if TOOLS_AVAILABLE:
            intellectual_tools = [
                CitationVerifierTool(),
                BraveSearchTool()
            ]

        return Agent(
            config=self.agents_config["dr_hassan_al_hikmah___intellectual_pillar_expert"],


            tools=intellectual_tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-sonnet-4-5-20250929",
                temperature=0.3,
            ),
            
        )
    
    @agent
    def dr_fatima_al_jism___physical_pillar_expert(self) -> Agent:
        # Medical and citation tools for physical/health expert
        physical_tools = []
        if TOOLS_AVAILABLE:
            physical_tools = [
                CitationVerifierTool(),
                MedicalClaimVerifierTool(),
                QatarStatsTool()
            ]

        return Agent(
            config=self.agents_config["dr_fatima_al_jism___physical_pillar_expert"],


            tools=physical_tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-sonnet-4-5-20250929",
                temperature=0.3,
            ),
            
        )
    
    @agent
    def dr_aisha_al_mujtama___social_pillar_expert(self) -> Agent:
        # Qatar stats and research tools for social expert
        social_tools = []
        if TOOLS_AVAILABLE:
            social_tools = [
                QatarStatsTool(),
                CitationVerifierTool(),
                BraveSearchTool()
            ]

        return Agent(
            config=self.agents_config["dr_aisha_al_mujtama___social_pillar_expert"],


            tools=social_tools,
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-sonnet-4-5-20250929",
                temperature=0.4,
            ),
            
        )
    
    @agent
    def dr_amira_al_tawhid___synthesizer(self) -> Agent:

        
        return Agent(
            config=self.agents_config["dr_amira_al_tawhid___synthesizer"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-opus-4-1-20250805",
                temperature=0.2,
            ),
            
        )
    
    @agent
    def dr_yusuf_al_mudeer___debate_orchestrator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["dr_yusuf_al_mudeer___debate_orchestrator"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="claude-sonnet-4-5-20250929",
                temperature=0.4,
            ),
            
        )
    

    
    @task
    def spiritual_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["spiritual_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def emotional_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["emotional_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def intellectual_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["intellectual_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def physical_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["physical_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def social_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["social_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def orchestrator_analysis_question_assignment(self) -> Task:
        return Task(
            config=self.tasks_config["orchestrator_analysis_question_assignment"],
            markdown=False,
            
            
        )
    
    @task
    def emotional_agent_response_to_orchestrator(self) -> Task:
        return Task(
            config=self.tasks_config["emotional_agent_response_to_orchestrator"],
            markdown=False,
            
            
        )
    
    @task
    def intellectual_agent_response_to_orchestrator(self) -> Task:
        return Task(
            config=self.tasks_config["intellectual_agent_response_to_orchestrator"],
            markdown=False,
            
            
        )
    
    @task
    def physical_agent_response_to_orchestrator(self) -> Task:
        return Task(
            config=self.tasks_config["physical_agent_response_to_orchestrator"],
            markdown=False,
            
            
        )
    
    @task
    def social_agent_response_to_orchestrator(self) -> Task:
        return Task(
            config=self.tasks_config["social_agent_response_to_orchestrator"],
            markdown=False,
            
            
        )
    
    @task
    def spiritual_agent_response_to_orchestrator(self) -> Task:
        return Task(
            config=self.tasks_config["spiritual_agent_response_to_orchestrator"],
            markdown=False,
            
            
        )
    
    @task
    def integrated_wellbeing_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["integrated_wellbeing_assessment"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AcademicDebateCouncil crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
