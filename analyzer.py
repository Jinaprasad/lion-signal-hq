"""
🦁 LION SIGNAL HQ - AI Analyzer
================================
This is the BRAIN that reads PDFs and tells you what's important.

It takes 20 PDF links, sends them to Gemini AI, and gets back smart summaries.
"""

import google.generativeai as genai
import os
import time
from config import *

class GeminiAnalyzer:
    """
    The Smart Brain that analyzes PDFs
    """
    
    def __init__(self, api_key):
        """
        Set up Gemini AI
        
        Args:
            api_key: Your Gemini API key (get free from Google AI Studio)
        """
        print("🧠 Starting Gemini Brain...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create the model
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        print(f"✅ Gemini Brain ready! Using model: {GEMINI_MODEL}")
    
    def analyze_batch(self, announcements):
        """
        Analyze a batch of announcements (up to 20)
        
        Args:
            announcements: List of announcement dictionaries with 'pdf_link'
        
        Returns:
            List of same announcements but with AI analysis added
        """
        
        if not announcements:
            return []
        
        batch_size = len(announcements)
        print(f"\n🧠 Analyzing batch of {batch_size} announcements...")
        
        # Build the prompt with all PDF links
        prompt = ANALYSIS_PROMPT + "\n\nHere are the announcements to analyze:\n\n"
        
        for i, ann in enumerate(announcements, 1):
            prompt += f"\n{i}. COMPANY: {ann.get('company', 'Unknown')}\n"
            prompt += f"   SUBJECT: {ann.get('subject', 'Unknown')}\n"
            prompt += f"   PDF URL: {ann['pdf_link']}\n"
            prompt += f"   EXCHANGE: {ann.get('exchange', 'Unknown')}\n"
            prompt += "   ---\n"
        
        prompt += "\n\nNow analyze each one and provide the structured output as specified."
        
        try:
            print("  → Sending to Gemini AI...")
            
            # Send to Gemini (with retry logic)
            for attempt in range(GEMINI_MAX_RETRIES):
                try:
                    response = self.model.generate_content(
                        prompt,
                        generation_config={
                            'temperature': 0.3,  # Low temperature = more focused
                            'max_output_tokens': 8000,  # Enough for 20 summaries
                        }
                    )
                    
                    analysis_text = response.text
                    print("  → Got response from Gemini!")
                    break
                    
                except Exception as e:
                    print(f"  ⚠️ Attempt {attempt + 1} failed: {e}")
                    if attempt < GEMINI_MAX_RETRIES - 1:
                        time.sleep(5)  # Wait before retry
                    else:
                        print("  ❌ All retries failed!")
                        return announcements  # Return without analysis
            
            # Parse the response
            analyzed = self._parse_gemini_response(analysis_text, announcements)
            
            print(f"✅ Analysis complete! Processed {len(analyzed)} announcements")
            
            return analyzed
            
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return announcements  # Return originals if analysis fails
    
    def _parse_gemini_response(self, response_text, original_announcements):
        """
        Parse Gemini's response and add analysis to announcements
        
        This is tricky because Gemini's output format might vary.
        We'll do our best to extract the structured data.
        """
        
        analyzed = []
        
        # Split response into sections (one per announcement)
        sections = response_text.split('---')
        
        for i, ann in enumerate(original_announcements):
            # Start with original data
            result = ann.copy()
            
            # Try to find matching section
            matching_section = None
            if i < len(sections):
                matching_section = sections[i]
            
            if matching_section:
                # Extract fields using simple string parsing
                result['ai_company'] = self._extract_field(matching_section, 'COMPANY')
                result['ai_headline'] = self._extract_field(matching_section, 'HEADLINE')
                result['ai_category'] = self._extract_field(matching_section, 'CATEGORY')
                result['ai_importance'] = self._extract_importance(matching_section)
                result['ai_summary'] = self._extract_field(matching_section, 'SUMMARY')
                result['ai_key_numbers'] = self._extract_field(matching_section, 'KEY_NUMBERS')
            else:
                # No analysis available - set defaults
                result['ai_company'] = ann.get('company', 'Unknown')
                result['ai_headline'] = ann.get('subject', 'Unknown')
                result['ai_category'] = 'OTHER'
                result['ai_importance'] = 5
                result['ai_summary'] = 'Analysis pending'
                result['ai_key_numbers'] = 'None'
            
            analyzed.append(result)
        
        return analyzed
    
    def _extract_field(self, text, field_name):
        """Extract a field from the response text"""
        try:
            pattern = f"{field_name}:(.+?)(?=\n[A-Z]+:|$)"
            import re
            match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
        except:
            pass
        return "Unknown"
    
    def _extract_importance(self, text):
        """Extract importance score (1-10)"""
        try:
            import re
            match = re.search(r'IMPORTANCE:\s*(\d+)', text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return max(1, min(10, score))  # Clamp between 1-10
        except:
            pass
        return 5  # Default to medium importance


def analyze_in_batches(announcements, api_key):
    """
    Helper function to analyze ALL announcements in batches of 20
    
    Args:
        announcements: Full list of announcements
        api_key: Gemini API key
    
    Returns:
        All announcements with AI analysis added
    """
    
    if not announcements:
        print("No announcements to analyze!")
        return []
    
    analyzer = GeminiAnalyzer(api_key)
    
    all_analyzed = []
    
    # Split into batches of BATCH_SIZE (from config.py)
    for i in range(0, len(announcements), BATCH_SIZE):
        batch = announcements[i:i + BATCH_SIZE]
        
        print(f"\n📦 Batch {i//BATCH_SIZE + 1} ({len(batch)} announcements)")
        
        analyzed_batch = analyzer.analyze_batch(batch)
        all_analyzed.extend(analyzed_batch)
        
        # Be nice to the API - wait between batches
        if i + BATCH_SIZE < len(announcements):
            print("  ⏱️ Waiting 3 seconds before next batch...")
            time.sleep(3)
    
    return all_analyzed


# Test if run directly
if __name__ == "__main__":
    print("Testing Gemini Analyzer...")
    
    # You need to set your API key as environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ Please set GEMINI_API_KEY environment variable")
        print("   Get your free key from: https://aistudio.google.com/apikey")
    else:
        # Test with dummy data
        test_announcements = [
            {
                'company': 'Test Company',
                'subject': 'Q3 Results',
                'pdf_link': 'https://example.com/test.pdf',
                'exchange': 'BSE'
            }
        ]
        
        analyzer = GeminiAnalyzer(api_key)
        results = analyzer.analyze_batch(test_announcements)
        
        print("\nAnalysis result:")
        print(results[0])
