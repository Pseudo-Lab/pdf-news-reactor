# Makefile

# ============================
# Phony Targets
# ============================

.PHONY: prepare_image load_env login build logout

# ============================
# Variables
# ============================

# Docker configuration
PLATFORMS := linux/amd64,linux/arm64
DOCKERFILES := \
    python/Dockerfile.create_topic \
    python/Dockerfile.producer \
    python/Dockerfile.consumer

IMAGES := \
    create_reaction_topic \
    reaction_producer \
    reaction_consumer

# ============================
# Load Environment Variables (Optional)
# ============================

-include .env

# ============================
# prepare_image Target
# ============================

prepare_image: login build logout
	@echo "🎉 Images have been pushed to Docker Hub with tag $(IMAGE_TAG)."

# ============================
# login Target
# ============================

login:
	@echo "🔑 Logging into Docker Hub..."
	@echo "$(DOCKER_PASSWORD)" | docker login -u "$(DOCKER_USERNAME)" --password-stdin
	@echo "✅ Docker login successful."

# ============================
# build Target
# ============================

build:
	@echo "🏗️  Building Docker images..."
	@for i in $(shell seq 1 $(words $(DOCKERFILES))); do \
		Dockerfile=$$(echo $(DOCKERFILES) | cut -d' ' -f$$i); \
		Image=$$(echo $(IMAGES) | cut -d' ' -f$$i); \
		echo "Building $$Image using $$Dockerfile..."; \
		docker buildx build --platform $(PLATFORMS) \
			-t $(DOCKER_USERNAME)/$$Image:$(IMAGE_TAG) \
			-f $$Dockerfile --push python; \
	done
	@echo "✅ Docker images built successfully."

# ============================
# logout Target
# ============================

logout:
	@echo "🔒 Logging out from Docker Hub..."
	@docker logout
	@echo "✅ Docker logout successful."

