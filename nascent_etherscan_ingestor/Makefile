
# Stop and restart everything
all: stop clear build detached test
		@echo "Docker is running..."

# Stop and restart everything in detached mode
attached: stop clear build start
		@echo "Docker is running..."

start:
		./scripts/start.sh

build:
		./scripts/build.sh

clear:
		./scripts/clear.sh

stop:
		./scripts/stop.sh

detached:
		./scripts/detached_start.sh

lint:
		./scripts/lint.sh

test:
		./scripts/test.sh

run:
		./scripts/solution.sh
