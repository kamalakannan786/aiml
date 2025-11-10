#!/bin/bash

echo "🚀 Setting up Smart Resume Checker..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Train ML model
echo "🧠 Training ML model..."
cd ml-service
python train_model.py
cd ..

# Install frontend dependencies
echo "⚛️ Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🏃♂️ To run the application:"
echo "1. Start ML service: cd ml-service && python app.py"
echo "2. Start backend: cd backend && python app.py"
echo "3. Start frontend: cd frontend && npm start"
echo ""
echo "Or use Docker: docker-compose up"