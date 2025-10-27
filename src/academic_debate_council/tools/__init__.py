"""
Verification Tools for Academic Debate Council

This package provides API-based tools for verifying citations, Islamic texts,
and fact-checking claims to eliminate hallucinated sources.
"""

# Citation verification tools
from .citation_verifier import (
    CitationVerifierTool,
    MedicalClaimVerifierTool,
    verify_citation_standalone,
    verify_medical_claim_standalone
)

# Islamic text verification tools
from .islamic_texts import (
    HadithSearchTool,
    QuranVerseTool,
    ShamelaSearchTool,
    MadhabFatwaTool,
    search_hadith_standalone,
    get_quran_verse_standalone,
    search_shamela_standalone,
    search_madhab_fatwa_standalone
)

# Fact-checking and search tools
from .fact_checker import (
    BraveSearchTool,
    PerplexityFactCheckTool,
    QatarStatsTool,
    brave_search_standalone,
    perplexity_fact_check_standalone,
    get_qatar_stats_standalone
)

# Legacy custom tool (keep for backwards compatibility)
from .custom_tool import MyCustomTool

__all__ = [
    # Citation verification
    'CitationVerifierTool',
    'MedicalClaimVerifierTool',
    'verify_citation_standalone',
    'verify_medical_claim_standalone',
    
    # Islamic texts
    'HadithSearchTool',
    'QuranVerseTool',
    'ShamelaSearchTool',
    'MadhabFatwaTool',
    'search_hadith_standalone',
    'get_quran_verse_standalone',
    'search_shamela_standalone',
    'search_madhab_fatwa_standalone',
    
    # Fact-checking
    'BraveSearchTool',
    'PerplexityFactCheckTool',
    'QatarStatsTool',
    'brave_search_standalone',
    'perplexity_fact_check_standalone',
    'get_qatar_stats_standalone',
    
    # Legacy
    'MyCustomTool'
]
