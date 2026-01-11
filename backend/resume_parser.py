"""Resume Parsing Module - Handles resume extraction and skill detection"""

import PyPDF2
import docx2txt
import re


def extract_pdf(fpath):
    """Extract text from PDF"""
    txt = ""
    try:
        with open(fpath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                txt += page.extract_text()
    except Exception as e:
        print(f"PDF extract error: {e}")
    return txt


def extract_docx(fpath):
    """Extract text from DOCX"""
    try:
        return docx2txt.process(fpath)
    except Exception as e:
        print(f"DOCX extract error: {e}")
        return ""


def extract_doc(fpath):
    """Extract text from DOC"""
    try:
        return docx2txt.process(fpath)
    except Exception as e:
        print(f"DOC extract error: {e}")
        return ""


def extract_resume(fpath):
    """Extract text from resume file"""
    ext = fpath.rsplit('.', 1)[1].lower()
    if ext == 'pdf':
        return extract_pdf(fpath)
    elif ext == 'docx':
        return extract_docx(fpath)
    elif ext == 'doc':
        return extract_doc(fpath)
    else:
        return ""


def extract_email(txt):
    """Extract email from text"""
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, txt)
    return emails[0] if emails else None


def extract_phone(txt):
    """Extract phone number from text"""
    pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(pattern, txt)
    return phones[0] if phones else None


def extract_skills(txt):
    """Extract skills from resume text"""
    txt_low = txt.lower()
    skill_kws = {
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
    for skill in skill_kws:
        if skill in txt_low:
            found.append(skill)
    
    return found
