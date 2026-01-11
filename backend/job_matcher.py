"""Job Matching Module - Handles job matching and filtering logic"""


def calc_match(resume_skills, job_skills):
    """Calculate match percentage between resume and job skills"""
    if not job_skills or not resume_skills:
        return 0
    
    resume_low = [s.lower().strip() for s in resume_skills]
    job_low = [s.lower().strip() for s in job_skills]
    
    exact = set(resume_low) & set(job_low)
    
    partial = 0
    for rs in resume_low:
        for js in job_low:
            if rs not in exact and js not in exact:
                if rs in js or js in rs:
                    partial += 0.5
                    break
    
    total = len(exact) + partial
    pct = (total / len(job_low)) * 100
    
    return min(pct, 100)


def recommend_jobs(resume_skills, jobs_db, top_n=10, min_match=10, loc_filter=None, skill_filter=None):
    """
    Recommend jobs based on resume skills
    
    Args:
        resume_skills: List of skills from resume
        jobs_db: List of available jobs
        top_n: Number of top jobs to return
        min_match: Minimum match percentage
        loc_filter: Location filter
        skill_filter: Skill filter
    
    Returns:
        List of matched jobs sorted by match percentage
    """
    matches = []
    
    print(f"Got {len(jobs_db)} jobs from db")
    print(f"Resume skills: {resume_skills}")
    
    for job in jobs_db:
        score = calc_match(resume_skills, job['required_skills'])
        
        resume_low = [s.lower().strip() for s in resume_skills]
        job_low = [s.lower().strip() for s in job['required_skills']]
        matching = []
        
        for rs in resume_skills:
            for js in job['required_skills']:
                if rs.lower() == js.lower() or rs.lower() in js.lower() or js.lower() in rs.lower():
                    if js not in matching:
                        matching.append(js)
        
        if loc_filter and loc_filter.lower() not in job.get('location', '').lower():
            continue
            
        if skill_filter:
            filter_low = [s.lower().strip() for s in skill_filter]
            has_skill = any(
                any(sf in js or js in sf for js in job_low)
                for sf in filter_low
            )
            if not has_skill:
                continue
        
        if score >= min_match:
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
    
    print(f"Returning {len(matches[:top_n])} jobs (filtered from {len(matches)} matches)")
    
    return matches[:top_n]
