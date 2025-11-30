# AI Resume Parser & Job Matcher

A modern full-stack web application that intelligently parses resumes and recommends personalized job matches using machine learning algorithms. Features a sleek dark-themed UI with comprehensive ML model analysis and visualizations.

## Features

### Core Functionality
- Drag & drop resume upload (.docx format)
- Automatic skill extraction from resumes
- Smart job matching algorithm (10+ job categories)
- Real-time match percentage calculation
- Email and phone number extraction

### ML Analysis Dashboard
- Three ML models comparison (Decision Tree, Logistic Regression, Random Forest)
- Confusion matrices for each model
- ROC curves with AUC scores
- Feature importance visualization
- 5-fold cross-validation results
- Detailed classification reports
- Model performance comparison charts

### UI/UX
- Dark theme with yellow accents (black, white, grey, dark blue, yellow palette)
- Smooth animations with Framer Motion
- Responsive design for all screen sizes
- Professional data visualizations

## Tech Stack

### Frontend
- React 18
- Framer Motion (animations)
- React Dropzone (file upload)
- Axios (API calls)
- Custom SVG visualizations

### Backend
- Flask (REST API)
- Python-docx (document parsing)
- NumPy (numerical computations)
- Regex (pattern matching)

### ML Models (Simulated)
- Decision Tree Classifier
- Logistic Regression
- Random Forest Classifier

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to backend folder:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

Backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend folder:
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

Frontend will run on `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Drag and drop your resume (.docx format) or click to browse
3. Wait for the AI to analyze your resume
4. View extracted information:
   - Email address
   - Phone number
   - Detected skills
5. Browse personalized job recommendations with match percentages
6. Click "Show ML Analysis" to view:
   - Model performance metrics
   - Confusion matrices
   - ROC curves
   - Feature importance
   - Cross-validation scores
   - Classification reports

## Job Categories

The system matches resumes against 10 job categories:
- Data Scientist
- Machine Learning Engineer
- Full Stack Developer
- Backend Developer
- Frontend Developer
- DevOps Engineer
- Data Analyst
- Software Engineer
- Mobile Developer
- Cloud Architect

## How Job Matching Works

1. **Skill Extraction**: Scans resume for relevant technical skills
2. **Skill Matching**: Compares resume skills with job requirements
3. **Score Calculation**: `(Matching Skills / Required Skills) × 100`
4. **Ranking**: Returns top 5 jobs sorted by match percentage
5. **Display**: Shows matching skills for each recommended job

## Project Structure

```
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── Results.js
│   │   │   └── AdvancedAnalysis.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── uploads/
├── Datasets/
│   └── (sample resumes)
├── Resume_parser.ipynb
├── README.md
└── .gitignore
```

## API Endpoints

### POST `/api/upload`
Upload and analyze resume

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (resume.docx)

**Response:**
```json
{
  "success": true,
  "filename": "resume.docx",
  "email": "user@example.com",
  "phone": "+1234567890",
  "skills": ["python", "machine learning", "react"],
  "jobs": [
    {
      "title": "Data Scientist",
      "company": "Tech Corp",
      "match": 85.7,
      "description": "...",
      "matching_skills": ["python", "machine learning"]
    }
  ],
  "ml_analysis": { ... }
}
```

### GET `/api/health`
Health check endpoint

## ML Metrics Explained

- **Accuracy**: Overall correctness of predictions
- **Precision**: Accuracy of positive predictions
- **Recall**: Ability to find all positive cases
- **F1 Score**: Harmonic mean of precision and recall
- **AUC**: Area Under ROC Curve (model discrimination ability)
- **Confusion Matrix**: True/False Positives and Negatives

## Future Enhancements

- [ ] PDF resume support
- [ ] Real ML model training with actual data
- [ ] User authentication and profiles
- [ ] Resume database and history
- [ ] Advanced NLP for better skill extraction
- [ ] Company-specific job matching
- [ ] Resume improvement suggestions
- [ ] Export analysis to PDF
- [ ] Multi-language support
- [ ] Integration with job boards APIs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Acknowledgments

- Built with React and Flask
- ML concepts inspired by scikit-learn
- UI design inspired by modern dark themes
- Sample resumes in Datasets folder for testing

## Contact

For questions or suggestions, please open an issue on GitHub.

---

**Note**: This is a demonstration project. The ML models use simulated data for visualization purposes. For production use, train models with real resume datasets.
