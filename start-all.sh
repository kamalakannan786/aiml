#!/bin/bash

echo "🚀 Starting Smart Resume Checker..."

# Install missing dependencies
echo "📦 Installing dependencies..."
pip3 install --user flask flask-cors requests PyPDF2 mysql-connector-python

# Start ML Service
echo "🧠 Starting ML Service..."
cd ml-service && python3 app.py &
ML_PID=$!
cd ..

sleep 3

# Start Backend
echo "🔧 Starting Backend..."
cd backend && python3 app.py &
BACKEND_PID=$!
cd ..

sleep 3

# Start Frontend
echo "⚛️ Starting Frontend..."
cd frontend && npm start &
FRONTEND_PID=$!
cd ..

echo "✅ All services started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:5000"
echo "🧠 ML Service: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Cleanup function
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $ML_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup INT
wait