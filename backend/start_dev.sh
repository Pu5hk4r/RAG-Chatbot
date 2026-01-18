# start_dev.sh - Development startup script
#!/bin/bash
# Start all services for development

echo "🚀 Starting RAG Chatbot (Development Mode)"

# Function to cleanup on exit
cleanup() {
    echo "
🛑 Stopping services..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup EXIT INT TERM

# Start Redis
echo "📡 Starting Redis..."
redis-server --daemonize yes

# Start Celery Worker
echo "👷 Starting Celery Worker..."
celery -A config worker -l info &

# Start Celery Beat
echo "⏰ Starting Celery Beat..."
celery -A config beat -l info &

# Wait a bit for services to start
sleep 2

# Start Django
echo "🌐 Starting Django..."
python manage.py runserver

# Keep script running
wait
