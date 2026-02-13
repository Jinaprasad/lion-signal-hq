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
            'Referer': 'https://www.nseindia.com/'
        }

    def init_nse_session(self):
        """Initializes cookies for NSE to avoid 401/403 errors"""
        try:
            self.session.get("https://www.nseindia.com", headers=self.headers, timeout=10)
            time.sleep(2)
        except Exception as e:
            print(f"Session Init Warning: {e}")

    def scrape_nse(self, is_sme=False):
        """Fetches NSE Equity or SME announcements via direct API"""
        self.init_nse_session()
        index_type = 'sme' if is_sme else 'equities'
        url = f"https://www.nseindia.com/api/corporate-announcements?index={index_type}"
        
        try:
            response = self.session.get(url, headers=self.headers, timeout=15)
            if response.status_code != 200:
                return []
            
            data = response.json()
            announcements = []
            for item in data:
                file_id = item.get('attachment', '')
                if file_id:
                    # Constructs the real download link shown in your screenshot
                    link = f"https://nsearchives.nseindia.com/corporate/{file_id}"
                    announcements.append({
                        'exchange': 'NSE-SME' if is_sme else 'NSE',
                        'company': item.get('symbol', 'Unknown'),
                        'subject': item.get('desc', 'No Subject'),
                        'pdf_link': link,
                        'timestamp': item.get('attime', '')
                    })
            return announcements
        except Exception as e:
            print(f"NSE API Error: {e}")
            return []

    def scrape_bse(self):
        """Fetches BSE announcements using direct API to bypass 'No Records' screen"""
        api_url = "https://api.bseindia.com/BseOnlineGui/api/AnnSubCategory/getAnnData"
        today = datetime.now().strftime('%Y%m%d')
        
        params = {
            'strType': 'C',
            'strSDate': today,
            'strEDate': today,
            'strCat': '-1',
            'strPrevDate': today,
            'strScrip': '',
            'strSearch': 'P'
        }
        
        headers = self.headers.copy()
        headers['Referer'] = "https://www.bseindia.com/corporates/ann.html"
        
        try:
            r = self.session.get(api_url, headers=headers, params=params, timeout=15)
            if r.status_code != 200:
                return []
            
            data = r.json()
            return [{
                'exchange': 'BSE',
                'company': i.get('SLONGNAME', 'Unknown'),
                'subject': i.get('NEWSSUB', 'No Subject'),
                'pdf_link': f"https://www.bseindia.com/xml-data/corpfiling/AttachLive/{i.get('ATTACHMENTNAME')}",
                'timestamp': i.get('NEWS_DT', '')
            } for i in data if i.get('ATTACHMENTNAME')]
        except Exception as e:
            print(f"BSE API Error: {e}")
            return []

    def scrape_all(self):
        """Combines all sources into a single feed"""
        all_data = []
        all_data.extend(self.scrape_nse(is_sme=False))
        all_data.extend(self.scrape_nse(is_sme=True))
        all_data.extend(self.scrape_bse())
        return all_data
