from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re
import numpy as np

app = Flask(__name__)
CORS(app)

class ResumeAnalyzer:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        self.quality_model = None
        self.skills_keywords = [
            'python', 'java', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 
            'kubernetes', 'machine learning', 'data science', 'tensorflow', 'pytorch'
        ]
        
    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def extract_skills(self, text):
        found_skills = []
        text_lower = text.lower()
        for skill in self.skills_keywords:
            if skill in text_lower:
                found_skills.append(skill)
        return found_skills
    
    def calculate_ats_score(self, text):
        sections = ['experience', 'education', 'skills', 'projects']
        score = 0
        for section in sections:
            if section in text.lower():
                score += 25
        return min(score, 100)
    
    def analyze_resume(self, resume_text, job_description=""):
        # Preprocess
        clean_text = self.preprocess_text(resume_text)
        
        # Extract skills
        found_skills = self.extract_skills(resume_text)
        
        # Calculate ATS score
        ats_score = self.calculate_ats_score(resume_text)
        
        # Basic quality scoring
        word_count = len(clean_text.split())
        quality_score = min(50 + (word_count / 10), 100)
        
        # Job fit analysis
        job_fit_score = 75  # Default
        missing_skills = []
        
        if job_description:
            job_skills = self.extract_skills(job_description)
            common_skills = set(found_skills) & set(job_skills)
            job_fit_score = (len(common_skills) / max(len(job_skills), 1)) * 100
            missing_skills = list(set(job_skills) - set(found_skills))
        
        return {
            'quality_score': round(quality_score, 1),
            'ats_score': ats_score,
            'job_fit_score': round(job_fit_score, 1),
            'found_skills': found_skills,
            'missing_skills': missing_skills,
            'recommendations': self.generate_recommendations(quality_score, ats_score, missing_skills)
        }
    
    def generate_recommendations(self, quality_score, ats_score, missing_skills):
        recommendations = []
        
        if quality_score < 70:
            recommendations.append("Add more detailed work experience with quantifiable achievements")
        
        if ats_score < 80:
            recommendations.append("Include standard resume sections: Experience, Education, Skills")
        
        if missing_skills:
            recommendations.append(f"Consider adding these skills: {', '.join(missing_skills[:3])}")
        
        return recommendations

analyzer = ResumeAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        result = analyzer.analyze_resume(resume_text, job_description)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)