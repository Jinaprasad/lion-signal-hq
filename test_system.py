"""
🦁 LION SIGNAL HQ - Quick Test
===============================
Run this to test if everything works BEFORE deploying to GitHub!

This will:
1. Check if all files exist
2. Check if Python packages are installed
3. Test scraper (get 5 announcements)
4. Test Gemini analyzer (if API key set)
5. Test database
6. Show sample dashboard
"""

import os
import sys

def print_header(text):
    """Print a nice header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_mark(success):
    """Return ✅ or ❌"""
    return "✅" if success else "❌"

def test_files():
    """Check if all required files exist"""
    print_header("1. CHECKING FILES")
    
    required_files = [
        'config.py',
        'scraper.py',
        'analyzer.py',
        'database.py',
        'main.py',
        'app.py',
        'requirements.txt',
        '.github/workflows/schedule.yml',
        'templates/dashboard.html'
    ]
    
    all_good = True
    
    for file in required_files:
        exists = os.path.exists(file)
        print(f"  {check_mark(exists)} {file}")
        if not exists:
            all_good = False
    
    return all_good

def test_imports():
    """Check if all Python packages are installed"""
    print_header("2. CHECKING PYTHON PACKAGES")
    
    packages = {
        'requests': 'requests',
        'beautifulsoup4': 'bs4',
        'google.generativeai': 'google.generativeai',
        'flask': 'flask'
    }
    
    all_good = True
    
    for package_name, import_name in packages.items():
        try:
            __import__(import_name)
            print(f"  ✅ {package_name}")
        except ImportError:
            print(f"  ❌ {package_name} - Run: pip install {package_name}")
            all_good = False
    
    return all_good

def test_scraper():
    """Test the scraper"""
    print_header("3. TESTING SCRAPER")
    
    try:
        from scraper import AnnouncementScraper
        
        print("  → Creating scraper...")
        scraper = AnnouncementScraper()
        
        print("  → Testing BSE scraper (this might take 10-20 seconds)...")
        bse_data = scraper.scrape_bse()
        
        print(f"  ✅ Found {len(bse_data)} BSE announcements")
        
        if bse_data:
            print("\n  Sample announcement:")
            sample = bse_data[0]
            print(f"    Company: {sample.get('company', 'N/A')}")
            print(f"    Subject: {sample.get('subject', 'N/A')[:60]}...")
            print(f"    PDF: {sample.get('pdf_link', 'N/A')[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_analyzer():
    """Test Gemini analyzer"""
    print_header("4. TESTING GEMINI AI")
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("  ⚠️  GEMINI_API_KEY not set")
        print("     Set it with: export GEMINI_API_KEY='your-key-here'")
        print("     Get key from: https://aistudio.google.com/apikey")
        return False
    
    try:
        from analyzer import GeminiAnalyzer
        
        print("  → Creating analyzer...")
        analyzer = GeminiAnalyzer(api_key)
        
        print("  ✅ Gemini connection successful!")
        print("     Note: Not running full analysis to save API quota")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def test_database():
    """Test database"""
    print_header("5. TESTING DATABASE")
    
    try:
        from database import Database
        
        print("  → Creating database...")
        db = Database("test_db.db")
        
        print("  → Adding test announcement...")
        test_ann = {
            'exchange': 'TEST',
            'company': 'Test Company',
            'pdf_link': 'https://example.com/test.pdf',
            'ai_headline': 'Test Headline',
            'ai_summary': 'This is a test',
            'ai_importance': 8
        }
        
        db.add_announcement(test_ann)
        
        print("  → Retrieving announcements...")
        results = db.get_recent_announcements(limit=1)
        
        print("  → Getting stats...")
        stats = db.get_stats()
        
        print(f"  ✅ Database working! Total: {stats['total']} announcements")
        
        db.close()
        
        # Clean up test database
        os.remove("test_db.db")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    
    print("\n" + "🦁 "*15)
    print("  LION SIGNAL HQ - QUICK TEST")
    print("🦁 "*15 + "\n")
    
    results = []
    
    results.append(("Files", test_files()))
    results.append(("Packages", test_imports()))
    results.append(("Scraper", test_scraper()))
    results.append(("Gemini AI", test_analyzer()))
    results.append(("Database", test_database()))
    
    # Summary
    print_header("SUMMARY")
    
    for test_name, success in results:
        print(f"  {check_mark(success)} {test_name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED! You're ready to deploy!")
        print("\nNext steps:")
        print("  1. Push code to GitHub")
        print("  2. Add GEMINI_API_KEY to GitHub Secrets")
        print("  3. Enable GitHub Actions")
        print("  4. Watch it run!")
    else:
        print("\n⚠️  Some tests failed. Fix the issues above before deploying.")
    
    print("\n" + "🦁 "*15 + "\n")

if __name__ == "__main__":
    main()
