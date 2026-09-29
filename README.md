# AI Smart Resume–Job Matcher

An AI-powered web application that analyzes a candidate's resume against a job description using semantic similarity, skill matching, entity matching, and personalized skill recommendations.

## Project Overview

The AI Smart Resume–Job Matcher helps job seekers understand how well their resume aligns with a specific job description.

The application accepts resumes in PDF, DOCX, or TXT format and compares the extracted resume content with the provided job description. It uses a Sentence Transformer model to calculate semantic similarity and identifies matching and missing skills.

## Key Features

* Resume upload in PDF, DOCX, and TXT formats
* AI-based semantic similarity analysis
* Resume-to-job matching score
* Matching skills identification
* Missing skills identification
* Related skill recommendations
* Semantic entity matching between resume and job requirements
* Resume content analysis
* Improvement suggestions
* Interactive Streamlit dashboard
* PDF analysis report generation

## Technologies Used

* Python
* Streamlit
* Sentence Transformers
* Scikit-learn
* PyMuPDF
* python-docx
* Pandas
* ReportLab

## AI Model

The project uses the `all-MiniLM-L6-v2` Sentence Transformer model for generating text embeddings.

The embeddings are compared using cosine similarity to measure the semantic relationship between the resume and job description.

> The similarity percentage represents semantic similarity between the provided texts. It should not be interpreted as a guaranteed hiring probability or an objective qualification percentage.

## System Workflow

```text
Resume Upload
      ↓
Resume Text Extraction
      ↓
Text Preprocessing
      ↓
AI Embedding Generation
      ↓
Semantic Similarity Analysis
      ↓
Skill Extraction & Comparison
      ↓
Missing Skill Identification
      ↓
Related Skill Recommendations
      ↓
Semantic Entity Matching
      ↓
Resume Improvement Suggestions
      ↓
PDF Report
```

## Project Structure

```text
AI-Resume-Matcher/
│
├── app.py
├── requirements.txt
├── .gitignore
│
└── modules/
    ├── entity_matcher.py
    ├── matcher.py
    ├── recommender.py
    └── skill_extractor.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/murugesH-3/AI-Resume-Matcher.git
```

### 2. Open the project folder

```bash
* Support for more resume formats
* Job recommendation based on resume content
* Resume keyword optimization
* Resume section quality analysis


This project is intended as an assistive tool for resume analysis. Its similarity score and recommendations are based on the implemented AI and rule-based techniques and should not be treated as a definitive hiring decision.

## Author
**Murugesh**

GitHub: https://github.com/murugesH-3

## Disclaimer
* Local or optimized AI model deployment
* Improved multilingual resume analysis
* Integration with job portals
* Larger and customizable skill databases
* Improved entity recognition
```bash
## Future Enhancements

pip install -r requirements.txt
8. Download the generated PDF report.

```
7. Examine semantic matches between job requirements and resume content.

5. Check matching and missing skills.
6. Review related skill recommendations.
2. Enter or paste the target job description.
3. Click **Analyze Resume**.
4. Review the semantic similarity score.

1. Upload your resume.
The application will open in your web browser.

## How to Use
streamlit run app.py
```


```bash
## Running the Application

Start the Streamlit application using:
### 5. Install dependencies

```bash
```


```bash
venv\Scripts\activate
### 4. Activate the virtual environment

On Windows:
python -m venv venv
```

cd AI-Resume-Matcher
```


