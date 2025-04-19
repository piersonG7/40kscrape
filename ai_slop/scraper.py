import json
import time
from typing import Dict, List, Any
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus

class ArmyListScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        # Set headers to mimic a browser request
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page_content(self, url: str) -> str:
        """Fetch the page content using requests."""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return ""
            
    def parse_table(self, html_content: str, detachment: str) -> List[Dict[str, Any]]:
        """Parse the HTML content and extract data from the table."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the main table - you might need to adjust this selector based on the actual HTML structure
        table = soup.find('table', {'class': 'table'})  # Adjust class name if needed
        if not table:
            print("No table found in the HTML content")
            return []
            
        # Find all rows
        rows = table.find_all('tr')
        if not rows:
            print("No rows found in the table")
            return []
            
        # Extract headers
        headers = []
        header_row = rows[0]
        for th in header_row.find_all(['th', 'td']):
            headers.append(th.text.strip())
            
        data = []
        for row in rows[1:]:  # Skip header row
            cells = row.find_all('td')
            if len(cells) != len(headers):
                continue  # Skip malformed rows
                
            row_data = {'Detachment': detachment}  # Add detachment info to each row
            for header, cell in zip(headers, cells):
                # Clean the cell text
                cell_text = cell.text.strip()
                # Remove any extra whitespace
                cell_text = ' '.join(cell_text.split())
                row_data[header] = cell_text
                
            data.append(row_data)
            
        return data
        
    def save_to_json(self, data: List[Dict[str, Any]], filename: str = 'army_lists.json'):
        """Save the scraped data to a JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
    def scrape(self):
        """Main scraping method."""
        # List of Space Marine detachments
        detachments = [
            "1st Company Task Force",
            "2nd Company Task Force",
            "3rd Company Task Force",
            "4th Company Task Force",
            "5th Company Task Force",
            "6th Company Task Force",
            "7th Company Task Force",
            "8th Company Task Force",
            "9th Company Task Force",
            "10th Company Task Force",
            "Black Templars Sword Brethren",
            "Blood Angels Sons of Sanguinius",
            "Dark Angels Unforgiven Task Force",
            "Space Wolves Champions of Fenris",
            "White Scars Stormlance Task Force"
        ]
        
        print(f"Found {len(detachments)} Space Marine detachments to scrape")
        all_data = []
        
        for detachment in detachments:
            print(f"\nScraping data for {detachment}...")
            url = f"{self.base_url}&detachment={quote_plus(detachment)}"
            html_content = self.get_page_content(url)
            
            if html_content:
                data = self.parse_table(html_content, detachment)
                all_data.extend(data)
                print(f"Found {len(data)} entries for {detachment}")
                time.sleep(1)  # Be nice to the server
            else:
                print(f"Failed to fetch data for {detachment}")
                
        if all_data:
            self.save_to_json(all_data)
            print(f"\nSuccessfully scraped {len(all_data)} total entries")
        else:
            print("No data was scraped")

if __name__ == "__main__":
    base_url = "https://armylists.rmz.gs/?losses=all&faction=Space+Marines&rounds=4&offset=0&player_count=0"
    scraper = ArmyListScraper(base_url)
    scraper.scrape() 