"""
Fact-Checking and Real-Time Search Tools for Academic Debate System

This module provides tools for real-time fact-checking and web search using:
- Brave Search API (free tier available)
- Perplexity AI API (AI-powered search with citations)

These tools help verify claims, find current statistics, and access recent information.
"""

import os
import time
from typing import Type, Dict, Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import requests
from bs4 import BeautifulSoup
from openai import OpenAI


class BraveSearchInput(BaseModel):
    """Input schema for Brave Search API."""
    query: str = Field(..., description="Search query")
    academic_only: bool = Field(default=False, description="Restrict to academic sources (scholar.google.com, pubmed.gov)")
    max_results: int = Field(default=10, description="Maximum number of results")


class PerplexitySearchInput(BaseModel):
    """Input schema for Perplexity AI search."""
    claim: str = Field(..., description="Claim to fact-check")
    context: str = Field(default="", description="Additional context for the search")


class QatarStatsInput(BaseModel):
    """Input schema for Qatar statistics search."""
    topic: str = Field(..., description="Topic or indicator to search for (e.g., 'labor force', 'population', 'GDP')")


class BraveSearchTool(BaseTool):
    """
    Search the web using Brave Search API.
    
    Brave Search offers a generous free tier (2000 searches/month)
    and provides high-quality, privacy-focused search results.
    """
    
    name: str = "brave_search"
    description: str = (
        "Search the web using Brave Search API. "
        "Can restrict searches to academic sources only. "
        "Returns titles, URLs, and descriptions of top results. "
        "Use this to find recent information, statistics, or verify claims."
    )
    args_schema: Type[BaseModel] = BraveSearchInput
    
    def _run(self, query: str, academic_only: bool = False, max_results: int = 10) -> str:
        """
        Perform web search using Brave Search API.
        
        Args:
            query: Search query
            academic_only: If True, restrict to academic sources
            max_results: Maximum number of results
            
        Returns:
            Formatted string with search results
        """
        api_key = os.getenv('BRAVE_API_KEY')
        
        if not api_key:
            return (
                "⚠️ BRAVE API KEY NOT CONFIGURED\n\n"
                "To use web search, you need a FREE API key:\n"
                "1. Visit: https://brave.com/search/api/\n"
                "2. Sign up for free tier (2000 searches/month)\n"
                "3. Add to .env file: BRAVE_API_KEY=your_key_here\n\n"
                "For now, proceed without real-time web search or manually verify claims."
            )
        
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key
            }
            
            # Modify query for academic-only search
            if academic_only:
                query = f"{query} (site:scholar.google.com OR site:pubmed.gov OR site:arxiv.org OR site:jstor.org OR site:researchgate.net)"
            
            params = {
                'q': query,
                'count': min(max_results, 20),  # API limit
                'search_lang': 'en',
                'safesearch': 'moderate'
            }
            
            time.sleep(0.1)
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 401:
                return (
                    "⚠️ INVALID BRAVE API KEY\n\n"
                    "Your API key is invalid or expired.\n"
                    "Get a new key from: https://brave.com/search/api/"
                )
            
            if response.status_code == 429:
                return (
                    "⚠️ RATE LIMIT EXCEEDED\n\n"
                    "You've exceeded the free tier limit (2000 searches/month).\n"
                    "Wait until next month or upgrade your plan."
                )
            
            if response.status_code != 200:
                return f"⚠️ API ERROR (Status {response.status_code})"
            
            data = response.json()
            
            if 'web' not in data or 'results' not in data['web']:
                return "❌ No search results found."
            
            results = data['web']['results']
            
            if not results:
                return f"❌ NO RESULTS FOUND\n\nSearch query: {query}\n\nTry different keywords."
            
            # Format results
            formatted = (
                f"🔍 BRAVE SEARCH RESULTS\n\n"
                f"Query: {query}\n"
                f"Results found: {len(results)}\n"
                f"{'Academic sources only' if academic_only else 'General web search'}\n\n"
            )
            
            for i, result in enumerate(results[:max_results], 1):
                title = result.get('title', 'No title')
                url = result.get('url', 'No URL')
                description = result.get('description', 'No description')
                
                formatted += (
                    f"{i}. {title}\n"
                    f"   URL: {url}\n"
                    f"   {description[:150]}{'...' if len(description) > 150 else ''}\n\n"
                )
            
            formatted += (
                "✅ These are current web search results. "
                "Review and cite credible sources with URLs."
            )
            
            return formatted
            
        except requests.exceptions.Timeout:
            return "⚠️ REQUEST TIMEOUT: Search took too long."
        except Exception as e:
            return f"⚠️ ERROR: {str(e)}"


class PerplexityFactCheckTool(BaseTool):
    """
    Use Perplexity AI to fact-check claims with citations.
    
    Perplexity AI provides AI-powered search with automatic source citations.
    Great for fact-checking specific claims.
    """
    
    name: str = "perplexity_fact_check"
    description: str = (
        "Use Perplexity AI to fact-check claims with cited sources. "
        "Provide a claim to verify. "
        "Returns AI-generated response with source citations. "
        "Excellent for verifying statistics, current events, and controversial claims."
    )
    args_schema: Type[BaseModel] = PerplexitySearchInput
    
    def _run(self, claim: str, context: str = "") -> str:
        """
        Fact-check a claim using Perplexity AI with official SDK.
        
        Args:
            claim: Claim to fact-check
            context: Additional context
            
        Returns:
            Formatted string with fact-check results
        """
        api_key = os.getenv('PERPLEXITY_API_KEY')
        
        if not api_key:
            return (
                "⚠️ PERPLEXITY API KEY NOT CONFIGURED\n\n"
                "To use AI-powered fact-checking:\n"
                "1. Visit: https://www.perplexity.ai/settings/api\n"
                "2. Sign up ($5 credit includes ~1000 searches)\n"
                "3. Add to .env file: PERPLEXITY_API_KEY=your_key_here\n\n"
                "ALTERNATIVE: Use brave_search tool for manual fact-checking."
            )
        
        try:
            # Initialize OpenAI client pointing to Perplexity endpoint
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.perplexity.ai",
                timeout=30.0  # 30 second timeout
            )

            # Construct prompt
            user_prompt = f"Fact-check this claim with current, authoritative sources. Provide specific citations with URLs. Be objective and note any nuances: {claim}"
            if context:
                user_prompt += f"\n\nContext: {context}"

            # Make API call using OpenAI-compatible SDK with timeout
            completion = client.chat.completions.create(
                model="sonar",
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=1000,
                timeout=30  # 30 second timeout for this specific request
            )
            
            # Extract the fact-check result
            fact_check_result = completion.choices[0].message.content
            
            # Format response
            formatted = (
                f"🤖 PERPLEXITY AI FACT-CHECK\n\n"
                f"Claim: {claim}\n\n"
                f"Analysis:\n{fact_check_result}\n\n"
                f"✅ This fact-check includes AI-generated analysis with source citations."
            )
            
            return formatted
            
        except Exception as e:
            error_msg = str(e)
            if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
                return (
                    "⚠️ PERPLEXITY API TIMEOUT\n\n"
                    "The Perplexity API request timed out after 30 seconds.\n\n"
                    "RECOMMENDATION: Proceed with your analysis using general knowledge.\n"
                    "If you need specific fact-checking, use the brave_search tool instead."
                )
            elif "401" in error_msg or "Unauthorized" in error_msg:
                return (
                    "⚠️ INVALID PERPLEXITY API KEY\n\n"
                    "Your API key is invalid or expired.\n"
                    "Get a new key from https://www.perplexity.ai/settings/api\n\n"
                    "RECOMMENDATION: Proceed without AI fact-checking."
                )
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                return (
                    "⚠️ PERPLEXITY RATE LIMIT EXCEEDED\n\n"
                    "Too many requests to Perplexity API.\n\n"
                    "RECOMMENDATION: Proceed with your analysis using general knowledge."
                )
            else:
                return (
                    f"⚠️ PERPLEXITY API ERROR: {error_msg[:100]}\n\n"
                    f"RECOMMENDATION: Proceed without this specific fact-check."
                )


class QatarStatsTool(BaseTool):
    """
    Search for Qatar-specific statistics and data.
    
    This tool searches official Qatar government sources and reliable
    data providers for statistics about Qatar.
    """
    
    name: str = "get_qatar_statistics"
    description: str = (
        "Search for official Qatar statistics and data. "
        "Provide topic or indicator name (e.g., 'labor force participation', 'population demographics'). "
        "Returns data from Qatar Statistics Authority and other official sources. "
        "Use this for any claims about Qatar demographics, economy, or society."
    )
    args_schema: Type[BaseModel] = QatarStatsInput
    
    def _run(self, topic: str) -> str:
        """
        Search for Qatar-specific statistics.
        
        Args:
            topic: Topic or indicator to search
            
        Returns:
            Formatted string with Qatar statistics
        """
        try:
            # This is a simplified implementation that uses web search
            # A full implementation would integrate with Qatar Statistics Authority API
            
            # Use Brave Search if available
            api_key = os.getenv('BRAVE_API_KEY')
            
            if api_key:
                # Search official Qatar sources
                search_query = f"{topic} site:psa.gov.qa OR site:qnv2030.gov.qa OR site:gco.gov.qa"
                
                url = "https://api.search.brave.com/res/v1/web/search"
                
                headers = {
                    "Accept": "application/json",
                    "X-Subscription-Token": api_key
                }
                
                params = {
                    'q': search_query,
                    'count': 5,
                }
                
                time.sleep(0.1)
                
                response = requests.get(url, headers=headers, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get('web', {}).get('results', [])
                    
                    if results:
                        formatted = (
                            f"📊 QATAR STATISTICS SEARCH\n\n"
                            f"Topic: {topic}\n"
                            f"Official sources found: {len(results)}\n\n"
                        )
                        
                        for i, result in enumerate(results[:3], 1):
                            formatted += (
                                f"{i}. {result.get('title', 'No title')}\n"
                                f"   Source: {result.get('url', 'No URL')}\n"
                                f"   {result.get('description', 'No description')[:150]}...\n\n"
                            )
                        
                        formatted += (
                            "✅ Review these official sources and cite specific data with URLs.\n\n"
                            "RECOMMENDED SOURCES:\n"
                            "- Qatar Statistics Authority (psa.gov.qa)\n"
                            "- Qatar National Vision 2030 (qnv2030.gov.qa)\n"
                            "- Government Communications Office (gco.gov.qa)"
                        )
                        
                        return formatted
            
            # Fallback: Scrape Qatar official sources directly
            results = []
            
            # Try scraping World Bank Qatar page
            try:
                wb_url = "https://data.worldbank.org/country/qatar"
                time.sleep(0.2)
                response = requests.get(wb_url, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for indicator data
                    indicators = soup.find_all(['div', 'tr'], class_=['indicator', 'data-row'], limit=5)
                    
                    for indicator in indicators:
                        try:
                            name = indicator.find(['td', 'div', 'span'], class_=['indicator-name', 'name'])
                            value = indicator.find(['td', 'div', 'span'], class_=['indicator-value', 'value'])
                            year = indicator.find(['td', 'div', 'span'], class_=['indicator-year', 'year'])
                            
                            if name and value:
                                results.append({
                                    'source': 'World Bank',
                                    'indicator': name.get_text(strip=True),
                                    'value': value.get_text(strip=True),
                                    'year': year.get_text(strip=True) if year else 'Latest',
                                    'url': wb_url
                                })
                        except Exception:
                            continue
            except Exception:
                pass
            
            # Try Trading Economics Qatar page
            try:
                te_url = f"https://tradingeconomics.com/qatar/{topic.replace(' ', '-').lower()}"
                time.sleep(0.2)
                response = requests.get(te_url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for latest data
                    data_elements = soup.find_all(['div', 'td'], class_=['data-value', 'te-value'], limit=3)
                    
                    for elem in data_elements:
                        try:
                            value_text = elem.get_text(strip=True)
                            if value_text:
                                results.append({
                                    'source': 'Trading Economics',
                                    'indicator': topic,
                                    'value': value_text,
                                    'year': 'Latest',
                                    'url': te_url
                                })
                        except Exception:
                            continue
            except Exception:
                pass
            
            # Try Qatar Portal for general statistics
            try:
                qp_url = "https://portal.www.gov.qa/wps/portal/topics/Economy+and+Business/qatareconomy"
                time.sleep(0.2)
                response = requests.get(qp_url, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for statistical data
                    stats = soup.find_all(['p', 'li', 'div'], limit=10)
                    
                    for stat in stats:
                        text = stat.get_text(strip=True)
                        # Look for patterns like numbers with percentages or millions/billions
                        if any(keyword in text.lower() for keyword in ['%', 'million', 'billion', 'population', 'gdp', 'employment']):
                            if len(text) < 500 and len(text) > 20:
                                results.append({
                                    'source': 'Qatar Portal',
                                    'indicator': 'General Statistics',
                                    'value': text,
                                    'year': 'Current',
                                    'url': qp_url
                                })
                                break
            except Exception:
                pass
            
            if not results:
                return (
                    f"📊 QATAR STATISTICS: {topic}\n\n"
                    f"❌ Could not extract data via web scraping\n\n"
                    f"RECOMMENDED ACTIONS:\n"
                    f"1. Visit Qatar Statistics Authority: https://www.psa.gov.qa/\n"
                    f"2. Check World Bank Qatar: https://data.worldbank.org/country/qatar\n"
                    f"3. Review Trading Economics: https://tradingeconomics.com/qatar/indicators\n"
                    f"4. Qatar Open Data Portal: https://www.data.gov.qa/\n\n"
                    f"Cite specific numbers with URLs when available."
                )
            
            # Format scraped results
            formatted = (
                f"📊 QATAR STATISTICS (WEB SCRAPED)\n\n"
                f"Topic: {topic}\n"
                f"Data points found: {len(results)}\n\n"
            )
            
            for i, result in enumerate(results[:5], 1):
                formatted += (
                    f"{i}. {result['indicator']}\n"
                    f"   Value: {result['value']}\n"
                    f"   Year: {result['year']}\n"
                    f"   Source: {result['source']}\n"
                    f"   URL: {result['url']}\n\n"
                )
            
            formatted += (
                "✅ Data extracted from official sources. "
                "Always cite with source URLs and verify numbers are current."
            )
            
            return formatted
            
        except Exception as e:
            return f"⚠️ ERROR: {str(e)}"


# Standalone helper functions

def brave_search_standalone(query: str, academic_only: bool = False, max_results: int = 10) -> Dict[str, Any]:
    """
    Standalone function for Brave Search without CrewAI integration.
    
    Args:
        query: Search query
        academic_only: Restrict to academic sources
        max_results: Maximum results
        
    Returns:
        Dictionary with search results
    """
    tool = BraveSearchTool()
    result = tool._run(query=query, academic_only=academic_only, max_results=max_results)
    return {"status": "success", "data": result}


def perplexity_fact_check_standalone(claim: str, context: str = "") -> Dict[str, Any]:
    """
    Standalone function for Perplexity fact-checking without CrewAI integration.
    
    Args:
        claim: Claim to fact-check
        context: Additional context
        
    Returns:
        Dictionary with fact-check results
    """
    tool = PerplexityFactCheckTool()
    result = tool._run(claim=claim, context=context)
    return {"status": "success", "data": result}


def get_qatar_stats_standalone(topic: str) -> Dict[str, Any]:
    """
    Standalone function to search Qatar statistics without CrewAI integration.
    
    Args:
        topic: Topic to search
        
    Returns:
        Dictionary with statistics search results
    """
    tool = QatarStatsTool()
    result = tool._run(topic=topic)
    return {"status": "success", "data": result}


# Example usage
if __name__ == "__main__":
    print("=" * 80)
    print("FACT-CHECKING AND SEARCH TOOLS - TEST")
    print("=" * 80)
    
    # Test 1: Brave Search for academic sources
    print("\n🔍 TEST 1: Searching for academic sources on labor market in Qatar")
    print("-" * 80)
    result1 = brave_search_standalone(
        query="labor market Qatar kafala system",
        academic_only=True,
        max_results=5
    )
    print(result1['data'])
    
    # Test 2: Qatar statistics search
    print("\n\n📊 TEST 2: Searching Qatar population statistics")
    print("-" * 80)
    result2 = get_qatar_stats_standalone(topic="population demographics expatriates")
    print(result2['data'])
    
    # Test 3: Perplexity fact-check
    print("\n\n🤖 TEST 3: Fact-checking claim about Qatar economy")
    print("-" * 80)
    result3 = perplexity_fact_check_standalone(
        claim="Qatar has the highest GDP per capita in the world",
        context="Discussing economic development in Gulf states"
    )
    print(result3['data'])
    
    # Test 4: General web search
    print("\n\n🌐 TEST 4: General web search about Qatar National Vision 2030")
    print("-" * 80)
    result4 = brave_search_standalone(
        query="Qatar National Vision 2030 employment goals",
        academic_only=False,
        max_results=5
    )
    print(result4['data'])
