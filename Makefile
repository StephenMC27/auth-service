# Start FastAPI service
start:
	fastapi dev app/main.py

# Sort imports and format code
format:
	isort .
	black .

# Run unit tests
unit-test:
	pytest test/