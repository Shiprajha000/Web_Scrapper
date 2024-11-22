import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_indeed_jobs(query="Python developer", location="Bengaluru, Karnataka"):
    # Use the correct Indeed search URL with query and location
    base_url = "https://in.indeed.com/"
    params = {'q': query, 'l': location}
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
     
    # Send the GET request to the Indeed page
    response = requests.get(base_url, params=params, headers=headers)
    
    # Ensure the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    job_listings = []
    
    # Inspect the structure of the page to find the correct tags/classes for job data
    for job_card in soup.find_all('a', class_='result'):
        job_title = job_card.find('h2', class_='jobTitle')
        job_title = job_title.get_text(strip=True) if job_title else "No title"
        
        company = job_card.find('span', class_='companyName')
        company = company.get_text(strip=True) if company else "Not listed"
        
        location = job_card.find('div', class_='companyLocation')
        location = location.get_text(strip=True) if location else "Not listed"
        
        salary = job_card.find('span', class_='salary-snippet')
        salary = salary.get_text(strip=True) if salary else "Not listed"
        
        job_listings.append({
            'job_title': job_title,
            'company': company,
            'location': location,
            'salary': salary
        })
    
    return job_listings

def save_jobs_to_mongo(job_listings):
    if not job_listings:
        print("No job listings found.")
        return

    client = MongoClient('mongodb://localhost:27017/')
    db = client['job_data']
    collection = db['python_jobs']
    collection.insert_many(job_listings)
    print(f"{len(job_listings)} jobs saved to MongoDB.")

if __name__ == "__main__":
    jobs = get_indeed_jobs()
    
    # Check if jobs were scraped
    print(f"Found {len(jobs)} job listings.")
    
    # If jobs are found, save them to MongoDB
    if jobs:
        save_jobs_to_mongo(jobs)
