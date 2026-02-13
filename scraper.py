import requests
import time
from datetime import datetime

class AnnouncementScraper:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
        }

    def init_nse_session(self):
        """Must visit home page first to get cookies or NSE blocks everything"""
        try:
            self.session.get("https://www.nseindia.com", headers=self.headers, timeout=10)
            time.sleep(1)
        except:
            pass

    def scrape_nse(self, is_sme=False):
        self.init_nse_session()
        # Direct API endpoint bypasses the 'button click' requirement
        url = "https://www.nseindia.com/api/corporate-announcements"
        params = {'index': 'sme' if is_sme else 'equities'}
        
        try:
            response = self.session.get(url, headers=self.headers, params=params, timeout=15)
            data = response.json()
            
            announcements = []
            for item in data:
                # We construct the direct link that bypasses JavaScript
                file_id = item.get('attachment', '')
                direct_link = f"https://nsearchives.nseindia.com/corporate/{file_id}" if file_id else ""
                
                announcements.append({
                    'exchange': 'NSE-SME' if is_sme else 'NSE',
                    'company': item.get('symbol', 'Unknown'),
                    'subject': item.get('desc', 'No Subject'),
                    'pdf_link': direct_link,
                    'timestamp': item.get('attime', '')
                })
            return announcements
        except Exception as e:
            print(f"NSE Error: {e}")
            return []

    def scrape_bse(self):
        # BSE API Method - Bypasses the 'Copy Link Address' requirement
        url = "https://api.bseindia.com/BseOnlineGui/api/AnnSubCategory/getAnnData"
        headers = self.headers.copy()
        headers['Referer'] = "https://www.bseindia.com/"
        
        params = {
            'strType': 'C',
            'strSDate': datetime.now().strftime('%Y%m%d'),
            'strEDate': datetime.now().strftime('%Y%m%d'),
            'strCat': '-1',
            'strPrevDate': datetime.now().strftime('%Y%m%d'),
            'strScrip': '',
            'strSearch': 'P'
        }
        
        try:
            r = requests.get(url, headers=headers, params=params, timeout=15)
            # BSE returns a list of dicts directly
            return [{
                'exchange': 'BSE',
                'company': item.get('SLONGNAME', ''),
                'subject': item.get('NEWSSUB', ''),
                'pdf_link': item.get('ATTACHMENTNAME', ''),
                'timestamp': item.get('NEWS_DT', '')
            } for item in r.json()]
        except:
            return []
