# Activate venv
& .\venv\Scripts\Activate.ps1

# Test PostgreSQL connection
Write-Host "Testing PostgreSQL connection..."
$env:PGPASSWORD = 'postgres'
psql -U postgres -h localhost -c "SELECT 1" 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ PostgreSQL is running" -ForegroundColor Green
    
    # Check if database exists
    psql -U postgres -h localhost -c "SELECT 1 FROM pg_database WHERE datname='rag_chatbot_db'" 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database exists" -ForegroundColor Green
    } else {
        Write-Host "Database not found. Please create it first." -ForegroundColor Yellow
    }
} else {
    Write-Host "✗ PostgreSQL is not running or not accessible" -ForegroundColor Red
    Write-Host "Please start PostgreSQL service and try again" -ForegroundColor Yellow
    exit 1
}

# Run migrations
Write-Host "`nRunning migrations..."
python manage.py migrate

# Start the server
Write-Host "`nStarting Django development server..."
Write-Host "Backend available at: http://localhost:8000" -ForegroundColor Cyan
python manage.py runserver
