from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    try:
        # Simple mock analysis
        analysis = {
            'quality_score': 85.5,
            'ats_score': 78,
            'job_fit_score': 82,
            'found_skills': ['Python', 'JavaScript', 'Communication'],
            'missing_skills': ['Leadership', 'Project Management'],
            'recommendations': [
                'Add more quantifiable achievements',
                'Include relevant keywords for ATS optimization',
                'Strengthen your professional summary'
            ]
        }
        
        ai_suggestions = {
            'content_suggestions': [
                'Use action verbs to start bullet points',
                'Add metrics to demonstrate impact',
                'Tailor content to job requirements'
            ]
        }
        
        response = {
            'id': str(uuid.uuid4()),
            'analysis': analysis,
            'ai_suggestions': ai_suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5002)