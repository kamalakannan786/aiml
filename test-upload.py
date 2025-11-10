#!/usr/bin/env python3

import requests
import json

# Test the upload endpoint
def test_upload():
    url = "http://localhost:5000/api/resume/upload"
    
    # Create a simple test file
    test_content = b"Sample resume content for testing"
    
    files = {
        'resume': ('test_resume.pdf', test_content, 'application/pdf')
    }
    
    data = {
        'user_email': 'test@example.com',
        'job_description': 'Python developer position'
    }
    
    try:
        response = requests.post(url, files=files, data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_upload()