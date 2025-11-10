#!/bin/bash

echo "🚀 Starting Smart Resume Checker Services..."

# Start MySQL (if not running)
echo "📊 Starting MySQL database..."
brew services start mysql 2>/dev/null || echo "MySQL may already be running"

# Wait for MySQL to be ready
sleep 3

# Start ML Service
echo "🧠 Starting ML Service..."
cd ml-service
python app.py &
ML_PID=$!
cd ..

# Wait for ML service to start
sleep 5

# Start Backend
echo "🔧 Starting Backend API..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

# Start Frontend
echo "⚛️ Starting Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ All services started!"
echo ""
echo "🌐 Access the application at: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "🧠 ML Service: http://localhost:5001"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $ML_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for user to stop
wait