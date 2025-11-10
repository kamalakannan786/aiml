#!/bin/bash

echo "🧪 Testing Services..."

# Test ML Service
echo "Testing ML Service (port 5001)..."
curl -s http://localhost:5001/health || echo "❌ ML Service not running"

# Test Backend
echo "Testing Backend (port 5000)..."
curl -s http://localhost:5000/api/health || echo "❌ Backend not running"

# Test Frontend
echo "Testing Frontend (port 3000)..."
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend running" || echo "❌ Frontend not running"

echo "Done!"