import mysql.connector
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        self.config = {
            'host': 'localhost',
            'user': 'app_user',
            'password': 'app_password',
            'database': 'resume_checker'
        }
    
    def get_connection(self):
        return mysql.connector.connect(**self.config)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resume_analysis (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_email VARCHAR(255),
                resume_filename VARCHAR(255),
                resume_text TEXT,
                job_description TEXT,
                quality_score FLOAT,
                ats_score FLOAT,
                job_fit_score FLOAT,
                found_skills JSON,
                missing_skills JSON,
                recommendations JSON,
                ai_suggestions JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE,
                name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def save_analysis(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO resume_analysis 
            (user_email, resume_filename, resume_text, job_description, 
             quality_score, ats_score, job_fit_score, found_skills, 
             missing_skills, recommendations, ai_suggestions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            data.get('user_email'),
            data.get('filename'),
            data.get('resume_text'),
            data.get('job_description'),
            data.get('quality_score'),
            data.get('ats_score'),
            data.get('job_fit_score'),
            json.dumps(data.get('found_skills', [])),
            json.dumps(data.get('missing_skills', [])),
            json.dumps(data.get('recommendations', [])),
            json.dumps(data.get('ai_suggestions', {}))
        )
        
        cursor.execute(query, values)
        analysis_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return analysis_id
    
    def get_user_history(self, email):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT id, resume_filename, quality_score, ats_score, 
                   job_fit_score, created_at
            FROM resume_analysis 
            WHERE user_email = %s 
            ORDER BY created_at DESC
        """
        
        cursor.execute(query, (email,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results