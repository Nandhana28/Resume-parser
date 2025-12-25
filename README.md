# Resume Job Matcher with VBA Excel Automation

## Project Overview

Resume Job Matcher is a full-stack web application that analyzes resumes, extracts key information, and matches candidates with relevant job opportunities from multiple sources. The application features intelligent skill detection, real-time job scraping from global and Indian job portals, and professional Excel report generation with VBA-style formatting.

This tool is designed for job seekers, recruitment agencies, and HR departments to streamline the job matching process and generate comprehensive reports for analysis and tracking.

## Key Features

### Core Functionality
- Resume parsing and text extraction from PDF, DOCX, and DOC files
- Automatic skill detection from resume content (70+ recognized skills)
- Multi-source job scraping from global and Indian job portals
- Intelligent job matching algorithm with fuzzy skill matching
- Advanced filtering by location, skills, and match percentage
- Real-time job caching to optimize performance

### VBA Excel Automation Features

#### 1. Excel Report Generation
Export job matches to professionally formatted Excel reports with:
- Dashboard sheet with summary statistics and match distribution
- Skills sheet listing all detected skills from resume
- Job Matches sheet with color-coded match percentages
- Top 10 Matches sheet with best opportunities ranked by relevance
- Professional styling with headers, borders, and conditional formatting
- Auto-sized columns for optimal readability
- Direct application links for each job

#### 2. Bulk Resume Processing
Process multiple resumes simultaneously:
- Upload multiple resume files to the uploads folder
- Process all resumes with a single API call
- Generate consolidated Excel report with all results
- Track processing status for each resume
- Export summary statistics and top matches
- Perfect for recruitment agencies and HR departments

### Job Sources
- Naukri.com - India's largest job portal
- Instahyre - Indian tech job portal
- RemoteOK - International remote jobs via API
- Indeed - Global job search engine
- Fallback database - Jobs from major Indian IT companies (TCS, Infosys, Wipro, Accenture, HCL, Tech Mahindra, Cognizant, Capgemini)

## Technology Stack

### Backend
- Flask - Python web framework
- BeautifulSoup4 - Web scraping and HTML parsing
- PyPDF2 - PDF file parsing
- python-docx - DOCX file parsing
- openpyxl - Excel file generation and formatting
- xlsxwriter - Advanced Excel features
- requests - HTTP client for API calls
- CORS - Cross-Origin Resource Sharing support

### Frontend
- React 18 - UI framework
- Framer Motion - Smooth animations and transitions
- Axios - HTTP client for API communication
- React Dropzone - Drag-and-drop file upload
- CSS3 - Modern styling with dark theme

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn package manager

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the Flask server:
```bash
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

Frontend runs on `http://localhost:3000`

## Usage Guide

### Basic Workflow

1. Open the application in your browser at `http://localhost:3000`
2. Upload your resume (PDF, DOCX, or DOC format)
3. Wait for analysis to complete (5-10 seconds)
4. Review extracted information:
   - Email address
   - Phone number
   - Detected skills
5. View recommended jobs with match percentages
6. Use filters to refine results:
   - Filter by location
   - Filter by required skills
   - Adjust minimum match percentage
7. Export results to Excel for further analysis
8. Click job links to apply directly

### Excel Report Features

The generated Excel reports include:

- Dashboard: Overview of resume analysis with statistics
- Skills: Complete list of detected skills
- Job Matches: All matching jobs with color-coded percentages
- Top 10: Best matching opportunities ranked by relevance

Color coding in match percentages:
- Green (70%+): Excellent match
- Yellow (50-69%): Good match
- Orange (30-49%): Fair match
- Default: Low match

### Bulk Processing

1. Place multiple resume files in `backend/uploads/` folder
2. Send POST request to `/api/bulk-process` endpoint
3. Receive consolidated Excel report with all results
4. Download report from the uploads folder

## API Endpoints

### Resume Analysis
- `POST /api/upload` - Upload and analyze resume
- `POST /api/filter-jobs` - Filter jobs with custom criteria
- `POST /api/refresh-jobs` - Force refresh jobs from live sources

### Excel Export
- `POST /api/export-excel` - Generate Excel report for single resume
- `POST /api/bulk-process` - Process multiple resumes
- `GET /api/download-bulk-report/<filename>` - Download bulk report

### Job Management
- `GET /api/jobs` - Get cached job listings
- `POST /api/scrape-jobs` - Manually trigger job scraping
- `GET /api/cache-status` - Check cache freshness
- `GET /api/health` - Health check endpoint

## Web Scraping Implementation

### Scraping Strategy

The application uses a multi-source scraping strategy to ensure reliable job data:

1. **Primary Sources**: Naukri.com and Instahyre for Indian jobs
2. **Secondary Sources**: RemoteOK API and Indeed for international jobs
3. **Fallback Database**: Curated list of major Indian IT companies

### Scraping Technologies

- BeautifulSoup4: HTML parsing and element extraction
- Requests: HTTP requests with custom headers
- Selenium: Browser automation (optional for JavaScript-heavy sites)

### Scraping Implementation Details

#### Naukri.com Scraping
- Targets India's largest job portal
- Extracts job title, company, location, and job link
- Handles multiple HTML selectors for robustness
- Implements timeout and error handling

#### RemoteOK API
- Uses public JSON API for reliable data
- No HTML parsing required
- Provides international remote job opportunities
- Most reliable source with consistent data format

#### Indeed Scraping
- Scrapes global job listings
- Handles dynamic class names and selectors
- Implements fallback selectors for robustness
- Respects rate limiting with timeouts

#### Instahyre Scraping
- Targets Indian tech job portal
- Focuses on startup and tech company positions
- Extracts job details and company information

### Skill Extraction

The application detects 70+ technical skills including:

**Programming Languages**: Python, Java, JavaScript, C++, C#, Ruby, PHP, Swift, Kotlin, Go, Rust, TypeScript, VBA, R, MATLAB, Scala, Perl

**Web Technologies**: HTML, CSS, React, Angular, Vue, Node.js, Express, Django, Flask, Spring, ASP.NET

**Databases**: SQL, MySQL, PostgreSQL, MongoDB, Redis, Oracle, SQLite, Cassandra, DynamoDB

**Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, CI/CD, Terraform, Ansible

**Data Science & ML**: Machine Learning, Deep Learning, Data Analysis, Pandas, NumPy, Scikit-learn, TensorFlow, PyTorch, Keras, Statistics, Tableau, Power BI

**Mobile Development**: Android, iOS, React Native, Flutter

**Microsoft Office**: Excel, VBA, Macros, Power Query, Power Pivot, Access, Word, PowerPoint

**Other**: Git, Agile, Scrum, REST API, GraphQL, Microservices, Linux, Unix, Testing, JUnit, Selenium

### Caching Mechanism

- Jobs are cached for 30 minutes to reduce API calls
- Cache automatically refreshes when expired
- Manual refresh option available via API
- Timestamp tracking for cache freshness

### Error Handling

- Graceful fallback to cached data if scraping fails
- Fallback database with curated job listings
- Timeout handling for slow connections
- Comprehensive error logging

## Project Structure

```
resume-job-matcher/
├── backend/
│   ├── app.py                 Main Flask application
│   ├── requirements.txt       Python dependencies
│   ├── test_backend.py        Backend API tests
│   ├── test_scraping.py       Scraping functionality tests
│   ├── test_vba_features.py   VBA features tests
│   ├── VBA_FEATURES_GUIDE.txt VBA automation guide
│   └── uploads/               Resume uploads and Excel exports
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js  Resume upload component
│   │   │   └── Results.js     Results display component
│   │   ├── App.js             Main application component
│   │   ├── App.css            Application styling
│   │   └── index.js           Entry point
│   └── package.json           Node dependencies
├── Datasets/                  Sample resumes for testing
├── README.md                  This file
├── QUICK_START.txt            Quick reference guide
└── start_backend.bat          Windows startup script
```

## Testing

### Test Job Scraping
```bash
cd backend
python test_scraping.py
```

Shows status of all job sources and sample jobs.

### Test Backend APIs
```bash
cd backend
python test_backend.py
```

Tests all API endpoints and job retrieval.

### Test VBA Features
```bash
cd backend
python test_vba_features.py
```

Tests Excel export and bulk processing functionality.

## Configuration

### Environment Variables
- `UPLOAD_FOLDER`: Directory for resume uploads (default: 'uploads')
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)
- `CACHE_DURATION`: Job cache duration in seconds (default: 1800)

### Customization

Modify scraping parameters in `backend/app.py`:
- `maxJobs`: Number of jobs to scrape per source
- `cacheDur`: Cache duration in seconds
- `ALLOWED_EXTENSIONS`: Supported file types

## Performance Optimization

- Job caching reduces API calls and improves response time
- Lazy loading of job data
- Optimized skill matching algorithm
- Efficient Excel report generation
- Minimal frontend bundle size

## Security Considerations

- File upload validation (extension and size checks)
- Secure filename handling with werkzeug
- CORS protection enabled
- Input sanitization for skill extraction
- No sensitive data stored in cache

## Troubleshooting

### Upload Fails
1. Check backend is running on port 5000
2. Verify file format (PDF, DOCX, DOC)
3. Check file size (max 16MB)
4. Review browser console for error details

### No Jobs Found
1. Check internet connection
2. Run `test_scraping.py` to verify sources
3. Check backend logs for scraping errors
4. Fallback database will be used if scraping fails

### Excel Export Issues
1. Verify openpyxl is installed: `pip install openpyxl xlsxwriter`
2. Check backend is running
3. Ensure browser allows file downloads
4. Check backend console for errors

### Slow Performance
1. Clear browser cache
2. Restart backend to clear job cache
3. Check internet connection speed
4. Reduce number of jobs to process

## Future Enhancements

- LinkedIn integration for job scraping
- Email automation for job applications
- Resume template generator
- Interview preparation assistant
- Salary comparison tool
- Application tracking system
- Network contact manager
- Advanced analytics dashboard

## Contributing

Contributions are welcome. Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check this README
2. Run test scripts to diagnose issues
3. Review browser console (F12)
4. Check backend logs
5. Refer to VBA_FEATURES_GUIDE.txt for automation features

## Acknowledgments

- Job data from Naukri.com, Instahyre, RemoteOK, and Indeed
- Built with Flask, React, and modern web technologies
- Inspired by the need for efficient job matching solutions

---

**Last Updated**: December 2025
**Version**: 2.0 (VBA Features Included)
**Status**: Production Ready
