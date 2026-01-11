"""Job Scraping Module - Handles multi-source job scraping"""

import requests
from bs4 import BeautifulSoup
import time


def extract_skills_from_title(title):
    """Extract skills from job title"""
    title_low = title.lower()
    skill_map = {
        'python': ['python'], 'java': ['java'], 'javascript': ['javascript', 'js'], 
        'react': ['react', 'reactjs'], 'node': ['node', 'node.js', 'nodejs'], 
        'aws': ['aws', 'amazon web services'], 'azure': ['azure'],
        'docker': ['docker'], 'kubernetes': ['kubernetes', 'k8s'], 
        'sql': ['sql', 'mysql', 'postgresql'], 'machine learning': ['machine learning', 'ml'], 
        'data science': ['data science', 'data scientist'], 'devops': ['devops'], 
        'frontend': ['frontend', 'front-end', 'front end'],
        'backend': ['backend', 'back-end', 'back end'], 
        'full stack': ['full stack', 'fullstack', 'full-stack'],
        'angular': ['angular'], 'vue': ['vue', 'vuejs'], 'django': ['django'], 
        'flask': ['flask'], 'api': ['api', 'rest', 'restful'], 'git': ['git', 'github'], 
        'typescript': ['typescript', 'ts'], 'mongodb': ['mongodb', 'mongo'], 
        'redis': ['redis'], 'ci/cd': ['ci/cd', 'cicd', 'jenkins'],
        'agile': ['agile', 'scrum'], 'testing': ['testing', 'test', 'qa'],
    }
    
    found = []
    for skill, kws in skill_map.items():
        if any(kw in title_low for kw in kws):
            found.append(skill)
    
    if not found:
        if 'engineer' in title_low or 'developer' in title_low:
            found = ['programming', 'software development', 'problem solving']
        elif 'data' in title_low:
            found = ['data analysis', 'sql', 'python']
        elif 'manager' in title_low:
            found = ['management', 'leadership', 'agile']
        else:
            found = ['communication', 'teamwork', 'problem solving']
    
    return found


def scrape_indeed(kw="software engineer", loc="", max_jobs=20):
    """Scrape jobs from Indeed"""
    jobs = []
    try:
        qry = kw.replace(' ', '+')
        loc_qry = loc.replace(' ', '+')
        url = f"https://www.indeed.com/jobs?q={qry}&l={loc_qry}"
        
        hdrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('div', class_='job_seen_beacon')[:max_jobs]
            
            for card in cards:
                try:
                    title_elem = card.find('h2', class_='jobTitle')
                    comp_elem = card.find('span', class_='companyName')
                    loc_elem = card.find('div', class_='companyLocation')
                    link_elem = card.find('a', class_='jcs-JobTitle')
                    
                    if title_elem and comp_elem:
                        title = title_elem.text.strip()
                        job = {
                            'title': title,
                            'company': comp_elem.text.strip(),
                            'location': loc_elem.text.strip() if loc_elem else 'Remote',
                            'link': f"https://www.indeed.com{link_elem['href']}" if link_elem else '',
                            'description': f"Looking for {title}",
                            'required_skills': extract_skills_from_title(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Indeed job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Indeed")
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
    
    return jobs


def scrape_remote_ok(kw="software", max_jobs=20):
    """Scrape jobs from RemoteOK"""
    jobs = []
    try:
        url = "https://remoteok.com/api"
        hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            listings = data[1:max_jobs+1] if len(data) > 1 else []
            
            for job_data in listings:
                try:
                    if isinstance(job_data, dict):
                        title = job_data.get('position', 'N/A')
                        comp = job_data.get('company', 'N/A')
                        loc = job_data.get('location', 'Remote')
                        tags = job_data.get('tags', [])
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': loc if loc else 'Remote',
                            'link': job_data.get('url', ''),
                            'description': job_data.get('description', f"{title} at {comp}")[:200],
                            'required_skills': [tag.lower() for tag in tags[:5]] if tags else extract_skills_from_title(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing RemoteOK job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from RemoteOK")
    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")
    
    return jobs


def scrape_naukri(kw="software engineer", loc="", max_jobs=20):
    """Scrape jobs from Naukri.com"""
    jobs = []
    try:
        qry = kw.replace(' ', '-')
        loc_qry = loc.replace(' ', '-') if loc else 'india'
        url = f"https://www.naukri.com/{qry}-jobs-in-{loc_qry}"
        
        hdrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('article', class_='jobTuple')[:max_jobs]
            
            for card in cards:
                try:
                    title_elem = card.find('a', class_='title')
                    comp_elem = card.find('a', class_='subTitle')
                    loc_elem = card.find('span', class_='location')
                    
                    if title_elem:
                        title = title_elem.text.strip()
                        comp = comp_elem.text.strip() if comp_elem else 'Company in India'
                        l = loc_elem.text.strip() if loc_elem else 'India'
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': l,
                            'link': f"https://www.naukri.com{title_elem['href']}" if title_elem.get('href') else 'https://www.naukri.com',
                            'description': f"{title} at {comp}",
                            'required_skills': extract_skills_from_title(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Naukri job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Naukri")
    except Exception as e:
        print(f"Error scraping Naukri: {e}")
    
    return jobs


def scrape_instahyre(kw="software", max_jobs=20):
    """Scrape jobs from Instahyre"""
    jobs = []
    try:
        url = f"https://www.instahyre.com/search-jobs/?q={kw.replace(' ', '+')}"
        hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('div', class_='opportunity-card')[:max_jobs]
            
            for card in cards:
                try:
                    title_elem = card.find('h3')
                    comp_elem = card.find('p', class_='company-name')
                    loc_elem = card.find('span', class_='location')
                    
                    if title_elem:
                        title = title_elem.text.strip()
                        comp = comp_elem.text.strip() if comp_elem else 'Indian Tech Company'
                        l = loc_elem.text.strip() if loc_elem else 'India'
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': l,
                            'link': 'https://www.instahyre.com',
                            'description': f"{title} at {comp}",
                            'required_skills': extract_skills_from_title(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Instahyre job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Instahyre")
    except Exception as e:
        print(f"Error scraping Instahyre: {e}")
    
    return jobs


def get_indian_fallback():
    """Get fallback jobs from Indian companies"""
    return [
        {'title': 'Python Developer', 'company': 'TCS', 'location': 'Bangalore, India', 'description': 'Python developer for enterprise', 'required_skills': ['python', 'django', 'sql', 'rest api', 'git'], 'link': 'https://www.tcs.com/careers'},
        {'title': 'Full Stack Developer', 'company': 'Infosys', 'location': 'Hyderabad, India', 'description': 'Full stack with React and Node.js', 'required_skills': ['javascript', 'react', 'node', 'mongodb', 'html', 'css'], 'link': 'https://www.infosys.com/careers'},
        {'title': 'Data Analyst', 'company': 'Wipro', 'location': 'Pune, India', 'description': 'Data analyst with Excel and SQL', 'required_skills': ['excel', 'sql', 'python', 'data analysis', 'tableau'], 'link': 'https://careers.wipro.com'},
        {'title': 'VBA Developer', 'company': 'Accenture India', 'location': 'Mumbai, India', 'description': 'VBA developer for Excel automation', 'required_skills': ['vba', 'excel', 'macros', 'sql', 'access'], 'link': 'https://www.accenture.com/in-en/careers'},
        {'title': 'Java Developer', 'company': 'HCL Technologies', 'location': 'Chennai, India', 'description': 'Java backend developer', 'required_skills': ['java', 'spring', 'sql', 'rest api', 'microservices'], 'link': 'https://www.hcltech.com/careers'},
        {'title': 'DevOps Engineer', 'company': 'Tech Mahindra', 'location': 'Bangalore, India', 'description': 'DevOps with AWS and Docker', 'required_skills': ['aws', 'docker', 'kubernetes', 'jenkins', 'linux'], 'link': 'https://www.techmahindra.com/careers'},
        {'title': 'React Developer', 'company': 'Cognizant', 'location': 'Noida, India', 'description': 'Frontend React developer', 'required_skills': ['react', 'javascript', 'html', 'css', 'typescript'], 'link': 'https://careers.cognizant.com'},
        {'title': 'Business Analyst', 'company': 'Capgemini India', 'location': 'Gurgaon, India', 'description': 'Business analyst with Excel and VBA', 'required_skills': ['excel', 'vba', 'sql', 'power bi', 'data analysis'], 'link': 'https://www.capgemini.com/in-en/careers'}
    ]


def get_fallback_jobs():
    """Get all fallback jobs"""
    ind_jobs = get_indian_fallback()
    intl_jobs = [
        {'title': 'Senior Python Developer', 'company': 'TechCorp Solutions', 'location': 'Remote', 'description': 'Experienced Python developer for scalable backend', 'required_skills': ['python', 'django', 'flask', 'api', 'sql', 'git', 'docker'], 'link': 'https://example.com/jobs/python-dev'},
        {'title': 'Data Scientist', 'company': 'DataTech Analytics', 'location': 'Remote', 'description': 'Data Scientist with ML and Python', 'required_skills': ['python', 'machine learning', 'data analysis', 'sql', 'pandas', 'numpy'], 'link': 'https://example.com/jobs/data-scientist'},
        {'title': 'DevOps Engineer', 'company': 'Cloud Infrastructure Co', 'location': 'Remote', 'description': 'DevOps with AWS and Kubernetes', 'required_skills': ['docker', 'kubernetes', 'aws', 'ci/cd', 'linux', 'git', 'python'], 'link': 'https://example.com/jobs/devops'},
        {'title': 'Frontend React Developer', 'company': 'UI/UX Studios', 'location': 'Remote', 'description': 'Frontend React developer', 'required_skills': ['react', 'javascript', 'html', 'css', 'typescript', 'git'], 'link': 'https://example.com/jobs/frontend'}
    ]
    return ind_jobs + intl_jobs


def scrape_jobs_multi(kw="software developer", loc="", max_jobs=20):
    """Scrape jobs from multiple sources"""
    all_jobs = []
    
    print("Trying Naukri.com...")
    naukri = scrape_naukri(kw, loc or "india", max_jobs=8)
    all_jobs.extend(naukri)
    
    print("Trying Instahyre...")
    insta = scrape_instahyre(kw, max_jobs=5)
    all_jobs.extend(insta)
    
    print("Trying RemoteOK...")
    remote = scrape_remote_ok(kw.split()[0], max_jobs=7)
    all_jobs.extend(remote)
    
    if len(all_jobs) < max_jobs:
        print("Trying Indeed...")
        indeed = scrape_indeed(kw, loc, max_jobs=5)
        all_jobs.extend(indeed)
    
    if len(all_jobs) < 10:
        print("Adding fallback jobs...")
        all_jobs.extend(get_fallback_jobs())
    
    # Remove duplicates
    seen = set()
    unique = []
    for job in all_jobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique.append(job)
    
    return unique[:max_jobs]
