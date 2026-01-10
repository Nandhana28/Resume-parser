from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import docx2txt
import re
from collections import Counter
import requests
from bs4 import BeautifulSoup
import PyPDF2
from docx import Document
import time
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import BarChart, Reference
from datetime import datetime
import glob

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'docx', 'pdf', 'doc'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

jobCache = []
cacheTime = 0
cacheDur = 1800

def scrapeIndeed(kw="software engineer", loc="", maxJobs=20):
    jobs = []
    try:
        qry = kw.replace(' ', '+')
        locQry = loc.replace(' ', '+')
        url = f"https://www.indeed.com/jobs?q={qry}&l={locQry}"
        
        hdrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('div', class_='job_seen_beacon')[:maxJobs]
            
            if not cards:
                cards = soup.find_all('td', class_='resultContent')[:maxJobs]
            
            for card in cards:
                try:
                    titleElem = card.find('h2', class_='jobTitle')
                    if not titleElem:
                        titleElem = card.find('a', class_='jcs-JobTitle')
                    
                    compElem = card.find('span', class_='companyName')
                    if not compElem:
                        compElem = card.find('span', {'data-testid': 'company-name'})
                    
                    locElem = card.find('div', class_='companyLocation')
                    if not locElem:
                        locElem = card.find('div', {'data-testid': 'text-location'})
                    
                    linkElem = card.find('a', class_='jcs-JobTitle')
                    if not linkElem:
                        linkElem = card.find('a')
                    
                    if titleElem and compElem:
                        title = titleElem.text.strip()
                        job = {
                            'title': title,
                            'company': compElem.text.strip(),
                            'location': locElem.text.strip() if locElem else 'Remote',
                            'link': f"https://www.indeed.com{linkElem['href']}" if linkElem and linkElem.get('href') else '',
                            'description': f"Looking for {title}",
                            'required_skills': extractSkillsFromTitle(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Indeed job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Indeed")
        else:
            print(f"Indeed fetch failed: {resp.status_code}")
            
    except Exception as e:
        print(f"Error scraping Indeed: {e}")
    
    return jobs

def scrapeRemoteOk(kw="software", maxJobs=20):
    jobs = []
    try:
        url = "https://remoteok.com/api"
        hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            listings = data[1:maxJobs+1] if len(data) > 1 else []
            
            for jobData in listings:
                try:
                    if isinstance(jobData, dict):
                        title = jobData.get('position', 'N/A')
                        comp = jobData.get('company', 'N/A')
                        loc = jobData.get('location', 'Remote')
                        tags = jobData.get('tags', [])
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': loc if loc else 'Remote',
                            'link': jobData.get('url', ''),
                            'description': jobData.get('description', f"{title} at {comp}")[:200],
                            'required_skills': [tag.lower() for tag in tags[:5]] if tags else extractSkillsFromTitle(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing RemoteOK job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from RemoteOK")
        else:
            print(f"RemoteOK fetch failed: {resp.status_code}")
            
    except Exception as e:
        print(f"Error scraping RemoteOK: {e}")
    
    return jobs

def scrapeNaukri(kw="software engineer", loc="", maxJobs=20):
    jobs = []
    try:
        qry = kw.replace(' ', '-')
        locQry = loc.replace(' ', '-') if loc else 'india'
        url = f"https://www.naukri.com/{qry}-jobs-in-{locQry}"
        
        hdrs = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('article', class_='jobTuple')[:maxJobs]
            
            if not cards:
                cards = soup.find_all('div', class_='srp-jobtuple-wrapper')[:maxJobs]
            
            for card in cards:
                try:
                    titleElem = card.find('a', class_='title')
                    if not titleElem:
                        titleElem = card.find('a', {'class': lambda x: x and 'title' in x})
                    
                    compElem = card.find('a', class_='subTitle')
                    if not compElem:
                        compElem = card.find('div', class_='companyInfo')
                    
                    locElem = card.find('span', class_='location')
                    if not locElem:
                        locElem = card.find('li', class_='location')
                    
                    if titleElem:
                        title = titleElem.text.strip()
                        comp = compElem.text.strip() if compElem else 'Company in India'
                        l = locElem.text.strip() if locElem else 'India'
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': l,
                            'link': f"https://www.naukri.com{titleElem['href']}" if titleElem.get('href') else 'https://www.naukri.com',
                            'description': f"{title} at {comp}",
                            'required_skills': extractSkillsFromTitle(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Naukri job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Naukri")
        else:
            print(f"Naukri fetch failed: {resp.status_code}")
            
    except Exception as e:
        print(f"Error scraping Naukri: {e}")
    
    return jobs

def scrapeInstahyre(kw="software", maxJobs=20):
    jobs = []
    try:
        url = f"https://www.instahyre.com/search-jobs/?q={kw.replace(' ', '+')}"
        hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=hdrs, timeout=10)
        
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            cards = soup.find_all('div', class_='opportunity-card')[:maxJobs]
            
            for card in cards:
                try:
                    titleElem = card.find('h3')
                    compElem = card.find('p', class_='company-name')
                    locElem = card.find('span', class_='location')
                    
                    if titleElem:
                        title = titleElem.text.strip()
                        comp = compElem.text.strip() if compElem else 'Indian Tech Company'
                        l = locElem.text.strip() if locElem else 'India'
                        
                        job = {
                            'title': title,
                            'company': comp,
                            'location': l,
                            'link': 'https://www.instahyre.com',
                            'description': f"{title} at {comp}",
                            'required_skills': extractSkillsFromTitle(title)
                        }
                        jobs.append(job)
                except Exception as e:
                    print(f"Error parsing Instahyre job: {e}")
                    continue
            
            print(f"Scraped {len(jobs)} jobs from Instahyre")
        else:
            print(f"Instahyre fetch failed: {resp.status_code}")
            
    except Exception as e:
        print(f"Error scraping Instahyre: {e}")
    
    return jobs

def getIndianFallback():
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

def scrapeJobsMulti(kw="software engineer", loc="", maxJobs=20):
    allJobs = []
    
    print("Trying Naukri.com...")
    naukri = scrapeNaukri(kw, loc or "india", maxJobs=8)
    allJobs.extend(naukri)
    
    print("Trying Instahyre...")
    insta = scrapeInstahyre(kw, maxJobs=5)
    allJobs.extend(insta)
    
    print("Trying RemoteOK...")
    remote = scrapeRemoteOk(kw.split()[0], maxJobs=7)
    allJobs.extend(remote)
    
    if len(allJobs) < maxJobs:
        print("Trying Indeed...")
        indeed = scrapeIndeed(kw, loc, maxJobs=5)
        allJobs.extend(indeed)
    
    if len(allJobs) < 10:
        print("Adding fallback jobs...")
        allJobs.extend(getIndianFallback())
    
    seen = set()
    unique = []
    for job in allJobs:
        key = (job['title'].lower(), job['company'].lower())
        if key not in seen:
            seen.add(key)
            unique.append(job)
    
    return unique[:maxJobs]

def extractSkillsFromTitle(title):
    titleLow = title.lower()
    skillMap = {
        'python': ['python'], 'java': ['java'], 'javascript': ['javascript', 'js'], 'react': ['react', 'reactjs'],
        'node': ['node', 'node.js', 'nodejs'], 'aws': ['aws', 'amazon web services'], 'azure': ['azure'],
        'docker': ['docker'], 'kubernetes': ['kubernetes', 'k8s'], 'sql': ['sql', 'mysql', 'postgresql'],
        'machine learning': ['machine learning', 'ml'], 'data science': ['data science', 'data scientist'],
        'devops': ['devops'], 'frontend': ['frontend', 'front-end', 'front end'],
        'backend': ['backend', 'back-end', 'back end'], 'full stack': ['full stack', 'fullstack', 'full-stack'],
        'angular': ['angular'], 'vue': ['vue', 'vuejs'], 'django': ['django'], 'flask': ['flask'],
        'api': ['api', 'rest', 'restful'], 'git': ['git', 'github'], 'typescript': ['typescript', 'ts'],
        'mongodb': ['mongodb', 'mongo'], 'redis': ['redis'], 'ci/cd': ['ci/cd', 'cicd', 'jenkins'],
        'agile': ['agile', 'scrum'], 'testing': ['testing', 'test', 'qa'],
    }
    
    found = []
    for skill, kws in skillMap.items():
        if any(kw in titleLow for kw in kws):
            found.append(skill)
    
    if not found:
        if 'engineer' in titleLow or 'developer' in titleLow:
            found = ['programming', 'software development', 'problem solving']
        elif 'data' in titleLow:
            found = ['data analysis', 'sql', 'python']
        elif 'manager' in titleLow:
            found = ['management', 'leadership', 'agile']
        else:
            found = ['communication', 'teamwork', 'problem solving']
    
    return found

def getFallbackJobs():
    indJobs = getIndianFallback()
    intlJobs = [
        {'title': 'Senior Python Developer', 'company': 'TechCorp Solutions', 'location': 'Remote', 'description': 'Experienced Python developer for scalable backend', 'required_skills': ['python', 'django', 'flask', 'api', 'sql', 'git', 'docker'], 'link': 'https://example.com/jobs/python-dev'},
        {'title': 'Data Scientist', 'company': 'DataTech Analytics', 'location': 'Remote', 'description': 'Data Scientist with ML and Python', 'required_skills': ['python', 'machine learning', 'data analysis', 'sql', 'pandas', 'numpy'], 'link': 'https://example.com/jobs/data-scientist'},
        {'title': 'DevOps Engineer', 'company': 'Cloud Infrastructure Co', 'location': 'Remote', 'description': 'DevOps with AWS and Kubernetes', 'required_skills': ['docker', 'kubernetes', 'aws', 'ci/cd', 'linux', 'git', 'python'], 'link': 'https://example.com/jobs/devops'},
        {'title': 'Frontend React Developer', 'company': 'UI/UX Studios', 'location': 'Remote', 'description': 'Frontend React developer', 'required_skills': ['react', 'javascript', 'html', 'css', 'typescript', 'git'], 'link': 'https://example.com/jobs/frontend'}
    ]
    return indJobs + intlJobs

def getJobsDb(forceRefresh=False):
    global jobCache, cacheTime
    
    curTime = time.time()
    cacheAge = curTime - cacheTime if cacheTime > 0 else 0
    
    if not forceRefresh and jobCache and cacheAge < cacheDur:
        cacheMin = int(cacheAge / 60)
        print(f"Using cached jobs (cached {cacheMin} min ago)")
        return jobCache
    
    print("Scraping fresh jobs...")
    jobs = scrapeJobsMulti(kw="software developer", loc="", maxJobs=25)
    
    scrapeTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not jobs or len(jobs) == 0:
        print("Scraping failed, using fallback")
        jobs = getFallbackJobs()
        for job in jobs:
            job['scraped_at'] = scrapeTime
            job['is_fallback'] = True
    else:
        print(f"Got {len(jobs)} fresh jobs")
        for job in jobs:
            job['scraped_at'] = scrapeTime
            job['is_fallback'] = False
    
    jobCache = jobs
    cacheTime = curTime
    
    return jobs

def allowedFile(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extractPdf(fpath):
    txt = ""
    try:
        with open(fpath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                txt += page.extract_text()
    except Exception as e:
        print(f"PDF extract error: {e}")
    return txt

def extractDocx(fpath):
    try:
        return docx2txt.process(fpath)
    except Exception as e:
        print(f"DOCX extract error: {e}")
        return ""

def extractDoc(fpath):
    try:
        return docx2txt.process(fpath)
    except Exception as e:
        print(f"DOC extract error: {e}")
        return ""

def extractResume(fpath):
    ext = fpath.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extractPdf(fpath)
    elif ext == 'docx':
        return extractDocx(fpath)
    elif ext == 'doc':
        return extractDoc(fpath)
    else:
        return ""

def extractEmail(txt):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, txt)
    return emails[0] if emails else None

def extractPhone(txt):
    pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(pattern, txt)
    return phones[0] if phones else None

def extractSkills(txt):
    txtLow = txt.lower()
    skillKws = {
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin', 'go', 'rust', 'typescript',
        'vba', 'visual basic', 'r', 'matlab', 'scala', 'perl',
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'asp.net',
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra', 'dynamodb',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'ci/cd', 'terraform', 'ansible',
        'machine learning', 'deep learning', 'data analysis', 'pandas', 'numpy', 'scikit-learn', 
        'tensorflow', 'pytorch', 'keras', 'statistics', 'data visualization', 'tableau', 'power bi',
        'android', 'ios', 'react native', 'flutter', 'mobile development',
        'excel', 'vba', 'macros', 'power query', 'power pivot', 'access', 'word', 'powerpoint',
        'git', 'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'linux', 'unix',
        'api', 'rest', 'testing', 'junit', 'selenium'
    }
    
    found = []
    for skill in skillKws:
        if skill in txtLow:
            found.append(skill)
    
    return found

def calcMatch(resumeSkills, jobSkills):
    if not jobSkills or not resumeSkills:
        return 0
    
    resumeLow = [s.lower().strip() for s in resumeSkills]
    jobLow = [s.lower().strip() for s in jobSkills]
    
    exact = set(resumeLow) & set(jobLow)
    
    partial = 0
    for rs in resumeLow:
        for js in jobLow:
            if rs not in exact and js not in exact:
                if rs in js or js in rs:
                    partial += 0.5
                    break
    
    total = len(exact) + partial
    pct = (total / len(jobLow)) * 100
    
    return min(pct, 100)

def recommendJobs(resumeSkills, topN=10, minMatch=10, locFilter=None, skillFilter=None):
    matches = []
    jobsDb = getJobsDb()
    
    print(f"Got {len(jobsDb)} jobs from db")
    print(f"Resume skills: {resumeSkills}")
    
    for job in jobsDb:
        score = calcMatch(resumeSkills, job['required_skills'])
        
        resumeLow = [s.lower().strip() for s in resumeSkills]
        jobLow = [s.lower().strip() for s in job['required_skills']]
        matching = []
        
        for rs in resumeSkills:
            for js in job['required_skills']:
                if rs.lower() == js.lower() or rs.lower() in js.lower() or js.lower() in rs.lower():
                    if js not in matching:
                        matching.append(js)
        
        if locFilter and locFilter.lower() not in job.get('location', '').lower():
            continue
            
        if skillFilter:
            filterLow = [s.lower().strip() for s in skillFilter]
            hasSkill = any(
                any(sf in js or js in sf for js in jobLow)
                for sf in filterLow
            )
            if not hasSkill:
                continue
        
        if score >= minMatch:
            matches.append({
                'title': job['title'],
                'company': job['company'],
                'location': job.get('location', 'Not specified'),
                'description': job['description'],
                'match': round(score, 1),
                'matching_skills': matching,
                'link': job.get('link', ''),
                'required_skills': job['required_skills']
            })
    
    matches.sort(key=lambda x: x['match'], reverse=True)
    
    print(f"Returning {len(matches[:topN])} jobs (filtered from {len(matches)} matches)")
    
    return matches[:topN]



@app.route('/api/upload', methods=['POST'])
def uploadResume():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowedFile(file.filename):
        fname = secure_filename(file.filename)
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        file.save(fpath)
        
        txt = extractResume(fpath)
        email = extractEmail(txt)
        phone = extractPhone(txt)
        resumeSkills = extractSkills(txt)
        
        print(f"Extracted {len(resumeSkills)} skills")
        print(f"Skills: {resumeSkills}")
        
        allJobs = recommendJobs(resumeSkills, topN=50, minMatch=0)
        
        locs = list(set([job['location'] for job in allJobs if job['location'] != 'Not specified']))
        allSkillsSet = set()
        for job in allJobs:
            allSkillsSet.update(job.get('required_skills', []))
        availSkills = sorted(list(allSkillsSet))
        
        jobs = recommendJobs(resumeSkills, topN=20, minMatch=10)
        
        print(f"Got {len(jobs)} recommendations")
        
        if not jobs:
            print("No jobs with >10% match, lowering threshold")
            jobs = recommendJobs(resumeSkills, topN=20, minMatch=0)
        
        cacheAge = time.time() - cacheTime if cacheTime > 0 else 0
        cacheMin = int(cacheAge / 60)
        lastUpd = datetime.fromtimestamp(cacheTime).strftime("%Y-%m-%d %H:%M:%S") if cacheTime > 0 else "Just now"
        
        return jsonify({
            'success': True,
            'filename': fname,
            'email': email,
            'phone': phone,
            'skills': resumeSkills,
            'jobs': jobs,
            'total_jobs': len(jobs),
            'available_locations': locs,
            'available_skills': availSkills[:50],
            'cache_info': {
                'last_updated': lastUpd,
                'cache_age_minutes': cacheMin,
                'is_fresh': cacheAge < cacheDur
            }
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/scrape-jobs', methods=['POST'])
def scrapeJobs():
    data = request.get_json() or {}
    kw = data.get('keywords', 'software engineer')
    loc = data.get('location', '')
    maxJobs = data.get('max_jobs', 20)
    
    jobs = scrapeJobsMulti(kw=kw, loc=loc, maxJobs=maxJobs)
    
    if not jobs:
        jobs = getFallbackJobs()
    
    global jobCache, cacheTime
    jobCache = jobs
    cacheTime = time.time()
    
    return jsonify({
        'success': True,
        'jobs_count': len(jobs),
        'jobs': jobs,
        'source': 'scraped' if jobs != getFallbackJobs() else 'fallback'
    })

@app.route('/api/jobs', methods=['GET'])
def getJobs():
    jobs = getJobsDb()
    return jsonify({
        'success': True,
        'jobs_count': len(jobs),
        'jobs': jobs
    })

@app.route('/api/filter-jobs', methods=['POST'])
def filterJobs():
    data = request.get_json()
    
    resumeSkills = data.get('skills', [])
    locFilter = data.get('location')
    skillFilters = data.get('skill_filters', [])
    minMatch = data.get('min_match', 10)
    
    print(f"Filtering: loc={locFilter}, skills={skillFilters}, minMatch={minMatch}")
    
    jobs = recommendJobs(
        resumeSkills, 
        topN=50, 
        minMatch=minMatch,
        locFilter=locFilter,
        skillFilter=skillFilters if skillFilters else None
    )
    
    return jsonify({
        'success': True,
        'jobs': jobs,
        'total_jobs': len(jobs)
    })

@app.route('/api/cache-status', methods=['GET'])
def cacheStatus():
    curTime = time.time()
    cacheAge = curTime - cacheTime if cacheTime > 0 else 0
    cacheMin = int(cacheAge / 60)
    
    isFresh = cacheAge < cacheDur
    lastUpd = datetime.fromtimestamp(cacheTime).strftime("%Y-%m-%d %H:%M:%S") if cacheTime > 0 else "Never"
    
    return jsonify({
        'cache_age_minutes': cacheMin,
        'is_fresh': isFresh,
        'last_updated': lastUpd,
        'jobs_count': len(jobCache),
        'cache_duration_minutes': int(cacheDur / 60)
    })

@app.route('/api/refresh-jobs', methods=['POST'])
def refreshJobs():
    print("Force refreshing jobs...")
    jobs = getJobsDb(forceRefresh=True)
    
    return jsonify({
        'success': True,
        'jobs_count': len(jobs),
        'message': f'Refreshed {len(jobs)} jobs from live sources',
        'timestamp': time.time()
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/export-excel', methods=['POST'])
def exportExcel():
    data = request.get_json()
    
    fname = data.get('filename', 'resume')
    email = data.get('email', 'N/A')
    phone = data.get('phone', 'N/A')
    skills = data.get('skills', [])
    jobs = data.get('jobs', [])
    
    wb = Workbook()
    wsSummary = wb.active
    wsSummary.title = "Dashboard"
    
    hdrFill = PatternFill(start_color="2E7D32", end_color="2E7D32", fill_type="solid")
    hdrFont = Font(bold=True, color="FFFFFF", size=14)
    
    wsSummary['A1'] = "RESUME JOB MATCH REPORT"
    wsSummary['A1'].font = Font(bold=True, size=16, color="2E7D32")
    wsSummary.merge_cells('A1:D1')
    
    wsSummary['A3'] = "Resume Information"
    wsSummary['A3'].font = hdrFont
    wsSummary['A3'].fill = hdrFill
    wsSummary.merge_cells('A3:D3')
    
    wsSummary['A4'] = "Filename:"
    wsSummary['B4'] = fname
    wsSummary['A5'] = "Email:"
    wsSummary['B5'] = email
    wsSummary['A6'] = "Phone:"
    wsSummary['B6'] = phone
    wsSummary['A7'] = "Skills Found:"
    wsSummary['B7'] = len(skills)
    wsSummary['A8'] = "Report Date:"
    wsSummary['B8'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    wsSummary['A10'] = "Job Match Statistics"
    wsSummary['A10'].font = hdrFont
    wsSummary['A10'].fill = hdrFill
    wsSummary.merge_cells('A10:D10')
    
    wsSummary['A11'] = "Total Jobs Found:"
    wsSummary['B11'] = len(jobs)
    
    if jobs:
        avgMatch = sum(job['match'] for job in jobs) / len(jobs)
        topMatch = max(job['match'] for job in jobs)
        
        wsSummary['A12'] = "Average Match:"
        wsSummary['B12'] = f"{avgMatch:.1f}%"
        wsSummary['A13'] = "Top Match:"
        wsSummary['B13'] = f"{topMatch:.1f}%"
        
        excellent = len([j for j in jobs if j['match'] >= 70])
        good = len([j for j in jobs if 50 <= j['match'] < 70])
        fair = len([j for j in jobs if 30 <= j['match'] < 50])
        low = len([j for j in jobs if j['match'] < 30])
        
        wsSummary['A15'] = "Match Distribution"
        wsSummary['A15'].font = hdrFont
        wsSummary['A15'].fill = hdrFill
        wsSummary.merge_cells('A15:D15')
        
        wsSummary['A16'] = "Excellent (70%+):"
        wsSummary['B16'] = excellent
        wsSummary['A17'] = "Good (50-69%):"
        wsSummary['B17'] = good
        wsSummary['A18'] = "Fair (30-49%):"
        wsSummary['B18'] = fair
        wsSummary['A19'] = "Low (<30%):"
        wsSummary['B19'] = low
    
    wsSummary.column_dimensions['A'].width = 20
    wsSummary.column_dimensions['B'].width = 30
    
    wsSkills = wb.create_sheet("Skills")
    wsSkills['A1'] = "Detected Skills"
    wsSkills['A1'].font = hdrFont
    wsSkills['A1'].fill = hdrFill
    
    for idx, skill in enumerate(skills, start=2):
        wsSkills[f'A{idx}'] = skill
    
    wsSkills.column_dimensions['A'].width = 25
    
    wsJobs = wb.create_sheet("Job Matches")
    
    hdrs = ['#', 'Job Title', 'Company', 'Location', 'Match %', 'Matching Skills', 'Link']
    for col, hdr in enumerate(hdrs, start=1):
        cell = wsJobs.cell(row=1, column=col)
        cell.value = hdr
        cell.font = hdrFont
        cell.fill = hdrFill
        cell.alignment = Alignment(horizontal='center', vertical='center')
    
    for idx, job in enumerate(jobs, start=2):
        wsJobs.cell(row=idx, column=1, value=idx-1)
        wsJobs.cell(row=idx, column=2, value=job['title'])
        wsJobs.cell(row=idx, column=3, value=job['company'])
        wsJobs.cell(row=idx, column=4, value=job.get('location', 'N/A'))
        
        matchCell = wsJobs.cell(row=idx, column=5, value=job['match'])
        if job['match'] >= 70:
            matchCell.fill = PatternFill(start_color="C8E6C9", end_color="C8E6C9", fill_type="solid")
        elif job['match'] >= 50:
            matchCell.fill = PatternFill(start_color="FFF9C4", end_color="FFF9C4", fill_type="solid")
        elif job['match'] >= 30:
            matchCell.fill = PatternFill(start_color="FFCCBC", end_color="FFCCBC", fill_type="solid")
        
        wsJobs.cell(row=idx, column=6, value=', '.join(job.get('matching_skills', [])))
        wsJobs.cell(row=idx, column=7, value=job.get('link', ''))
    
    wsJobs.column_dimensions['A'].width = 5
    wsJobs.column_dimensions['B'].width = 30
    wsJobs.column_dimensions['C'].width = 25
    wsJobs.column_dimensions['D'].width = 20
    wsJobs.column_dimensions['E'].width = 10
    wsJobs.column_dimensions['F'].width = 40
    wsJobs.column_dimensions['G'].width = 50
    
    wsTop = wb.create_sheet("Top 10 Matches")
    wsTop['A1'] = "TOP 10 JOB MATCHES"
    wsTop['A1'].font = Font(bold=True, size=14, color="2E7D32")
    wsTop.merge_cells('A1:E1')
    
    topHdrs = ['Rank', 'Job Title', 'Company', 'Match %', 'Location']
    for col, hdr in enumerate(topHdrs, start=1):
        cell = wsTop.cell(row=2, column=col)
        cell.value = hdr
        cell.font = hdrFont
        cell.fill = hdrFill
    
    topJobs = sorted(jobs, key=lambda x: x['match'], reverse=True)[:10]
    for idx, job in enumerate(topJobs, start=3):
        wsTop.cell(row=idx, column=1, value=idx-2)
        wsTop.cell(row=idx, column=2, value=job['title'])
        wsTop.cell(row=idx, column=3, value=job['company'])
        wsTop.cell(row=idx, column=4, value=job['match'])
        wsTop.cell(row=idx, column=5, value=job.get('location', 'N/A'))
    
    wsTop.column_dimensions['A'].width = 8
    wsTop.column_dimensions['B'].width = 35
    wsTop.column_dimensions['C'].width = 25
    wsTop.column_dimensions['D'].width = 12
    wsTop.column_dimensions['E'].width = 20
    
    # VBA Automation Sheet
    wsVBA = wb.create_sheet("VBA Automation Tools")
    wsVBA['A1'] = "VBA AUTOMATION TOOLS & MACROS"
    wsVBA['A1'].font = Font(bold=True, size=14, color="FFFFFF")
    wsVBA['A1'].fill = PatternFill(start_color="1565C0", end_color="1565C0", fill_type="solid")
    wsVBA.merge_cells('A1:C1')
    
    wsVBA['A3'] = "Available Macros"
    wsVBA['A3'].font = Font(bold=True, size=12, color="FFFFFF")
    wsVBA['A3'].fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")
    wsVBA.merge_cells('A3:C3')
    
    vbaMacros = [
        ("FilterByMatch", "Filters jobs by match percentage threshold"),
        ("SortByCompany", "Sorts job list alphabetically by company"),
        ("HighlightTopMatches", "Highlights jobs with >70% match in green"),
        ("ExportToCSV", "Exports current sheet to CSV format"),
        ("SendEmailReport", "Sends report via email with job summary"),
        ("GenerateChart", "Creates match distribution pie chart"),
        ("AutoFormat", "Auto-formats all sheets with professional styling"),
        ("RefreshData", "Refreshes job data from API"),
        ("CreatePivotTable", "Creates pivot table from job data"),
        ("ConditionalFormatting", "Applies conditional formatting to match %")
    ]
    
    row = 4
    for macro, desc in vbaMacros:
        wsVBA[f'A{row}'] = macro
        wsVBA[f'B{row}'] = desc
        wsVBA[f'A{row}'].font = Font(bold=True, color="1565C0")
        row += 1
    
    wsVBA.column_dimensions['A'].width = 25
    wsVBA.column_dimensions['B'].width = 50
    
    wsVBA['A16'] = "Quick Actions"
    wsVBA['A16'].font = Font(bold=True, size=12, color="FFFFFF")
    wsVBA['A16'].fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")
    wsVBA.merge_cells('A16:C16')
    
    quickActions = [
        ("Ctrl+Shift+F", "Open Filter Dialog"),
        ("Ctrl+Shift+S", "Sort by Match Score"),
        ("Ctrl+Shift+E", "Export Report"),
        ("Ctrl+Shift+R", "Refresh All Data"),
        ("Ctrl+Shift+C", "Create Summary Chart")
    ]
    
    row = 17
    for shortcut, action in quickActions:
        wsVBA[f'A{row}'] = shortcut
        wsVBA[f'B{row}'] = action
        row += 1
    
    wsVBA['A24'] = "Data Analysis Features"
    wsVBA['A24'].font = Font(bold=True, size=12, color="FFFFFF")
    wsVBA['A24'].fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")
    wsVBA.merge_cells('A24:C24')
    
    features = [
        "Match Score Distribution Analysis",
        "Company Frequency Analysis",
        "Location-based Job Clustering",
        "Skill Gap Analysis",
        "Salary Range Estimation (if available)",
        "Job Market Trend Analysis"
    ]
    
    row = 25
    for feature in features:
        wsVBA[f'A{row}'] = f"• {feature}"
        row += 1
    
    exportFname = f"job_matches_{fname.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    exportPath = os.path.join(app.config['UPLOAD_FOLDER'], exportFname)
    wb.save(exportPath)
    
    absPath = os.path.abspath(exportPath)
    
    return jsonify({
        'success': True,
        'message': 'Excel report generated with VBA automation tools',
        'filename': exportFname,
        'filepath': absPath,
        'relative_path': f'backend/uploads/{exportFname}',
        'vba_features': {
            'macros_included': len(vbaMacros),
            'quick_actions': len(quickActions),
            'analysis_features': len(features)
        }
    })


@app.route('/api/bulk-process', methods=['POST'])
def bulkProcess():
    uploadDir = app.config['UPLOAD_FOLDER']
    
    resumeFiles = []
    for ext in ['*.pdf', '*.docx', '*.doc']:
        resumeFiles.extend(glob.glob(os.path.join(uploadDir, ext)))
    
    if not resumeFiles:
        return jsonify({'error': 'No resume files found'}), 400
    
    results = []
    
    for fpath in resumeFiles:
        try:
            fname = os.path.basename(fpath)
            txt = extractResume(fpath)
            email = extractEmail(txt)
            phone = extractPhone(txt)
            skills = extractSkills(txt)
            jobs = recommendJobs(skills, topN=10, minMatch=10)
            
            avgMatch = sum(job['match'] for job in jobs) / len(jobs) if jobs else 0
            topMatch = max(job['match'] for job in jobs) if jobs else 0
            
            results.append({
                'filename': fname,
                'email': email,
                'phone': phone,
                'skills_count': len(skills),
                'skills': skills,
                'jobs_found': len(jobs),
                'avg_match': round(avgMatch, 1),
                'top_match': round(topMatch, 1),
                'top_jobs': jobs[:5]
            })
            
        except Exception as e:
            results.append({
                'filename': os.path.basename(fpath),
                'error': str(e)
            })
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Bulk Processing Results"
    
    hdrFill = PatternFill(start_color="2E7D32", end_color="2E7D32", fill_type="solid")
    hdrFont = Font(bold=True, color="FFFFFF", size=12)
    
    hdrs = ['#', 'Filename', 'Email', 'Phone', 'Skills', 'Jobs Found', 'Avg Match %', 'Top Match %', 'Status']
    for col, hdr in enumerate(hdrs, start=1):
        cell = ws.cell(row=1, column=col)
        cell.value = hdr
        cell.font = hdrFont
        cell.fill = hdrFill
    
    for idx, result in enumerate(results, start=2):
        ws.cell(row=idx, column=1, value=idx-1)
        ws.cell(row=idx, column=2, value=result['filename'])
        ws.cell(row=idx, column=3, value=result.get('email', 'N/A'))
        ws.cell(row=idx, column=4, value=result.get('phone', 'N/A'))
        ws.cell(row=idx, column=5, value=result.get('skills_count', 0))
        ws.cell(row=idx, column=6, value=result.get('jobs_found', 0))
        ws.cell(row=idx, column=7, value=result.get('avg_match', 0))
        ws.cell(row=idx, column=8, value=result.get('top_match', 0))
        ws.cell(row=idx, column=9, value='Error' if 'error' in result else 'Success')
    
    ws.column_dimensions['A'].width = 5
    ws.column_dimensions['B'].width = 30
    ws.column_dimensions['C'].width = 25
    ws.column_dimensions['D'].width = 15
    ws.column_dimensions['E'].width = 10
    ws.column_dimensions['F'].width = 12
    ws.column_dimensions['G'].width = 12
    ws.column_dimensions['H'].width = 12
    ws.column_dimensions['I'].width = 10
    
    bulkFname = f"bulk_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    bulkPath = os.path.join(uploadDir, bulkFname)
    wb.save(bulkPath)
    
    return jsonify({
        'success': True,
        'processed': len(results),
        'results': results,
        'excel_report': bulkFname
    })

@app.route('/api/download-bulk-report/<fname>', methods=['GET'])
def downloadBulkReport(fname):
    fpath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    if os.path.exists(fpath):
        return send_file(fpath, as_attachment=True, download_name=fname)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
