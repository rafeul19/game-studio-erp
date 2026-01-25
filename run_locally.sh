#!/bin/bash

# Function to kill child processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "🚀 Starting Game Studio ERP Locally..."

# Check Backend
echo "📦 Setting up Backend..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1
python manage.py migrate > /dev/null 2>&1
echo "✅ Backend Setup Complete"

# Start Backend
echo "🔥 Starting Backend Server on http://localhost:8000"
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

# Start Frontend
cd ../frontend
echo "📦 Installing Frontend Dependencies (this might take a moment)..."
npm install > /dev/null 2>&1
echo "🔥 Starting Frontend Server on http://localhost:3000"
npm run dev &
FRONTEND_PID=$!

# Wait for both
wait $BACKEND_PID $FRONTEND_PID
