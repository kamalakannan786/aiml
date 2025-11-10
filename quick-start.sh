#!/bin/bash

echo "🚀 Quick Start - Smart Resume Checker"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --user -r requirements.txt

# Train ML model
echo "🧠 Training ML model..."
cd ml-service
python3 train_model.py
cd ..

# Install frontend dependencies
echo "⚛️ Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "🏃♂️ Starting services..."

# Start ML service
cd ml-service
python3 app.py &
cd ..

sleep 3

# Start backend
cd backend  
python3 app.py &
cd ..

sleep 3

# Start frontend
cd frontend
npm start

echo "🌐 Access at: http://localhost:3000"