"""
Citation Verification Tools for Academic Debate System

This module provides tools to verify academic citations using:
- Semantic Scholar API (for general academic papers)
- PubMed API (for medical/health research)

Both APIs are FREE and require NO API keys for basic usage.
API key is OPTIONAL for Semantic Scholar to get higher rate limits.
"""

from crewai.tools import BaseTool
from typing import Type, Dict, Any, Optional, List
from pydantic import BaseModel, Field
import requests
import time
import os


class SemanticScholarInput(BaseModel):
    """Input schema for Semantic Scholar citation verification."""
    author: str = Field(..., description="Primary author's last name")
    year: str = Field(..., description="Publication year")
    title_keywords: str = Field(..., description="Key words from the paper title")


class PubMedSearchInput(BaseModel):
    """Input schema for PubMed medical claim verification."""
    keywords: str = Field(..., description="Keywords to search in medical literature")
    max_results: int = Field(default=5, description="Maximum number of results to return")


class CitationVerifierTool(BaseTool):
    """
    Verify academic citations using Semantic Scholar API.
    
    This tool searches for papers by author, year, and title keywords
    to confirm if a citation exists and retrieve accurate metadata.
    """
    
    name: str = "verify_citation"
    description: str = (
        "Verify if an academic citation exists using Semantic Scholar API. "
        "Provide author last name, publication year, and title keywords. "
        "Returns paper details including title, authors, venue, and citation count. "
        "Use this BEFORE making specific claims about research papers."
    )
    args_schema: Type[BaseModel] = SemanticScholarInput
    
    def _run(self, author: str, year: str, title_keywords: str) -> str:
        """
        Verify citation using Semantic Scholar API (Bulk Search endpoint).
        
        Based on Semantic Scholar official tutorial:
        https://www.semanticscholar.org/product/api/tutorial
        
        Args:
            author: Primary author's last name
            year: Publication year
            title_keywords: Key words from paper title
            
        Returns:
            JSON string with paper details or verification failure message
        """
        try:
            # Use bulk search endpoint (more efficient and supports better filtering)
            base_url = "https://api.semanticscholar.org/graph/v1/paper/search/bulk"
            
            # Construct optimized search query using best practices:
            # - Quoted phrases for exact matching
            # - Author name and title keywords
            query = f'{author} "{title_keywords}"'
            
            # Request comprehensive fields
            params = {
                'query': query,
                'year': year,  # Year filter for precise matching
                'fields': 'paperId,title,authors,year,venue,citationCount,influentialCitationCount,abstract,externalIds,publicationTypes,publicationDate,url',
                'sort': 'citationCount:desc'  # Sort by most cited first
            }
            
            # Check for optional API key (higher rate limits)
            headers = {}
            api_key = os.getenv('SEMANTIC_SCHOLAR_API_KEY')
            if api_key:
                headers['x-api-key'] = api_key
            
            # Add delay to respect rate limits
            time.sleep(0.1)
            
            # Make request with timeout
            response = requests.get(base_url, params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Bulk search returns 'data' array directly
                papers = data.get('data', [])
                
                # Get multiple results and find best match
                all_papers: List[Dict] = []
                token = data.get('token')
                
                # Collect papers from first batch
                all_papers.extend(papers)
                
                # Get more results if token exists (pagination)
                # Limit to 3 batches to avoid excessive API calls
                batch_count = 1
                while token and batch_count < 3:
                    time.sleep(0.1)
                    next_response = requests.get(
                        base_url,
                        params={**params, 'token': token},
                        headers=headers,
                        timeout=15
                    )
                    if next_response.status_code == 200:
                        next_data = next_response.json()
                        all_papers.extend(next_data.get('data', []))
                        token = next_data.get('token')
                        batch_count += 1
                    else:
                        break
                
                if all_papers:
                    # Sort by citation count (most cited = most reliable)
                    all_papers.sort(key=lambda p: p.get('citationCount', 0), reverse=True)
                    best_match = all_papers[0]
                    
                    # Extract comprehensive metadata
                    result = {
                        'exists': True,
                        'paper_id': best_match.get('paperId', 'Unknown'),
                        'title': best_match.get('title', 'Unknown'),
                        'authors': [a.get('name', 'Unknown') for a in best_match.get('authors', [])],
                        'year': best_match.get('year', 'Unknown'),
                        'venue': best_match.get('venue', 'Unknown'),
                        'citation_count': best_match.get('citationCount', 0),
                        'influential_citations': best_match.get('influentialCitationCount', 0),
                        'doi': best_match.get('externalIds', {}).get('DOI', 'Not available'),
                        'pub_types': best_match.get('publicationTypes', []),
                        'pub_date': best_match.get('publicationDate', 'Unknown'),
                        'url': best_match.get('url', f"https://www.semanticscholar.org/paper/{best_match.get('paperId', '')}"),
                        'abstract_preview': (best_match.get('abstract', '')[:250] + '...') if best_match.get('abstract') else 'Not available',
                        'total_found': len(all_papers)
                    }
                    
                    # Format comprehensive response
                    pub_types_str = ', '.join(result['pub_types']) if result['pub_types'] else 'Not specified'
                    
                    formatted = (
                        f"✅ CITATION VERIFIED\n\n"
                        f"Title: {result['title']}\n"
                        f"Authors: {', '.join(result['authors'][:3])}{' et al.' if len(result['authors']) > 3 else ''}\n"
                        f"Year: {result['year']}\n"
                        f"Venue: {result['venue']}\n"
                        f"Citations: {result['citation_count']}\n"
                        f"DOI: {result['doi']}\n\n"
                        f"Abstract Preview: {result['abstract_preview']}\n\n"
                        f"✅ VERIFIED REFERENCE: You may cite this paper with confidence."
                    )
                    
                    return formatted
                else:
                    return (
                        f"❌ CITATION NOT FOUND\n\n"
                        f"Search query: {query}\n\n"
                        f"No matching papers found in Semantic Scholar database.\n"
                        f"RECOMMENDATION: Either search with different keywords or "
                        f"reframe your claim without this specific citation. "
                        f"Use phrases like 'Research suggests...' or 'Studies indicate...' "
                        f"without citing a specific paper."
                    )
            else:
                # Handle rate limiting gracefully
                if response.status_code == 429:
                    return (
                        f"⚠️ RATE LIMIT REACHED\n\n"
                        f"Semantic Scholar API has reached its rate limit.\n\n"
                        f"RECOMMENDATION: Proceed with general research principles.\n"
                        f"Use phrases like:\n"
                        f"- 'Research in this area suggests...'\n"
                        f"- 'Studies have shown...'\n"
                        f"- 'Academic literature indicates...'\n\n"
                        f"Avoid citing specific papers you cannot verify."
                    )
                else:
                    return (
                        f"⚠️ API ERROR (Status {response.status_code})\n\n"
                        f"Could not verify citation at this time. "
                        f"Please proceed without this specific citation."
                    )
                
        except requests.exceptions.Timeout:
            return "⚠️ REQUEST TIMEOUT: Could not verify citation. Proceed without specific citation."
        except Exception as e:
            return f"⚠️ ERROR: {str(e)}. Proceed without specific citation."


class MedicalClaimVerifierTool(BaseTool):
    """
    Verify medical/health claims using PubMed API.
    
    This tool searches PubMed (official NIH database) for medical
    research papers matching specific keywords.
    """
    
    name: str = "verify_medical_claim"
    description: str = (
        "Search PubMed (NIH medical database) to verify medical or health-related claims. "
        "Provide keywords related to the medical claim. "
        "Returns number of relevant studies found and their PubMed IDs. "
        "Use this for any health, medical, or clinical claims."
    )
    args_schema: Type[BaseModel] = PubMedSearchInput
    
    def _run(self, keywords: str, max_results: int = 5) -> str:
        """
        Search PubMed for medical research.
        
        Args:
            keywords: Search keywords for medical literature
            max_results: Maximum number of results to return
            
        Returns:
            JSON string with search results or failure message
        """
        try:
            # Step 1: Search for PMIDs
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            
            search_params = {
                'db': 'pubmed',
                'term': keywords,
                'retmode': 'json',
                'retmax': max_results,
                'sort': 'relevance'
            }
            
            time.sleep(0.1)  # Respect rate limits
            
            search_response = requests.get(search_url, params=search_params, timeout=10)
            
            if search_response.status_code != 200:
                return f"⚠️ PubMed API Error (Status {search_response.status_code})"
            
            search_data = search_response.json()
            
            if 'esearchresult' not in search_data:
                return "⚠️ PubMed API returned unexpected format"
            
            result = search_data['esearchresult']
            count = int(result.get('count', 0))
            pmids = result.get('idlist', [])
            
            if count == 0:
                return (
                    f"❌ NO MEDICAL STUDIES FOUND\n\n"
                    f"Search keywords: {keywords}\n\n"
                    f"No studies found in PubMed database.\n"
                    f"RECOMMENDATION: Reframe your claim without specific medical citations "
                    f"or use more general language like 'Medical research suggests...' "
                    f"without citing specific studies."
                )
            
            # Step 2: Get details for found PMIDs
            if pmids:
                summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
                
                summary_params = {
                    'db': 'pubmed',
                    'id': ','.join(pmids[:3]),  # Get details for top 3
                    'retmode': 'json'
                }
                
                time.sleep(0.1)
                
                summary_response = requests.get(summary_url, params=summary_params, timeout=10)
                
                if summary_response.status_code == 200:
                    summary_data = summary_response.json()
                    
                    papers = []
                    if 'result' in summary_data:
                        for pmid in pmids[:3]:
                            if pmid in summary_data['result']:
                                paper_data = summary_data['result'][pmid]
                                papers.append({
                                    'pmid': pmid,
                                    'title': paper_data.get('title', 'Unknown'),
                                    'authors': paper_data.get('authors', [{}])[0].get('name', 'Unknown') if paper_data.get('authors') else 'Unknown',
                                    'pubdate': paper_data.get('pubdate', 'Unknown'),
                                    'source': paper_data.get('source', 'Unknown')
                                })
                    
                    formatted = (
                        f"✅ MEDICAL STUDIES FOUND\n\n"
                        f"Search keywords: {keywords}\n"
                        f"Total studies found: {count}\n\n"
                        f"Top Results:\n"
                    )
                    
                    for i, paper in enumerate(papers, 1):
                        formatted += (
                            f"\n{i}. {paper['title']}\n"
                            f"   First Author: {paper['authors']}\n"
                            f"   Date: {paper['pubdate']}\n"
                            f"   Journal: {paper['source']}\n"
                            f"   PMID: {paper['pmid']}\n"
                            f"   Link: https://pubmed.ncbi.nlm.nih.gov/{paper['pmid']}/\n"
                        )
                    
                    formatted += (
                        f"\n✅ These are VERIFIED medical studies from PubMed. "
                        f"You may reference this body of research with confidence."
                    )
                    
                    return formatted
            
            # Fallback if details retrieval fails
            return (
                f"✅ MEDICAL STUDIES EXIST\n\n"
                f"Search keywords: {keywords}\n"
                f"Total studies found: {count}\n"
                f"PubMed IDs: {', '.join(pmids)}\n\n"
                f"✅ Multiple studies found. You may reference this body of research."
            )
            
        except requests.exceptions.Timeout:
            return "⚠️ REQUEST TIMEOUT: Could not verify medical claim. Proceed without specific citation."
        except Exception as e:
            return f"⚠️ ERROR: {str(e)}. Proceed without specific medical citation."


# Helper function for standalone usage (non-CrewAI)
def verify_citation_standalone(author: str, year: str, title_keywords: str) -> Dict[str, Any]:
    """
    Standalone function to verify citations without CrewAI integration.
    
    Args:
        author: Primary author's last name
        year: Publication year
        title_keywords: Key words from paper title
        
    Returns:
        Dictionary with verification results
    """
    tool = CitationVerifierTool()
    result = tool._run(author=author, year=year, title_keywords=title_keywords)
    return {"status": "success", "data": result}


def verify_medical_claim_standalone(keywords: str, max_results: int = 5) -> Dict[str, Any]:
    """
    Standalone function to verify medical claims without CrewAI integration.
    
    Args:
        keywords: Search keywords for medical literature
        max_results: Maximum number of results to return
        
    Returns:
        Dictionary with verification results
    """
    tool = MedicalClaimVerifierTool()
    result = tool._run(keywords=keywords, max_results=max_results)
    return {"status": "success", "data": result}


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("CITATION VERIFICATION TOOL - TEST")
    print("=" * 80)
    
    # Test 1: Verify a real citation
    print("\n📚 TEST 1: Verifying real citation (Cipriani et al. 2018)")
    print("-" * 80)
    result1 = verify_citation_standalone(
        author="Cipriani",
        year="2018",
        title_keywords="antidepressant efficacy comparative"
    )
    print(result1['data'])
    
    # Test 2: Verify medical claim
    print("\n\n🏥 TEST 2: Verifying medical claim about depression treatment")
    print("-" * 80)
    result2 = verify_medical_claim_standalone(
        keywords="depression treatment efficacy meta-analysis",
        max_results=3
    )
    print(result2['data'])
    
    # Test 3: Try to verify non-existent citation
    print("\n\n❌ TEST 3: Attempting to verify non-existent citation")
    print("-" * 80)
    result3 = verify_citation_standalone(
        author="NotARealAuthor",
        year="2099",
        title_keywords="completely fabricated study"
    )
    print(result3['data'])
