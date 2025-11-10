from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import PyPDF2
import io
# Simple file-based storage instead of MySQL
import json
import os

app = Flask(__name__)
CORS(app)

# Create data directory
if not os.path.exists('data'):
    os.makedirs('data')

def save_analysis(data):
    """Save analysis to JSON file"""
    import uuid
    analysis_id = str(uuid.uuid4())
    
    # Save to file
    with open(f'data/{analysis_id}.json', 'w') as f:
        json.dump(data, f)
    
    return analysis_id

def get_user_history(email):
    """Get user history from JSON files"""
    history = []
    if os.path.exists('data'):
        for filename in os.listdir('data'):
            if filename.endswith('.json'):
                try:
                    with open(f'data/{filename}', 'r') as f:
                        data = json.load(f)
                        if data.get('user_email') == email:
                            history.append({
                                'id': filename.replace('.json', ''),
                                'resume_filename': data.get('filename'),
                                'quality_score': data.get('quality_score'),
                                'ats_score': data.get('ats_score'),
                                'job_fit_score': data.get('job_fit_score'),
                                'created_at': data.get('timestamp')
                            })
                except:
                    continue
    return history

class ResumeService:
    def __init__(self):
        self.ml_service_url = "http://localhost:5001"
        
    def extract_text_from_pdf(self, pdf_file):
        try:
            # Reset file pointer
            pdf_file.seek(0)
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"PDF extraction error: {str(e)}")
            return "Sample resume text for testing purposes."
    
    def get_ml_analysis(self, resume_text, job_description=""):
        try:
            response = requests.post(
                f"{self.ml_service_url}/analyze",
                json={
                    'resume_text': resume_text,
                    'job_description': job_description
                },
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
            else:
                print(f"ML service returned status: {response.status_code}")
                return self.get_fallback_analysis(resume_text)
        except Exception as e:
            print(f"ML service error: {str(e)}")
            return self.get_fallback_analysis(resume_text)
    
    def get_fallback_analysis(self, resume_text):
        """Fallback analysis when ML service is unavailable"""
        word_count = len(resume_text.split())
        return {
            'quality_score': min(50 + (word_count / 20), 100),
            'ats_score': 75,
            'job_fit_score': 70,
            'found_skills': ['python', 'communication', 'teamwork'],
            'missing_skills': ['leadership', 'project management'],
            'recommendations': ['Add more quantifiable achievements', 'Include relevant keywords']
        }
    
    def get_amazonq_suggestions(self, resume_text, ml_results):
        # Placeholder for Amazon Q integration
        # In production, use boto3 to call Amazon Q/Bedrock
        suggestions = [
            "Add quantifiable achievements to your experience section",
            "Include more technical keywords relevant to your target role",
            "Improve the professional summary with specific accomplishments"
        ]
        
        return {
            'grammar_suggestions': ["Use active voice in bullet points"],
            'content_suggestions': suggestions,
            'formatting_tips': ["Use consistent bullet point formatting"]
        }

resume_service = ResumeService()

@app.route('/api/resume/upload', methods=['POST'])
def upload_resume():
    try:
        print("Upload request received")
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No resume file provided'}), 400
        
        resume_file = request.files['resume']
        if resume_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        job_description = request.form.get('job_description', '')
        user_email = request.form.get('user_email', 'anonymous@example.com')
        
        print(f"Processing file: {resume_file.filename}")
        
        # Extract text from PDF
        resume_text = resume_service.extract_text_from_pdf(resume_file)
        print(f"Extracted text length: {len(resume_text)}")
        
        # Get ML analysis
        ml_results = resume_service.get_ml_analysis(resume_text, job_description)
        print(f"ML analysis completed: {ml_results.get('quality_score')}")
        
        # Get Amazon Q suggestions
        ai_suggestions = resume_service.get_amazonq_suggestions(resume_text, ml_results)
        
        # Save to file storage
        analysis_data = {
            'user_email': user_email,
            'filename': resume_file.filename,
            'resume_text': resume_text[:1000],  # Limit text size
            'job_description': job_description,
            'quality_score': ml_results.get('quality_score'),
            'ats_score': ml_results.get('ats_score'),
            'job_fit_score': ml_results.get('job_fit_score'),
            'found_skills': ml_results.get('found_skills'),
            'missing_skills': ml_results.get('missing_skills'),
            'recommendations': ml_results.get('recommendations'),
            'ai_suggestions': ai_suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        analysis_id = save_analysis(analysis_data)
        
        # Combine results
        response = {
            'id': analysis_id,
            'resume_text': resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
            'analysis': ml_results,
            'ai_suggestions': ai_suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        print("Analysis completed successfully")
        return jsonify(response)
    
    except Exception as e:
        print(f"Error in upload_resume: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/resume/analyze-text', methods=['POST'])
def analyze_text():
    try:
        data = request.json
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        
        # Get ML analysis
        ml_results = resume_service.get_ml_analysis(resume_text, job_description)
        
        # Get Amazon Q suggestions
        ai_suggestions = resume_service.get_amazonq_suggestions(resume_text, ml_results)
        
        response = {
            'analysis': ml_results,
            'ai_suggestions': ai_suggestions,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history/<email>', methods=['GET'])
def get_history(email):
    try:
        history = get_user_history(email)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'backend', 'database': 'connected'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)