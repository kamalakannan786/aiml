import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import nltk
import re

# Download required NLTK data
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
except:
    pass

class ResumeModelTrainer:
    def __init__(self):
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def create_sample_data(self):
        """Create sample training data for demonstration"""
        sample_resumes = [
            "Python developer with 3 years experience in machine learning and data science. Built REST APIs using Flask and Django.",
            "Java software engineer with Spring Boot experience. Worked on microservices architecture and AWS cloud deployment.",
            "Frontend developer skilled in React, JavaScript, and CSS. Created responsive web applications with modern UI frameworks.",
            "Data scientist with expertise in Python, SQL, and machine learning. Experience with TensorFlow and scikit-learn.",
            "DevOps engineer with Docker, Kubernetes, and AWS experience. Automated CI/CD pipelines using Jenkins.",
            "Full-stack developer with Node.js and React experience. Built scalable web applications with MongoDB database.",
            "Mobile app developer with React Native and Flutter experience. Published apps on iOS and Android platforms.",
            "Backend engineer with Python and PostgreSQL experience. Designed database schemas and optimized query performance."
        ]
        
        # Quality scores (0-100)
        quality_scores = [85, 78, 82, 90, 88, 75, 80, 86]
        
        return pd.DataFrame({
            'resume_text': sample_resumes,
            'quality_score': quality_scores
        })
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text
    
    def train_model(self, data):
        """Train the resume quality prediction model"""
        # Preprocess text
        data['cleaned_text'] = data['resume_text'].apply(self.preprocess_text)
        
        # Create TF-IDF features
        X = self.tfidf.fit_transform(data['cleaned_text']).toarray()
        y = data['quality_score']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"MSE: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")
        
        return self.model, self.tfidf
    
    def save_model(self, model_path='models/resume_quality_model.pkl', 
                   tfidf_path='models/tfidf_vectorizer.pkl'):
        """Save trained model and vectorizer"""
        import os
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.tfidf, tfidf_path)
        print(f"Model saved to {model_path}")
        print(f"Vectorizer saved to {tfidf_path}")

if __name__ == "__main__":
    trainer = ResumeModelTrainer()
    
    # Create sample data (in production, load from CSV)
    data = trainer.create_sample_data()
    print(f"Training with {len(data)} samples")
    
    # Train model
    model, tfidf = trainer.train_model(data)
    
    # Save model
    trainer.save_model()
    
    print("Training completed successfully!")