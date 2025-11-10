#!/bin/bash

echo "🚀 Starting Smart Resume Checker..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Train ML model
echo "🧠 Training ML model..."
cd ml-service && python3 train_model.py && cd ..

# Install frontend dependencies
echo "⚛️ Installing frontend dependencies..."
cd frontend && npm install && cd ..

echo "🏃♂️ Starting services..."

# Start ML service in background
echo "🧠 Starting ML Service on port 5001..."
(cd ml-service && python3 app.py) &
ML_PID=$!

sleep 3

# Start backend in background
echo "🔧 Starting Backend API on port 5000..."
(cd backend && python3 app.py) &
BACKEND_PID=$!

sleep 3

# Start frontend
echo "🌐 Starting Frontend on port 3000..."
(cd frontend && npm start) &
FRONTEND_PID=$!

echo "✅ All services started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:5000"
echo "🧠 ML Service: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for services
wait

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $ML_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT