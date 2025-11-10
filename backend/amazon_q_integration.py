import boto3
import json
from typing import Dict, List

class AmazonQIntegration:
    def __init__(self, region='us-east-1'):
        self.bedrock = boto3.client('bedrock-runtime', region_name=region)
        
    def get_resume_suggestions(self, resume_text: str, ml_results: Dict) -> Dict:
        """Get AI-powered suggestions using Amazon Bedrock"""
        
        prompt = f"""
        Analyze this resume and provide specific improvement suggestions:
        
        Resume Text: {resume_text[:1000]}...
        
        Current Scores:
        - Quality Score: {ml_results.get('quality_score', 0)}/100
        - ATS Score: {ml_results.get('ats_score', 0)}/100
        - Job Fit Score: {ml_results.get('job_fit_score', 0)}/100
        
        Found Skills: {', '.join(ml_results.get('found_skills', []))}
        Missing Skills: {', '.join(ml_results.get('missing_skills', []))}
        
        Provide 3 specific, actionable suggestions to improve this resume:
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 500,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read())
            suggestions = result['content'][0]['text'].split('\n')
            
            return {
                'grammar_suggestions': ["Use active voice in bullet points"],
                'content_suggestions': [s.strip() for s in suggestions if s.strip()],
                'formatting_tips': ["Use consistent bullet point formatting", "Keep resume to 1-2 pages"]
            }
            
        except Exception as e:
            # Fallback suggestions if Amazon Q is not available
            return {
                'grammar_suggestions': ["Use active voice in bullet points"],
                'content_suggestions': [
                    "Add quantifiable achievements to your experience section",
                    "Include more technical keywords relevant to your target role",
                    "Improve the professional summary with specific accomplishments"
                ],
                'formatting_tips': ["Use consistent bullet point formatting"]
            }
    
    def analyze_resume_content(self, resume_text: str) -> Dict:
        """Analyze resume content for grammar and structure"""
        
        prompt = f"""
        Analyze this resume for grammar, structure, and professional tone:
        
        {resume_text[:1500]}
        
        Provide feedback on:
        1. Grammar and language issues
        2. Professional tone
        3. Structure and organization
        4. Missing sections
        
        Be specific and actionable.
        """
        
        try:
            response = self.bedrock.invoke_model(
                modelId='anthropic.claude-3-sonnet-20240229-v1:0',
                body=json.dumps({
                    'anthropic_version': 'bedrock-2023-05-31',
                    'max_tokens': 400,
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                })
            )
            
            result = json.loads(response['body'].read())
            return {'analysis': result['content'][0]['text']}
            
        except Exception as e:
            return {
                'analysis': 'Amazon Q analysis temporarily unavailable. Using ML-based analysis.'
            }