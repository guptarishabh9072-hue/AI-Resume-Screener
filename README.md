# AI Resume Screening System

An AI-powered Applicant Tracking System (ATS) that analyzes resumes against job descriptions, calculates compatibility scores, identifies skill gaps, and provides actionable recommendations for job seekers.

## Project Overview

This system leverages Natural Language Processing (NLP) techniques including TF-IDF vectorization, cosine similarity, and rule-based skill matching to evaluate how well a resume aligns with a specific job description. It provides a professional dashboard interface built with Streamlit for interactive analysis.

## Features

### Core Features
- **Resume Upload & Parsing** - Upload PDF resumes and extract text content using PDFPlumber
- **Job Description Input** - Paste job descriptions for comparison
- **ATS Score Calculation** - Multi-component scoring using TF-IDF and cosine similarity
- **Skill Gap Analysis** - Identify matching, missing, and extra skills
- **Recommendation Engine** - Personalized skill learning recommendations

### Dashboard Features
- Professional recruiter-style UI
- Interactive ATS Score Gauge
- KPI Cards with key metrics
- Skill Distribution Radar Chart
- Score Breakdown Bar Chart
- Skills by Category Pie Chart
- Tabbed Recommendations Section
- Downloadable PDF Reports

### Candidate Suitability Levels
- **Excellent** (80+): Strong alignment with job requirements
- **Good** (60-79): Good match with some skill gaps
- **Average** (40-59): Moderate match, significant upskilling needed
- **Poor** (<40): Low alignment, major skill gaps

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. Clone the repository or download the project files:
```bash
cd AI-Resume-Screener
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the project directory:
```bash
cd AI-Resume-Screener
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your browser and navigate to `http://localhost:8501`

4. Upload your resume PDF and paste the job description

5. Click **"Analyze Resume"** to get your results

## Project Structure

```
AI-Resume-Screener/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── .gitignore                      # Git ignore rules
│
├── data/
│   └── skills_database.csv         # Skills database (150+ skills)
│
├── src/
│   ├── __init__.py                 # Package initializer
│   ├── resume_parser.py            # PDF text extraction & parsing
│   ├── skill_extractor.py          # Skill extraction & matching
│   ├── ats_scorer.py               # ATS score calculation
│   ├── recommendation_engine.py    # Career recommendations
│   └── utils.py                    # Utility functions
│
├── outputs/                        # Generated reports
└── screenshots/                    # Application screenshots
```

## Screenshots

Screenshots are saved in the `screenshots/` folder. To capture screenshots:

1. Run the application
2. Upload a sample resume
3. Enter a job description
4. Click Analyze
5. Take screenshots of each section
6. Save them in the `screenshots/` folder

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Web application framework |
| PDFPlumber | PDF text extraction |
| Pandas | Data manipulation |
| Scikit-Learn | TF-IDF, Cosine Similarity |
| Plotly | Interactive visualizations |
| ReportLab | PDF report generation |

## How It Works

### 1. Resume Parsing
- Extracts text from uploaded PDF using PDFPlumber
- Cleans and normalizes text
- Identifies resume sections (experience, education, skills, etc.)
- Extracts contact information (email, phone)

### 2. Skill Extraction
- Loads a predefined skills database (150+ skills across 8 categories)
- Uses pattern matching to find skills in text
- Supports both single-word and multi-word (compound) skills
- Groups skills by category

### 3. ATS Score Calculation
- **Text Similarity (35%)**: TF-IDF + cosine similarity between resume and JD
- **Keyword Match (35%)**: Density of JD keywords found in resume
- **Format Score (15%)**: Resume formatting quality
- **Section Coverage (15%)**: Presence of important resume sections

### 4. Skill Gap Analysis
- Matching skills (intersection of resume and JD skills)
- Missing skills (in JD but not in resume)
- Extra skills (in resume but not required by JD)

### 5. Recommendations
- Prioritized skill learning suggestions
- Career improvement recommendations
- Resume writing tips

## Future Enhancements

- [ ] Support for DOCX resume format
- [ ] Multi-language support
- [ ] Bulk resume processing and ranking
- [ ] Integration with job boards APIs
- [ ] Machine learning-based skill importance weighting
- [ ] Resume template suggestions
- [ ] Historical analysis tracking
- [ ] User authentication and saved analyses
- [ ] Export to multiple formats (HTML, JSON)
- [ ] Real-time job description analysis

## Sample Skills Database

The skills database includes 150+ skills across 8 categories:

- **Programming Languages**: Python, Java, JavaScript, SQL, etc.
- **Data Science**: Machine Learning, Deep Learning, NLP, etc.
- **Libraries & Frameworks**: TensorFlow, PyTorch, Scikit-Learn, etc.
- **Cloud & DevOps**: AWS, Docker, Kubernetes, CI/CD, etc.
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, etc.
- **Data Engineering**: Spark, Kafka, Airflow, ETL, etc.
- **Visualization**: Tableau, Power BI, Plotly, etc.
- **Soft Skills**: Communication, Leadership, Problem Solving, etc.

## License

This project is created for educational purposes as an MSc Data Science portfolio project.

## Acknowledgments

- Streamlit for the amazing web framework
- PDFPlumber for PDF text extraction
- Scikit-Learn for ML utilities
- The open-source NLP community
