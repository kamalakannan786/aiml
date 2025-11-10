-- Initialize database schema for Smart Resume Checker

USE resume_checker;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS resume_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (user_email),
    INDEX idx_created_at (created_at)
);

-- Insert sample data for testing
INSERT IGNORE INTO users (email, name) VALUES 
('demo@example.com', 'Demo User'),
('test@example.com', 'Test User');