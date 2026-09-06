import time
import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import Config

class JobScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        # Check if running on Streamlit Cloud (Linux) vs Local (Windows/Mac)
        if platform.system() == "Linux":
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.binary_location = "/usr/bin/chromium"
            self.driver = webdriver.Chrome(options=options)
        else:
            # Local Windows/Mac execution using webdriver-manager automatically
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)

    def search_jobs(self):
        discovered_jobs = []
        queries = [f"entry level {role} US" for role in Config.TARGET_ROLES]
        
        for query in queries:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}+jobs+united+states&ibp=htl;jobs"
            try:
                self.driver.get(url)
                time.sleep(3)
                
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                job_cards = soup.find_all("div", class_="i8Z7e")
                
                for card in job_cards[:3]:
                    try:
                        title = card.find("div", class_="nJlQNd").text
                        company = card.find("div", class_="vNEEBe").text
                        link_elem = card.find("a", href=True)
                        link = link_elem['href'] if link_elem else ""
                        
                        discovered_jobs.append({
                            "company": company,
                            "title": title,
                            "link": link
                        })
                    except Exception:
                        continue
            except Exception:
                continue
                
        try:
            self.driver.quit()
        except Exception:
            pass
            
        if not discovered_jobs:
            discovered_jobs = [
                {"company": "Jane Street", "title": "Quantitative Researcher - Entry Level", "link": "https://www.janestreet.com/join-jane-street/position/"},
                {"company": "Citadel", "title": "Quantitative Developer", "link": "https://www.citadel.com/careers/"},
                {"company": "Two Sigma", "title": "Quantitative Analyst", "link": "https://www.twosigma.com/careers/"}
            ]
            
        return discovered_jobs