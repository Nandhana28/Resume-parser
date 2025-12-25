# Resume Parser & Job Matcher with VBA Excel Automation

A full-stack web application that analyzes resumes, matches them with real jobs from multiple sources, and provides **VBA-powered Excel automation** for professional reporting and bulk processing.

## 🚀 Features

### Core Features
- **Resume Parsing** - Extract text from PDF, DOCX, and DOC files
- **Smart Skill Detection** - Identifies 70+ technical skills including VBA, Python, Java, React, AWS, etc.
- **Multi-Source Job Scraping** - Real jobs from Naukri.com, Instahyre, RemoteOK, and Indeed
- **Intelligent Matching** - Fuzzy skill matching with accurate percentage calculations
- **Advanced Filtering** - Filter by location, skills, and minimum match percentage

### 🆕 VBA Excel Automation Features

#### 1. **Excel Report Generation** 📊
Export job matches to professionally formatted Excel reports with:
- **Dashboard Sheet** - Summary statistics and match distribution
- **Skills Sheet** - All detected skills from resume
- **Job Matches Sheet** - Complete job listings with color-coded match percentages
  - Green (70%+) - Excellent matches
  - Yellow (50-69%) - Good matches
  - Orange (30-49%) - Fair matches
- **Top 10 Sheet** - Best matching jobs ranked by relevance
- **Auto-formatting** - Professional styling with headers, borders, and colors
- **One-click download** - Export directly from the web interface

#### 2. **Bulk Resume Processing** 📁
Process multiple resumes at once:
- Upload multiple resume files to the `backend/uploads` folder
- Process all resumes with a single API call
- Generate consolidated Excel report with:
  - Resume filename, email, phone
  - Skills count and detected skills
  - Jobs found and match statistics
  - Top 5 jobs for each resume
  - Success/error status for each file
- Perfect for recruitment agencies and HR departments

### Job Sources
- **Naukri.com** - India's largest job portal (8 jobs per search)
- **Instahyre** - Indian tech jobs (5 jobs per search)
- **RemoteOK** - International remote jobs via API (7 jobs)
- **Indeed** - Global job search engine (5 jobs)
- **Fallback Database** - Jobs from TCS, Infosys, Wipro, Accenture, HCL, Tech Mahindra, Cognizant, Capgemini

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **BeautifulSoup4** - Web scraping
- **PyPDF2** - PDF parsing
- **python-docx** - DOCX parsing
- **openpyxl** - Excel file generation with VBA-style formatting
- **xlsxwriter** - Advanced Excel features

### Frontend
- **React 18** - UI framework
- **Framer Motion** - Smooth animations
- **Axios** - HTTP client
- **React Dropzone** - File upload

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

Frontend runs on `http://localhost:3000`

## 🎯 Usage

### Basic Usage
1. **Upload Resume** - Drag and drop or click to upload (PDF, DOCX, DOC)
2. **View Results** - See extracted skills and matched jobs
3. **Filter Jobs** - Use location, skills, and match percentage filters
4. **Export to Excel** - Click "📊 Export to Excel" for professional report
5. **Apply** - Click job links to apply directly

### VBA Excel Export Usage
1. Upload and analyze your resume
2. Click **"📊 Export to Excel"** button
3. Excel file downloads automatically with:
   - Dashboard with statistics
   - Skills list
   - All job matches (color-coded)
   - Top 10 matches
4. Open in Excel/LibreOffice/Google Sheets
5. Use for job applications, tracking, or portfolio

### Bulk Processing Usage
1. Place multiple resume files in `backend/uploads/` folder
2. Send POST request to `/api/bulk-process`:
```bash
curl -X POST http://localhost:5000/api/bulk-process
```
3. Receive JSON response with all results
4. Download consolidated Excel report
5. Review all candidates in one spreadsheet

## 🔧 API Endpoints

### Resume Analysis
- `POST /api/upload` - Upload resume, get job matches
- `POST /api/filter-jobs` - Filter jobs with criteria
- `POST /api/refresh-jobs` - Force refresh jobs from live sources

### VBA Excel Features
- `POST /api/export-excel` - Generate Excel report for single resume
- `POST /api/bulk-process` - Process multiple resumes, generate bulk report
- `GET /api/download-bulk-report/<filename>` - Download bulk processing report

### Job Management
- `GET /api/jobs` - Get cached jobs
- `POST /api/scrape-jobs` - Manually trigger job scraping
- `GET /api/cache-status` - Check cache freshness
- `GET /api/health` - Health check

## 📊 Excel Report Structure

### Dashboard Sheet
```
RESUME JOB MATCH REPORT
├── Resume Information
│   ├── Filename
│   ├── Email
│   ├── Phone
│   ├── Skills Found
│   └── Report Date
├── Job Match Statistics
│   ├── Total Jobs Found
│   ├── Average Match %
│   └── Top Match %
└── Match Distribution
    ├── Excellent (70%+)
    ├── Good (50-69%)
    ├── Fair (30-49%)
    └── Low (<30%)
```

### Job Matches Sheet
- Color-coded match percentages
- Direct application links
- Matching skills highlighted
- Professional formatting

## 🧪 Testing

### Test Job Scraping
```bash
cd backend
python test_scraping.py
```

Shows status of:
- ✓ Naukri.com (Indian jobs)
- ✓ RemoteOK API (remote jobs)
- ✓ Indeed scraping

### Test Backend
```bash
cd backend
python test_backend.py
```

Tests all API endpoints and job retrieval.

## 🐛 Troubleshooting

### No Jobs Showing?

**Step 1**: Check backend console for:
```
DEBUG: Extracted X skills from resume
DEBUG: Got X jobs from database
DEBUG: Returning X jobs
```

**Step 2**: Test backend:
```bash
cd backend
python test_backend.py
```

**Step 3**: Check browser console (F12) for errors

**Step 4**: Test scraping:
```bash
cd backend
python test_scraping.py
```

### Excel Export Not Working?

**Check**:
- `openpyxl` and `xlsxwriter` installed: `pip install openpyxl xlsxwriter`
- Backend running on port 5000
- Browser allows file downloads
- Check backend console for errors

### Bulk Processing Issues?

**Check**:
- Resume files are in `backend/uploads/` folder
- Files are PDF, DOCX, or DOC format
- Backend has read permissions for uploads folder
- Check backend console for processing logs

## 📁 Project Structure

```
resume-job-matcher/
├── backend/
│   ├── app.py                 # Main Flask app with VBA features
│   ├── requirements.txt       # Python dependencies
│   ├── test_backend.py        # Backend tests
│   ├── test_scraping.py       # Scraping tests
│   └── uploads/               # Resume uploads & Excel exports
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js  # Upload component
│   │   │   └── Results.js     # Results with Excel export
│   │   ├── App.js             # Main app
│   │   ├── App.css            # Styling
│   │   └── index.js           # Entry point
│   └── package.json           # Node dependencies
├── Datasets/                  # Sample resumes for testing
├── Resume_parser.ipynb        # Jupyter notebook with ML models
├── start_backend.bat          # Windows startup script
└── README.md                  # This file
```

## 🎨 Features Showcase

### Smart Skill Detection
Detects 70+ skills including:
- **Programming**: Python, Java, JavaScript, C++, VBA, R
- **Web**: React, Angular, Vue, Node.js, Django, Flask
- **Database**: SQL, MySQL, PostgreSQL, MongoDB, Redis
- **Cloud**: AWS, Azure, GCP, Docker, Kubernetes
- **Data**: Machine Learning, Data Analysis, Pandas, NumPy
- **Office**: VBA, Excel, Macros, Power Query, Access

### Indian Job Market Focus
- Naukri.com integration for Indian jobs
- Instahyre for tech startups
- Major Indian cities covered (Bangalore, Hyderabad, Pune, Mumbai, Chennai, etc.)
- Fallback jobs from top Indian IT companies

### Professional Excel Reports
- VBA-style formatting and styling
- Color-coded match percentages
- Auto-sized columns
- Professional headers and borders
- Ready for printing or sharing

## 🔮 Future Enhancements

- LinkedIn integration
- Email automation for job applications
- Resume template generator
- Interview preparation assistant
- Salary comparison tool
- Application tracking system
- Network contact manager

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## 📧 Support

For issues or questions:
1. Check this README
2. Run test scripts (`test_backend.py`, `test_scraping.py`)
3. Check browser console (F12)
4. Review backend logs

---

**Built with ❤️ for job seekers and recruiters**

*Featuring VBA-powered Excel automation for professional reporting*
