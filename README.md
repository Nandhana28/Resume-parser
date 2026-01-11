# Resume Parser & Job Matcher with VBA Excel Automation

A full-stack web application that analyzes resumes, matches them with real jobs from multiple sources, and provides VBA-powered Excel automation for professional reporting and bulk processing.

## 🎯 Quick Start - VBA Features

### Export with VBA Tools (3 Steps)
1. Upload resume → Click "Export to Excel"
2. Open Excel file → Press `Alt+F11` to open VBA Editor
3. Copy macros from `backend/vba_macros_template.bas` → Paste into module → Run with `Alt+F8`

### 10 Pre-Built VBA Macros
- **FilterByMatch** - Filter jobs by match percentage
- **SortByMatchScore** - Sort jobs highest match first
- **HighlightTopMatches** - Color-code jobs by quality
- **ExportToCSV** - Export sheet to CSV
- **GenerateChart** - Create match distribution chart
- **AutoFormatSheets** - Professional formatting
- **CreateSummaryStats** - Generate statistics
- **ApplyConditionalFormatting** - Auto-format match %
- **ShowNavigationMenu** - Quick navigation
- **ExportTop10** - Export top 10 to new workbook

See `backend/vba_macros_template.bas` for complete macro code.

## Features

### Core Features
- Resume Parsing - Extract text from PDF, DOCX, and DOC files
- Smart Skill Detection - Identifies 70+ technical skills including VBA, Python, Java, React, AWS, etc.
- Multi-Source Job Scraping - Real jobs from Naukri.com, Instahyre, RemoteOK, and Indeed
- Intelligent Matching - Fuzzy skill matching with accurate percentage calculations
- Advanced Filtering - Filter by location, skills, and minimum match percentage

### VBA Excel Automation Features

#### 1. Excel Report Generation

Export job matches to professionally formatted Excel reports with:
- Dashboard Sheet - Summary statistics and match distribution
- Skills Sheet - All detected skills from resume
- Job Matches Sheet - Complete job listings with color-coded match percentages
  - Green (70%+) - Excellent matches
  - Yellow (50-69%) - Good matches
  - Orange (30-49%) - Fair matches
- Top 10 Sheet - Best matching jobs ranked by relevance
- **VBA Automation Tools Sheet** - Pre-built macros and quick actions
- Auto-formatting - Professional styling with headers, borders, and colors
- One-click download - Export directly from the web interface

#### 2. VBA Macros (10 Pre-Built)

Included macros for Excel automation:
- **FilterByMatch** - Filter jobs by minimum match percentage
- **SortByMatchScore** - Sort jobs by match (highest first)
- **HighlightTopMatches** - Color-code jobs by quality
- **ExportToCSV** - Export sheet to CSV format
- **GenerateChart** - Create match distribution pie chart
- **AutoFormatSheets** - Apply professional formatting to all sheets
- **CreateSummaryStats** - Generate detailed statistics sheet
- **ApplyConditionalFormatting** - Auto-format match % column
- **ShowNavigationMenu** - Quick navigation between sheets
- **ExportTop10** - Export top 10 matches to new workbook

See `VBA_SETUP_GUIDE.md` for detailed setup instructions.

#### 3. Bulk Resume Processing

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
- Naukri.com - India's largest job portal (8 jobs per search)
- Instahyre - Indian tech jobs (5 jobs per search)
- RemoteOK - International remote jobs via API (7 jobs)
- Indeed - Global job search engine (5 jobs)
- Fallback Database - Jobs from TCS, Infosys, Wipro, Accenture, HCL, Tech Mahindra, Cognizant, Capgemini

## Tech Stack

### Backend
- Flask - Python web framework
- BeautifulSoup4 - Web scraping
- PyPDF2 - PDF parsing
- python-docx - DOCX parsing
- openpyxl - Excel file generation with VBA-style formatting
- xlsxwriter - Advanced Excel features

### Frontend
- React 18 - UI framework
- Framer Motion - Smooth animations
- Axios - HTTP client
- React Dropzone - File upload

## Installation

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

## Usage

### Basic Usage
1. Upload Resume - Drag and drop or click to upload (PDF, DOCX, DOC)
2. View Results - See extracted skills and matched jobs
3. Filter Jobs - Use location, skills, and match percentage filters
4. Export to Excel - Click "Export to Excel" for professional report
5. Apply - Click job links to apply directly

### VBA Excel Export Usage
1. Upload and analyze your resume
2. Click "Export to Excel" button
3. Excel file downloads with:
   - Dashboard with statistics
   - Skills list
   - All job matches (color-coded)
   - Top 10 matches
   - **VBA Automation Tools sheet** with 10 pre-built macros
4. Open in Excel and add VBA macros:
   - Press `Alt+F11` to open VBA Editor
   - Right-click VBAProject → Insert → Module
   - Copy macro code from `backend/vba_macros_template.bas`
   - Paste into module and save as `.xlsm` format
5. Run macros with `Alt+F8`

### VBA Macro Examples

**Filter Jobs by Match %:**
```
Alt+F8 → FilterByMatch → Enter 60 → Shows only 60%+ matches
```

**Sort by Match Score:**
```
Alt+F8 → SortByMatchScore → Jobs sorted highest first
```

**Create Professional Report:**
```
Alt+F8 → AutoFormatSheets
Alt+F8 → GenerateChart
Alt+F8 → CreateSummaryStats
```

### Bulk Processing Usage
1. Place multiple resume files in `backend/uploads/` folder
2. Send POST request to `/api/bulk-process`:
```bash
curl -X POST http://localhost:5000/api/bulk-process
```
3. Receive JSON response with all results
4. Download consolidated Excel report
5. Review all candidates in one spreadsheet

## API Endpoints

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

## Excel Report Structure

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

## Troubleshooting

### No Jobs Showing?

Step 1: Check backend console for:
```
DEBUG: Extracted X skills from resume
DEBUG: Got X jobs from database
DEBUG: Returning X jobs
```

Step 2: Check browser console (F12) for errors

### Excel Export Not Working?

Check:
- `openpyxl` and `xlsxwriter` installed: `pip install openpyxl xlsxwriter`
- Backend running on port 5000
- Browser allows file downloads
- Check backend console for errors

### Bulk Processing Issues?

Check:
- Resume files are in `backend/uploads/` folder
- Files are PDF, DOCX, or DOC format
- Backend has read permissions for uploads folder
- Check backend console for processing logs

## Project Structure

```
Resume-parser/
├── backend/
│   ├── app.py                    Main Flask app (clean, modular)
│   ├── resume_parser.py          Resume extraction & skill detection
│   ├── job_scraper.py            Multi-source job scraping
│   ├── job_matcher.py            Job matching algorithm
│   ├── vba_export.py             Excel export with VBA tools
│   ├── vba_macros_template.bas   10 pre-built VBA macros
│   ├── requirements.txt          Python dependencies
│   └── uploads/                  Resume uploads & Excel exports
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js     Upload component
│   │   │   └── Results.js        Results with Excel export
│   │   ├── App.js                Main app
│   │   ├── App.css               Styling
│   │   └── index.js              Entry point
│   └── package.json              Node dependencies
├── Datasets/                     Sample resumes for testing
├── start_backend.bat             Windows startup script
└── README.md                     This file
```

## VBA Automation Guide

### What's Included
- **VBA Automation Tools Sheet** - Auto-generated in every Excel export
- **10 Pre-Built Macros** - Copy-paste ready, no coding required
- **Macro Template File** - `backend/vba_macros_template.bas`

### How to Add Macros

**Step 1: Open VBA Editor**
```
Excel → Alt+F11
```

**Step 2: Insert Module**
```
Right-click VBAProject → Insert → Module
```

**Step 3: Copy & Paste Macro**
```
Copy from: backend/vba_macros_template.bas
Paste into: VBA module
Save as: .xlsm format (macro-enabled)
```

**Step 4: Run Macro**
```
Alt+F8 → Select macro → Run
```

### Macro Reference

| Macro | Purpose | Usage |
|-------|---------|-------|
| FilterByMatch | Filter by match % | Alt+F8 → Enter threshold |
| SortByMatchScore | Sort highest first | Alt+F8 → Auto-sorts |
| HighlightTopMatches | Color-code jobs | Alt+F8 → Green/Yellow/Orange |
| ExportToCSV | Export to CSV | Alt+F8 → Creates CSV file |
| GenerateChart | Create pie chart | Alt+F8 → New sheet with chart |
| AutoFormatSheets | Professional styling | Alt+F8 → Formats all sheets |
| CreateSummaryStats | Statistics sheet | Alt+F8 → New stats sheet |
| ApplyConditionalFormatting | Auto-format % column | Alt+F8 → Color rules applied |
| ShowNavigationMenu | Quick navigation | Alt+F8 → Choose sheet |
| ExportTop10 | Export top 10 | Alt+F8 → New workbook |

### Troubleshooting

**Macros not showing in Alt+F8?**
- Save file as `.xlsm` format
- Close and reopen Excel
- Check VBA module has code

**"Object Required" error?**
- Check sheet names match exactly
- Verify "Job Matches" sheet exists
- Ensure data starts from row 2

**Macro runs but nothing happens?**
- Check if data exists in sheet
- Verify row/column numbers
- Check for hidden rows/columns

### Pro Tips

1. **Save as Macro-Enabled**
   ```
   File → Save As → Format: Excel Macro-Enabled (.xlsm)
   ```

2. **Test on Copy**
   ```
   Always test macros on a copy first
   Keep original file safe
   ```

3. **Combine Macros**
   ```
   Run AutoFormatSheets first
   Then ApplyConditionalFormatting
   Then GenerateChart
   ```

4. **Keyboard Shortcuts**
   ```
   Alt+F8 = Run Macro
   Alt+F11 = Open VBA Editor
   Ctrl+S = Save
   ```

## Architecture

### Modular Backend Design

**app.py** - Main Flask application with clean API endpoints

**resume_parser.py** - Resume extraction
- PDF, DOCX, DOC parsing
- Email & phone extraction
- Skill detection (70+ skills)

**job_scraper.py** - Multi-source job scraping
- Naukri.com, Instahyre, RemoteOK, Indeed
- Fallback jobs from Indian IT companies
- Skill extraction from job titles

**job_matcher.py** - Intelligent job matching
- Fuzzy skill matching
- Match percentage calculation
- Filtering by location & skills

**vba_export.py** - Excel generation with VBA tools
- Professional formatting
- VBA Automation Tools sheet
- Color-coded match percentages

**vba_macros_template.bas** - VBA macro code
- 10 pre-built macros
- Copy-paste ready
- Fully commented

### Smart Skill Detection

Detects 70+ skills including:
- Programming: Python, Java, JavaScript, C++, VBA, R
- Web: React, Angular, Vue, Node.js, Django, Flask
- Database: SQL, MySQL, PostgreSQL, MongoDB, Redis
- Cloud: AWS, Azure, GCP, Docker, Kubernetes
- Data: Machine Learning, Data Analysis, Pandas, NumPy
- Office: VBA, Excel, Macros, Power Query, Access

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

## License

This project is open source and available for educational purposes.

---

## Summary

✅ **Modular Backend** - 5 separate Python modules for easy maintenance
✅ **VBA Automation** - 10 pre-built macros for Excel automation
✅ **Professional Excel Reports** - Auto-generated with VBA tools sheet
✅ **Multi-Source Job Scraping** - Indeed, Naukri, Instahyre, RemoteOK
✅ **Intelligent Matching** - Fuzzy skill matching with accuracy
✅ **Bulk Processing** - Process multiple resumes at once
✅ **Clean Code** - Well-organized, documented, and tested

### Backend Modules
- `app.py` - Flask API (clean, 300 lines)
- `resume_parser.py` - Resume extraction
- `job_scraper.py` - Job scraping
- `job_matcher.py` - Matching algorithm
- `vba_export.py` - Excel generation
- `vba_macros_template.bas` - VBA macros

### Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run backend: `python app.py`
3. Run frontend: `npm start`
4. Upload resume → Export Excel → Add VBA macros → Run!

---

## Imp
lementation Summary

### ✅ What Was Done

**1. Modular Backend Architecture**
- Split monolithic `app.py` into 5 focused modules
- Each module handles one responsibility
- Easy to maintain, test, and extend

**2. VBA Automation Integration**
- Added VBA Automation Tools sheet to every Excel export
- 10 pre-built macros in `backend/vba_macros_template.bas`
- Copy-paste ready, no coding required

**3. Clean Code**
- Removed duplicate functions
- Consistent naming conventions
- Well-documented modules
- No syntax errors

**4. Comprehensive Documentation**
- VBA setup instructions in README
- Macro reference table
- Troubleshooting guide
- Pro tips and examples

### Backend Modules Breakdown

**app.py (300 lines)**
- Flask API endpoints
- Job caching logic
- Request handling
- Clean and focused

**resume_parser.py**
- PDF/DOCX/DOC extraction
- Email & phone extraction
- Skill detection (70+ skills)

**job_scraper.py**
- Multi-source scraping (4 sources)
- Fallback jobs
- Skill extraction from titles

**job_matcher.py**
- Fuzzy skill matching
- Match percentage calculation
- Filtering logic

**vba_export.py**
- Excel workbook generation
- VBA tools sheet creation
- Professional formatting

**vba_macros_template.bas**
- 10 production-ready macros
- Error handling
- User-friendly dialogs

### Files Removed
- ❌ VBA_SETUP_GUIDE.md (content in README)
- ❌ VBA_QUICK_REFERENCE.md (content in README)
- ❌ VBA_IMPLEMENTATION_SUMMARY.md (content in README)
- ❌ GETTING_STARTED_VBA.md (content in README)

### Files Created
- ✅ backend/resume_parser.py
- ✅ backend/job_scraper.py
- ✅ backend/job_matcher.py
- ✅ backend/vba_export.py

### Files Modified
- ✅ backend/app.py (cleaned and refactored)
- ✅ README.md (comprehensive VBA guide added)

---

**Status**: ✅ Complete and Ready to Use
**Version**: 1.0
**Last Updated**: January 10, 2026
