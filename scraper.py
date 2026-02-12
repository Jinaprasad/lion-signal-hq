"""
🦁 LION SIGNAL HQ - Web Scraper
================================
This robot visits BSE and NSE websites every 30 minutes.
It finds new announcements and gets their PDF links.

Think of it as a SCOUT that goes to the websites and brings back treasure maps (PDF links).
"""

import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
from config import *

class AnnouncementScraper:
    """
    The Scout Robot that finds announcements
    """
    
    def __init__(self):
        """Set up the robot"""
        # Make the robot look like a real browser (so websites don't block it)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        
        # For NSE, we need to visit homepage first to get cookies
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_bse(self):
        """
        Visit BSE website and get announcements
        
        Returns: List of announcements with PDF links
        """
        print("🔍 Visiting BSE website...")
        
        announcements = []
        
        try:
            # Visit BSE announcements page
            response = requests.get(BSE_ANNOUNCEMENTS_URL, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ BSE website returned error: {response.status_code}")
                return announcements
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the table with announcements
            # (This is simplified - real implementation needs exact BSE HTML structure)
            rows = soup.find_all('tr')
            
            for row in rows[:100]:  # Get last 100 announcements
                try:
                    # Extract data from each row
                    cells = row.find_all('td')
                    
                    if len(cells) < 5:
                        continue
                    
                    # Find PDF link
                    pdf_link = None
                    for link in row.find_all('a', href=True):
                        if '.pdf' in link['href'].lower():
                            if link['href'].startswith('http'):
                                pdf_link = link['href']
                            else:
                                pdf_link = 'https://www.bseindia.com' + link['href']
                            break
                    
                    if not pdf_link:
                        continue
                    
                    # Get announcement details
                    company = cells[1].get_text(strip=True) if len(cells) > 1 else "Unknown"
                    subject = cells[2].get_text(strip=True) if len(cells) > 2 else "Unknown"
                    date_time = cells[3].get_text(strip=True) if len(cells) > 3 else datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    
                    announcement = {
                        'exchange': 'BSE',
                        'company': company,
                        'subject': subject,
                        'pdf_link': pdf_link,
                        'timestamp': date_time,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    announcements.append(announcement)
                    
                except Exception as e:
                    print(f"⚠️ Error parsing BSE row: {e}")
                    continue
            
            print(f"✅ Found {len(announcements)} announcements from BSE")
            
        except Exception as e:
            print(f"❌ Error scraping BSE: {e}")
        
        return announcements
    
    def scrape_nse(self, is_sme=False):
        """
        Visit NSE website and get announcements
        
        NSE is tricky - needs cookies from homepage first!
        
        Args:
            is_sme: True for SME announcements, False for Equity
        
        Returns: List of announcements with PDF links
        """
        
        source = "NSE-SME" if is_sme else "NSE"
        print(f"🔍 Visiting {source} website...")
        
        announcements = []
        
        try:
            # STEP 1: Visit NSE homepage to get cookies
            print("  → Getting cookies from NSE homepage...")
            homepage = self.session.get('https://www.nseindia.com', headers=self.headers, timeout=30)
            time.sleep(2)  # Wait a bit
            
            # STEP 2: Now visit announcements page
            url = NSE_SME_URL if is_sme else NSE_EQUITY_URL
            print(f"  → Visiting announcements page...")
            
            response = self.session.get(url, headers=self.headers, timeout=30)
            
            if response.status_code != 200:
                print(f"❌ {source} returned error: {response.status_code}")
                return announcements
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find announcement rows
            rows = soup.find_all('tr')
            
            for row in rows[:100]:  # Get last 100
                try:
                    cells = row.find_all('td')
                    
                    if len(cells) < 4:
                        continue
                    
                    # Find PDF link
                    pdf_link = None
                    for link in row.find_all('a', href=True):
                        href = link['href']
                        if '.pdf' in href.lower():
                            if href.startswith('http'):
                                pdf_link = href
                            elif href.startswith('/'):
                                pdf_link = 'https://www.nseindia.com' + href
                            else:
                                # NSE archives at nsearchives.nseindia.com
                                if 'nsearchives' not in href:
                                    pdf_link = 'https://nsearchives.nseindia.com/corporate/' + href
                                else:
                                    pdf_link = href
                            break
                    
                    if not pdf_link:
                        continue
                    
                    # Get details
                    symbol = cells[0].get_text(strip=True) if len(cells) > 0 else "Unknown"
                    company = cells[1].get_text(strip=True) if len(cells) > 1 else "Unknown"
                    subject = cells[2].get_text(strip=True) if len(cells) > 2 else "Unknown"
                    date_time = cells[3].get_text(strip=True) if len(cells) > 3 else datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    
                    announcement = {
                        'exchange': source,
                        'company': company,
                        'symbol': symbol,
                        'subject': subject,
                        'pdf_link': pdf_link,
                        'timestamp': date_time,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    announcements.append(announcement)
                    
                except Exception as e:
                    print(f"⚠️ Error parsing {source} row: {e}")
                    continue
            
            print(f"✅ Found {len(announcements)} announcements from {source}")
            
        except Exception as e:
            print(f"❌ Error scraping {source}: {e}")
        
        return announcements
    
    def scrape_all(self):
        """
        Visit ALL sources and get all announcements
        
        Returns: Combined list from BSE, NSE Equity, NSE SME
        """
        print("\n" + "="*50)
        print("🦁 LION SCOUT STARTING...")
        print("="*50 + "\n")
        
        all_announcements = []
        
        # Scrape BSE
        if SHOW_BSE:
            bse_data = self.scrape_bse()
            all_announcements.extend(bse_data)
            time.sleep(3)  # Be nice, wait between requests
        
        # Scrape NSE Equity
        if SHOW_NSE:
            nse_data = self.scrape_nse(is_sme=False)
            all_announcements.extend(nse_data)
            time.sleep(3)
        
        # Scrape NSE SME
        if SHOW_NSE_SME:
            nse_sme_data = self.scrape_nse(is_sme=True)
            all_announcements.extend(nse_sme_data)
        
        print(f"\n✅ TOTAL FOUND: {len(all_announcements)} new announcements")
        print("="*50 + "\n")
        
        return all_announcements


# Simple test if you run this file directly
if __name__ == "__main__":
    print("Testing the scraper...")
    
    scraper = AnnouncementScraper()
    results = scraper.scrape_all()
    
    print(f"\nGot {len(results)} announcements!")
    
    if results:
        print("\nFirst announcement:")
        print(results[0])
