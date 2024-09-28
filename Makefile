# Define service paths
MAIN_WEB_PATH = main-web
REC_MODEL_PATH = reccommendation-ai

# Phony targets ensure that the Makefile doesn't expect these to be actual files or directories
.PHONY: start stop rebuild status logs down down-v test-main test-all

# Start both services with a delay
start:
	@echo "Starting services..."
	@cd $(MAIN_WEB_PATH) && docker compose up -d --build
	@echo "Waiting for 5 seconds before starting recommendation-ai service..."
	@sleep 5
	@cd $(REC_MODEL_PATH) && docker compose up -d --build

# Stop both services
stop:
	@echo "Stopping services..."
	@cd $(MAIN_WEB_PATH) && docker compose down
	@cd $(REC_MODEL_PATH) && docker compose down

# Rebuild both services without -d (attached mode)
rebuild:
	@echo "Rebuilding services..."
	@cd $(MAIN_WEB_PATH) && docker compose up --build
	@cd $(REC_MODEL_PATH) && docker compose up --build

# Check status of both services
status:
	@echo "Checking service status..."
	@cd $(MAIN_WEB_PATH) && docker compose ps
	@cd $(REC_MODEL_PATH) && docker compose ps

# Show logs for both services
logs:
	@echo "Showing logs..."
	@cd $(MAIN_WEB_PATH) && docker compose logs
	@cd $(REC_MODEL_PATH) && docker compose logs

# Stop both services and remove volumes
down-v:
	@echo "Stopping services and removing volumes..."
	@cd $(MAIN_WEB_PATH) && docker compose down -v
	@cd $(REC_MODEL_PATH) && docker compose down -v

# Stop both services without removing volumes
down:
	@echo "Stopping services without removing volumes..."
	@cd $(MAIN_WEB_PATH) && docker compose down
	@cd $(REC_MODEL_PATH) && docker compose down

# Run tests for the main-web service
test-main:
	@echo "Running tests for main-web service..."
	@cd $(MAIN_WEB_PATH) && docker compose exec api python manage.py test tests

# Run tests for both main-web and recommendation-ai services
test-all: test-main