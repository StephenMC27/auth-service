# Start FastAPI service
start:
	fastapi dev app/main.py

# Format code
format:
	isort .
	black .