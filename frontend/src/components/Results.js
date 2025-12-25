import React, { useState } from 'react';
import { motion } from 'framer-motion';
import axios from 'axios';

const Results = ({ data, onReset }) => {
  const [filteredJobs, setFilteredJobs] = useState(data.jobs);
  const [selLoc, setSelLoc] = useState('');
  const [selSkills, setSelSkills] = useState([]);
  const [minMatch, setMinMatch] = useState(10);
  const [isFiltering, setIsFiltering] = useState(false);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const cacheInfo = data.cache_info || {};
  
  const applyFilters = async () => {
    setIsFiltering(true);
    try {
      const resp = await axios.post('http://localhost:5000/api/filter-jobs', {
        skills: data.skills,
        location: selLoc || null,
        skill_filters: selSkills,
        min_match: minMatch
      });
      setFilteredJobs(resp.data.jobs);
    } catch (err) {
      console.error('Filter error:', err);
    }
    setIsFiltering(false);
  };
  
  const resetFilters = () => {
    setSelLoc('');
    setSelSkills([]);
    setMinMatch(10);
    setFilteredJobs(data.jobs);
  };
  
  const toggleSkill = (skill) => {
    if (selSkills.includes(skill)) {
      setSelSkills(selSkills.filter(s => s !== skill));
    } else {
      setSelSkills([...selSkills, skill]);
    }
  };
  
  const refreshJobs = async () => {
    setIsRefreshing(true);
    try {
      const resp = await axios.post('http://localhost:5000/api/refresh-jobs');
      alert(`Refreshed ${resp.data.jobs_count} jobs from live sources`);
      window.location.reload();
    } catch (err) {
      console.error('Refresh error:', err);
      alert('Failed to refresh jobs. Please try again.');
    }
    setIsRefreshing(false);
  };
  
  const exportToExcel = async () => {
    try {
      const resp = await axios.post('http://localhost:5000/api/export-excel', {
        filename: data.filename,
        email: data.email,
        phone: data.phone,
        skills: data.skills,
        jobs: filteredJobs
      });
      
      const msg = `Excel report saved successfully\n\nLocation: ${resp.data.relative_path}\n\nFilename: ${resp.data.filename}`;
      alert(msg);
    } catch (err) {
      console.error('Export error:', err);
      alert('Failed to export to Excel. Please try again.');
    }
  };
  
  return (
    <motion.div
      className="resultsContainer"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
    >
      <div className="resultsCard">
        <div className="resultsHeader">
          <div>
            <h2>Resume Analysis Complete</h2>
            {cacheInfo && (
              <p className="cacheStatus">
                {cacheInfo.is_fresh ? 'Fresh' : 'Expired'} - Jobs updated: {cacheInfo.last_updated}
              </p>
            )}
          </div>
          <div className="headerButtons">
            <button onClick={exportToExcel} className="exportBtn">
              Export to Excel
            </button>
            <button onClick={refreshJobs} className="refreshBtn" disabled={isRefreshing}>
              {isRefreshing ? 'Refreshing...' : 'Refresh Jobs'}
            </button>
            <button onClick={onReset} className="resetBtn">
              Upload Another
            </button>
          </div>
        </div>

        <div className="infoSection">
          <div className="infoItem">
            <strong>Email:</strong> {data.email || 'Not found'}
          </div>
          <div className="infoItem">
            <strong>Phone:</strong> {data.phone || 'Not found'}
          </div>
          <div className="infoItem">
            <strong>File:</strong> {data.filename}
          </div>
          {data.skills && data.skills.length > 0 && (
            <div className="infoItem skillsItem">
              <strong>Detected Skills:</strong>
              <div className="skillsTags">
                {data.skills.map((skill, idx) => (
                  <span key={idx} className="skillTag">{skill}</span>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="filtersSection">
          <h3>Filter Jobs</h3>
          
          <div className="filterRow">
            <div className="filterGroup">
              <label>Location:</label>
              <select 
                value={selLoc} 
                onChange={(e) => setSelLoc(e.target.value)}
                className="filterSelect"
              >
                <option value="">All Locations</option>
                {data.available_locations && data.available_locations.map((loc, idx) => (
                  <option key={idx} value={loc}>{loc}</option>
                ))}
              </select>
            </div>
            
            <div className="filterGroup">
              <label>Min Match %:</label>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={minMatch}
                onChange={(e) => setMinMatch(parseInt(e.target.value))}
                className="filterSlider"
              />
              <span className="matchValue">{minMatch}%</span>
            </div>
          </div>
          
          <div className="filterGroup">
            <label>Required Skills:</label>
            <div className="skillsMultiselect">
              {data.available_skills && data.available_skills.slice(0, 20).map((skill, idx) => (
                <button
                  key={idx}
                  className={`skillFilterBtn ${selSkills.includes(skill) ? 'active' : ''}`}
                  onClick={() => toggleSkill(skill)}
                >
                  {skill}
                </button>
              ))}
            </div>
          </div>
          
          <div className="filterActions">
            <button onClick={applyFilters} className="applyFilterBtn" disabled={isFiltering}>
              {isFiltering ? 'Filtering...' : 'Apply Filters'}
            </button>
            <button onClick={resetFilters} className="resetFilterBtn">
              Reset Filters
            </button>
          </div>
        </div>

        <div className="jobsSection">
          <h3>Recommended Jobs ({filteredJobs ? filteredJobs.length : 0} matches)</h3>
          {filteredJobs && filteredJobs.length > 0 ? filteredJobs.map((job, idx) => (
            <motion.div
              key={idx}
              className="jobCard"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: idx * 0.1 }}
            >
              <div className="jobHeader">
                <div className="jobTitleWrapper">
                  <div className="jobTitle">{job.title}</div>
                  {job.is_fallback && (
                    <span className="fallbackBadge" title="From fallback database">Fallback</span>
                  )}
                </div>
                <div className="matchBadge">{job.match}% Match</div>
              </div>
              <div className="jobCompany">{job.company}</div>
              {job.location && (
                <div className="jobLocation">{job.location}</div>
              )}
              {job.scraped_at && (
                <div className="jobTimestamp">Scraped: {job.scraped_at}</div>
              )}
              <div className="jobDesc">{job.description}</div>
              {job.matching_skills && job.matching_skills.length > 0 && (
                <div className="matchingSkills">
                  <strong>Matching Skills:</strong>
                  <div className="skillsTags">
                    {job.matching_skills.map((skill, idx) => (
                      <span key={idx} className="skillTag match">{skill}</span>
                    ))}
                  </div>
                </div>
              )}
              {job.link && (
                <a href={job.link} target="_blank" rel="noopener noreferrer" className="jobLink">
                  View Job
                </a>
              )}
            </motion.div>
          )) : (
            <div className="noJobs">
              <p>No matching jobs found. Try uploading a different resume or check your internet connection.</p>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default Results;
